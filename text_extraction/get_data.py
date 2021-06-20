import json
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

# rootdir = '/home/lollipop/PycharmProjects/2017'
# data = []
# counter = 0
# for root, subdirs, files in os.walk(rootdir):
#     for file in files:
#         if file.endswith('.pdf'):
#             try:
#                 pdf_file = open(root + '/' + file, 'rb')
#                 read_pdf = PyPDF4.PdfFileReader(pdf_file)
#                 number_of_pages = read_pdf.getNumPages()
#                 text = ''
#                 for i in range(0, number_of_pages):
#                     page = read_pdf.getPage(i)
#                     text += (page.extractText() + " ")
#
#                 translator = Translator()
#                 lang = translator.detect(text)
#                 if lang.lang != 'en':
#                     text = translator.translate(text).text
#                 data.append(text)
#             except ProtocolError:
#                 pass
#             except PdfReadError:
#                 pass
#             counter += 1
#             print(counter)
#             # try:
#             #     text = '\n'.join(f.readlines())
#             #     data.append(text)
#             # except UnicodeDecodeError:
#             #     pass
# file = open('../files/plain_text.json', 'w+')
# data = json.dumps(data)
# file.write(data)
# file.flush()
# file.close()

#train()

# all_data = json.load(open('../files/data.json'))
# data = json.load(open('../files/plain_text.json'))
# for p in data:
#     all_data.append(('plain_text', p))
# file = open('../files/all_data.json', 'w')
# all_data = json.dumps(all_data)
# file.write(all_data)
# file.flush()
# file.close()
