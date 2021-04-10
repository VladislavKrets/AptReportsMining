import nltk
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# nltk.download() при первом запуске раскомментить и скачать всё

f = open('chatbot.txt', 'r', errors='ignore')
raw = f.read()
raw = raw.lower()
sent_tokens = nltk.sent_tokenize(raw, language='russian')  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw, language='russian')  # converts to list of words
lemmer = nltk.stem.WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


def response():
    robo_response = ''
    russian_stopwords = stopwords.words("russian")
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=None)
    TfidfVec.stop_words_ = russian_stopwords
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if req_tfidf == 0:
        robo_response = robo_response + "Я вас не понял"
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
        return robo_response


flag = True
while flag:
    user_response = input()
    user_response = user_response.lower()
    sent_tokens.append(user_response)
    word_tokens = word_tokens + nltk.word_tokenize(user_response)
    final_words = list(set(word_tokens))
    print(response())
    sent_tokens.remove(user_response)
