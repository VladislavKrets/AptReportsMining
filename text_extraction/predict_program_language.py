import json
import os

import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import numpy as np
import joblib


def train():
    all_data = json.load(open('files/all_data.json'))
    df = pd.DataFrame(all_data, columns=['language', 'source'])
    df = df.sample(frac=1).reset_index(drop=True)
    X_train, X_test, y_train, y_test = train_test_split(df['source'], df['language'],
                                                        test_size=0.2, random_state=42)
    text_clf = Pipeline([('tfidf', TfidfVectorizer()),
                         ('sgd_clf', SGDClassifier(random_state=42))])
    text_clf = text_clf.fit(X_train, y_train)
    predicted = text_clf.predict(X_test)
    print(np.mean(predicted == y_test))
    joblib.dump(text_clf, 'files/model.pkl', compress=1)
    return text_clf


def get_model():
    text_clf = joblib.load(open('files/model.pkl', 'rb'))
    return text_clf


def get_languages(images_text):
    text_clf = get_model()
    return text_clf.predict(images_text)


# rootdir = '/home/lollipop/PycharmProjects/python-fire'
# data = []
# counter = 0
# for root, subdirs, files in os.walk(rootdir):
#     for file in files:
#         if file.endswith('.py'):
#             f = open(root + '/' + file, 'r')
#             try:
#                 text = '\n'.join(f.readlines())
#                 data.append(text)
#             except UnicodeDecodeError:
#                 pass
# file = open('../files/python.json', 'w+')
# print(len(data))
# data = json.dumps(data)
# file.write(data)
# file.flush()
# file.close()

# train()

# all_data = json.load(open('../files/all_data.json'))
# data = json.load(open('../files/python.json'))
# for p in data:
#     all_data.append(('python', p))
# file = open('../files/all_data.json', 'w')
# all_data = json.dumps(all_data)
# file.write(all_data)
# file.flush()
# file.close()
