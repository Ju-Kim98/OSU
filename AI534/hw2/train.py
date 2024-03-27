#!/usr/bin/env python3

from __future__ import division # no need for python3, but just in case used w/ python2

import sys
import time
from svector import svector

def read_from(textfile):
    for line in open(textfile):
        label, words = line.strip().split("\t")
        yield (1 if label=="+" else -1, words.split())

def make_vector(words):
    v = svector()
    for word in words:
        v[word] += 1
        v['<bias>'] = 1     # Add the bias term (constant feature)
 
    return v
            
def test(dev, model):
    tot, err = 0, 0
    mistakes = []
    for i, (label, words) in enumerate(read_from(dev), 1):  # note 1...|D|
        v = make_vector(words, bias=True)
        margin = label * (model.dot(v))
        if margin <= 0:
            err += 1
            mistakes.append((margin, label, words))
    return err / i, mistakes  # i is |D| now

def train(train, dev, epochs=5):
    t = time.time()
    best_err = 1.
    model = svector()
    for it in range(1, epochs + 1):
        updates = 0
        for i, (label, words) in enumerate(read_from(train), 1):  # label is +1 or -1
            sent = make_vector(words)
            if label * (model.dot(sent)) <= 0:
                updates += 1
                model += label * sent
        dev_err, _ = test(dev, model)
        best_err = min(best_err, dev_err)
        print("epoch %d, update %.1f%%, dev %.1f%%" % (it, updates / i * 100, dev_err * 100))
    print("best dev err %.1f%%, |w|=%d, time: %.1f secs" % (best_err * 100, len(model), time.time() - t))
    return model

def get_top_features(model, top_n=20):
    items = list(model.items())
    items.sort(key=lambda x: abs(x[1]), reverse=True)
    top_positive = [item for item in items if item[1] > 0][:top_n]
    top_negative = [item for item in items if item[1] < 0][:top_n]
    return top_positive, top_negative

def train_ave(train, dev, epochs=5):
    t = time.time()
    best_err = 1.
    model = svector()
    model_ave = svector()
    c = 0
    for it in range(1, epochs + 1):
        updates = 0
        for i, (label, words) in enumerate(read_from(train), 1):  # label is +1 or -1
            sent = make_vector(words)
            if label * (model.dot(sent)) <= 0:
                updates += 1
                model += label * sent
                model_ave += c * label * sent
            c += 1
        model_a = c * model - model_ave
        dev_err, mistakes = test(dev, model_a)
        best_err = min(best_err, dev_err)
        print("epoch %d, update %.1f%%, dev %.1f%%" % (it, updates / i * 100, dev_err * 100))
    print("best dev err %.1f%%, |w|=%d, time: %.1f secs" % (best_err * 100, len(model), time.time() - t))

    top_positive_features, top_negative_features = get_top_features(model_a)
    print("\nTop 20 Positive Features:")
    for feature, weight in top_positive_features:
        print(f"{feature}: {weight:.4f}")

    print("\nTop 20 Negative Features:")
    for feature, weight in top_negative_features:
        print(f"{feature}: {weight:.4f}")

    # Sort mistakes by confidence
    mistakes.sort(key=lambda x: x[0])
    # Get the top 5 negative examples that the model believes to be positive
    false_positives = [mistake for mistake in mistakes if mistake[1] == -1][:5]
    # Get the top 5 positive examples that the model believes to be negative
    false_negatives = [mistake for mistake in mistakes if mistake[1] == 1][-5:]

    print("\nTop 5 Negative Examples that model believes to be Positive:")
    for margin, label, words in false_positives:
        print(f"{' '.join(words)}")

    print("\nTop 5 Positive Examples that model believes to be Negative:")
    for margin, label, words in false_negatives:
        print(f"{' '.join(words)}")

    return model_a
    
#PART3
from __future__ import division
from collections import defaultdict
import sys
import time
from svector import svector

def read_data(textfile):
    data = []
    for line in open(textfile):
        label, words = line.strip().split("\t")
        data.append((1 if label == "+" else -1, words.split()))
    return data

def count_words(data):
    word_counts = defaultdict(int)
    for _, words in data:
        for word in words:
            word_counts[word] += 1
    return word_counts

def make_vector1(words, word_counts, bias=True):
    v = svector()
    for word in words:
        if word_counts[word] > 2:
            v[word] += 1
    if bias:
        v['<bias>'] = 1
    return v

def test1(dev, model, word_counts):
    tot, err = 0, 0
    for i, (label, words) in enumerate(read_data(dev), 1): # note 1...|D|
        v = make_vector1(words, word_counts, bias = True)
        err += label * (model.dot(make_vector1(words, word_counts))) <= 0
    return err/i  # i is |D| now


def train_ave(train, dev, epochs=5):
    t = time.time()
    best_err = 1.
    model = svector()
    model_ave = svector()
    c = 0
    train_data = read_data(train)
    dev_data = read_data(dev)
    word_counts = count_words(train_data)

    for it in range(1, epochs + 1):
        updates = 0
        for i, (label, words) in enumerate(read_data(train), 1):  # label is +1 or -1
            sent = make_vector1(words, word_counts)
            if label * (model.dot(sent)) <= 0:
                updates += 1
                model += label * sent
                model_ave += c * label * sent
            c += 1
        model_a = c * model - model_ave
        dev_err = test1(dev, model_a, word_counts)
        best_err = min(best_err, dev_err)
        print("epoch %d, update %.1f%%, dev %.1f%%" % (it, updates / i * 100, dev_err * 100))
    print("best dev err %.1f%%, |w|=%d, time: %.1f secs" % (best_err * 100, len(model), time.time() - t))

#PART4
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
    print(f"Accuracy on the development set: {accuracy:.2f}%")
    print("time: %.1f secs" % (time.time() - t))
if __name__ == "__main__":
     train(sys.argv[1], sys.argv[2])
     
     
#PART5


#if __name__ == "__main__":
#    train(sys.argv[1], sys.argv[2], 10)
