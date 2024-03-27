import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import time

def read_from(textfile):
    word, sign = [], []
    for line in open(textfile):
        label, words = line.strip().split("\t")
        sign.append(1 if label == "+" else -1)
        word.append(' '.join(words.split()))
    return word, sign

def train(trainfile, devfile):
    t = time.time()
    word_train, sign_train = read_from(trainfile)
    word_dev, sign_dev = read_from(devfile)

    vectorizer = CountVectorizer(min_df=2, token_pattern=r"\b\w{2,}\b")
    word_train = vectorizer.fit_transform(word_train)
    word_dev_Bi = vectorizer.transform(word_dev)
    
    # Increase the max_iter parameter
    model = LogisticRegression(max_iter=1000)

    model.fit(word_train, sign_train)
    sign_pred = model.predict(word_dev_Bi)
    accuracy = accuracy_score(sign_dev, sign_pred) * 100
   # print(f"Accuracy on the development set: {accuracy:.2f}%")
    print(100 - accuracy)

    print("time: %.1f secs" % (time.time() - t))
if __name__ == "__main__":
     train(sys.argv[1], sys.argv[2])
