from nltk import pos_tag, ne_chunk, word_tokenize, tree, tokenize
import json
import re


def extract_all_names(raw):
    toks = word_tokenize(raw)
    pos = pos_tag(toks)
    chunked_nes = ne_chunk(pos)
    return set([' '.join(map(lambda x: x[0], ne.leaves()))
                for ne in chunked_nes if isinstance(ne, tree.Tree)])


def extract_special_words(text):
    stop_words = json.load(open('files/words.json'))
    words = set()
    sentences = tokenize.sent_tokenize(text.lower())
    for sentence in sentences:
        s_words = [word for word
                   in tokenize.word_tokenize(sentence)
                   if word not in (',', '.', ':', '-', ';', '?', '!', '...',
                                   '"', "``", "`", "''", "[", "]", "(", ")", "@", '–', '&')
                   ]
        filtered_words = [word.strip() for word in s_words if word not in stop_words]
        words.update(filtered_words)
    return set([i for i in words if check_special_word(i)])


def check_special_word(word):
    return not re.match(r'\d+([.:]\d*)*', word) \
           and not re.match(r'//(www\.)?(?:[-\w.]|(?:%[\da-fA-F]{2}))+', word) \
           and not re.match(r'([\\/]?.*?\.[\w:]+)', word) \
           and len(word) > 2 and '\x00' not in word


def clear_special_words(words):
    file_extensions = map(lambda x: x.replace('.', ''), open('files/file_extensions.txt').readlines())
    return set(filter(lambda x: not x
                      .startswith('-') and not x
                      .endswith('-') and re
                      .match(r'^[A-Za-z0-9_/-]+$', x) and x not in file_extensions, words))
