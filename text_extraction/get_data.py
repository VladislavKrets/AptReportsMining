import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
import nltk


def train():
    all_data = json.load(open('files/data.json'))
    df = pd.DataFrame(all_data, columns=['language', 'source'])
    df = df.sample(frac=1).reset_index(drop=True)
    X_train, X_test, y_train, y_test = train_test_split(df['source'], df['language'],
                                                        test_size=0.2, random_state=42)
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB())])
    text_clf = text_clf.fit(X_train, y_train)
    predicted = text_clf.predict(X_train)
    print(np.mean(predicted == y_train))
    return text_clf


# rootdir = '/home/lollipop/PycharmProjects/c'
# data = []
# for root, subdirs, files in os.walk(rootdir):
#     for file in files:
#         if file.endswith('.c') or file.endswith('.h'):
#             f = open(root + '/' + file, 'r')
#             try:
#                 text = '\n'.join(f.readlines())
#                 data.append(text)
#             except UnicodeDecodeError:
#                 pass
# file = open('../files/c.json', 'w+')
# data = json.dumps(data)
# file.write(data)
# file.flush()
# file.close()

all_data = json.load(open('../files/assembly.json'))
words = {}
for item in all_data:
    for sent in nltk.sent_tokenize(item):
        for word in nltk.word_tokenize(sent):
            if word not in words:
                words[word] = 1
            else:
                words[word] += 1
df = pd.DataFrame(words.items(), columns=['word', 'count'])
df = df.sort_values(by=['count'], ascending=False)
df = df.head(1000)
df.to_csv(path_or_buf='../files/assembly.csv', index=False)
print(df)
