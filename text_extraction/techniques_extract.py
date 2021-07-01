from text_extraction import models
from nltk import tokenize
from nltk.stem.snowball import SnowballStemmer
import itertools
import math
from collections import defaultdict
from numpy import dot
import re
import numpy as np
np.seterr('raise')


class TechniquesExtractor:
    def __init__(self, text):
        self.text = text
        sentences, words, lexemes = self.load_source_text()
        self.sentences = sentences
        self.words = words
        self.lexemes = lexemes
        self.lexicon = set(itertools.chain(*lexemes))
        self.inverted_lexicon = dict((word, i) for i, word in enumerate(self.lexicon))
        self.WF = [defaultdict(int) for _ in lexemes]
        self.DF = defaultdict(int)
        for i, doc in enumerate(lexemes):
            for word in doc:
                self.WF[i][word] += 1
            for word in set(doc):
                self.DF[word] += 1
        self.TDM = self.create_tdm(lexemes)

    def search(self, query, top=5, min_value=0.05):

        ranked_result = []
        v = self.to_vector(self.q2stem(query))
        for i, vect in enumerate(self.TDM):
            ranked_result.append(
                (
                    dot(v, vect) / (dot(v, v) * dot(vect, vect)),  # cosine
                    self.sentences[i]
                )
            )
        ranked_result.sort(reverse=True)
        return [item for item in ranked_result[:top] if item[0] >= min_value]

    def load_source_text(self):
        stemmer = SnowballStemmer("english")
        sentences = []
        words = []
        lexemes = []
        text = self.text
        sentences = tokenize.sent_tokenize(text)
        for sentence in sentences:
            s_words = [word for word
                       in tokenize.word_tokenize(sentence)
                       if word not in (',', '.', ':', '-', ';', '?', '!', '"', "``", "`", "''")
                       ]
            s_lexemes = [stemmer.stem(word) for word in s_words]
            words.append(s_words)
            lexemes.append(s_lexemes)

        return sentences, words, lexemes

    def q2stem(self, query):
        stemmer = SnowballStemmer("english")
        return [stemmer.stem(word) for word in tokenize.word_tokenize(query.lower())]

    def exact_match(self, query):
        result = []
        q = set(self.q2stem(query))
        for i, sentence in enumerate(self.lexemes):
            if set(sentence).intersection(q) == q:
                result.append(self.sentences[i])
        return result

    def ranked_match(self, query, top=5):
        ranked_result = []
        q = set(self.q2stem(query))
        for i, sent in enumerate(self.lexemes):
            ranked_result.append(
                (
                    len(set(sent).intersection(q)),
                    self.sentences[i]
                )
            )
        ranked_result.sort(reverse=True)
        return [item[1] for item in ranked_result[:top]]

    def construct_lookup(self, lexemes):
        result = dict()
        for i, lx in enumerate(lexemes):
            for lexeme in lx:
                if lexeme not in result: result[lexeme] = set()
                result[lexeme].add(i)
        return result

    def tf(self, word, doc_i):
        return self.WF[doc_i][word] / len(self.lexemes[doc_i])

    def idf(self, word):
        return -math.log(self.DF[word] / len(self.lexemes))

    # use the same method to buid a vector for documents (just use lookup) and for new queries
    def to_vector(self, tokens, i=None):
        result = list([0] * len(self.lexicon))
        local_tf = {}
        if i is None:
            local_tf = dict((word, tokens.count(word)) for word in set(tokens))
        for word in tokens:
            if word in self.lexicon:
                if i is None:
                    result[self.inverted_lexicon[word]] = local_tf[word] * self.idf(word)
                else:
                    result[self.inverted_lexicon[word]] = self.tf(word, i) * self.idf(word)
        return result

    def create_tdm(self, lexemes):
        result = []
        for i, sent in enumerate(lexemes):
            result.append(self.to_vector(sent, i))
        return result


def search_techniques(text):
    extractor = TechniquesExtractor(text)
    techniques = models.Technique.select()
    extracted = set()
    for technique in techniques:
        try:
            data = extractor.search(technique.description)
            if data:
                extracted.add(technique.name)
        except FloatingPointError:
            pass
    techniques = set(map(lambda x: re.escape(x.name), techniques))
    techniques = '|'.join(techniques)
    extracted.update(map(lambda x: x.lower(), re.findall(techniques, text, re.I)))
    return extracted
