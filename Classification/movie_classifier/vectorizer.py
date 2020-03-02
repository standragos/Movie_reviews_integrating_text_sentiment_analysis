import os
import pickle
import re
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer

current_directory = os.path.dirname(__file__)
stop = pickle.load(open(os.path.join(current_directory, 'pkl_objects', 'stopwords.pkl'), 'rb'))


def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text.lower())
    text = re.sub('[\W]+', ' ', text.lower()) + \
           ' '.join(emoticons).replace('-', '')
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized


vect = HashingVectorizer(decode_error='ignore', n_features=2**21, preprocessor=None, tokenizer=tokenizer)

clf = pickle.load(open(os.path.join(current_directory, 'pkl_objects', 'classifier.plk'), 'rb'))

label = {0: 'negative', 1: 'positive'}
example = ['this movie was bad, the acting of the actors was not so good, everything was terrible about this movie'
           'i wont watch this movie again']
X = vect.transform(example)
print('Prediction: %s\nProbability: %.2f%%' % (label[clf.predict(X)[0]], np.max(clf.predict_proba(X))*100))
