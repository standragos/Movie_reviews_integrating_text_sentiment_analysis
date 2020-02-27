import os
import tarfile
from six.moves import urllib

DATA_DOWNLOAD_URL = "http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
DATA_PATH = os.path.join("data")


def fetch__data(data_download_url=DATA_DOWNLOAD_URL, data_path=DATA_PATH):
    if not os.path.isdir(data_path):
        os.makedirs(data_path)
    tgz_path = os.path.join(data_path, "aclImdb_v1.tar.gz")
    urllib.request.urlretrieve(data_download_url, tgz_path)
    reviews_tgz = tarfile.open(tgz_path)
    reviews_tgz.extractall(path=data_path)
    reviews_tgz.close()


fetch__data(DATA_DOWNLOAD_URL, DATA_PATH)