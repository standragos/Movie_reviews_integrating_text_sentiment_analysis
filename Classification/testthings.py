import pandas as pd
import re
from nltk.corpus import stopwords

stop = stopwords.words('english')

def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text.lower())
    text = re.sub('[\W]+', ' ', text.lower()) + \
           ' '.join(emoticons).replace('-', '')
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized

print(tokenizer(' <><>[] a >>??? running likes running and runs a lot'))

a = '<dada><xxxa>[] a >>??? running likes running <sadasdas> and runs a lot'
a = re.sub('<.*?>', '', a)
print(a)