import os
import pickle
import re

import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier

clf = SGDClassifier(loss='log', random_state=1, max_iter=1)

stop = stopwords.words('english')


def stream_docs(path):
    with open(path, 'r', encoding='utf-8') as csv:
        next(csv)  # skip the first line
        for line in csv:
            text, label = line[:-3], int(line[-2])
            yield text, label


doc_stream = stream_docs(path='movie_data.csv')


def get_minibatch(doc_stream, size):
    docs, y = [], []
    try:
        for _ in range(size):
            text, label = next(doc_stream)
            docs.append(text)
            y.append(label)
    except StopIteration:
        return None, None
    return docs, y


def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text.lower())
    text = re.sub('[\W]+', ' ', text.lower()) + \
           ' '.join(emoticons).replace('-', '')
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized


vectorizer = HashingVectorizer(decode_error='ignore', n_features=2 ** 21, preprocessor=None, tokenizer=tokenizer)

classes = np.array([0, 1])
for _ in range(45):
    X_train, y_train = get_minibatch(doc_stream, size=1000)
    if not X_train:
        break
    X_train = vectorizer.transform(X_train)
    clf.partial_fit(X_train, y_train, classes=classes)

X_test, y_test = get_minibatch(doc_stream, size=5000)
X_test = vectorizer.transform(X_test)


print('Accuracy: %.2f' % clf.score(X_test, y_test))
print('\n')

# this part is for saving the model into a folder
dest = os.path.join('movie_classifier', 'pkl_objects')
if not os.path.exists(dest):
    os.makedirs(dest)

pickle.dump(stop, open(os.path.join(dest, 'stopwords.pkl'), 'wb'), protocol=4)

pickle.dump(clf, open(os.path.join(dest, 'classifier.plk'), 'wb'), protocol=4)
# testing some text for further reviewing

# label = {0: 'negative', 1: 'positive'}
# example = ['i really liked the acting, but the movie itself slacked in my opinion. Could have been done better']
# X = vectorizer.transform(example)
# print('Prediction: %s\nProbability: %.2f%%' % (label[clf.predict(X)[0]], np.max(clf.predict_proba(X))*100))