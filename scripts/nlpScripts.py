from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np


def removeNoise(articles):
    punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~≥≤"""

    for article in articles:
        nopunc = [char for char in article.abstract if char not in punctuation]
        nopunc = ''.join(nopunc)

        nonumbers = [word for word in nopunc if not (word.isdigit())]
        nonumbers = ''.join(nonumbers)

        article.chAbstract = nonumbers
        article.words =  [word for word in nonumbers.split() if word.lower() not in stopwords.words('english')]


def stem(articles):
    snow_stemmer = SnowballStemmer(language='english')
    
    for article in articles:
        for i, w in enumerate(article.words):
            article.words[i] = snow_stemmer.stem(w)


def lemmatize(articles):
    lemmatizer = WordNetLemmatizer()

    for article in articles:
        for i, w in enumerate(article.words):
            article.words[i] = lemmatizer.lemmatize(w)

        words = article.chAbstract.split(' ')
        for i, word in enumerate(words):
            words[i] = lemmatizer.lemmatize(word)

        article.chAbstract = ' '.join(words)


def findSynonyms(words):
    synonyms = set()
    for word in words:
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.add(l.name())
    return synonyms


def abstractWeights(articles, words):
    chAbstracts = [article.chAbstract for article in articles]
   
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer_vectors = tfidf_vectorizer.fit_transform(chAbstracts)
    feature_names = tfidf_vectorizer.get_feature_names_out()

    words = words.intersection(feature_names)
    weights = np.zeros(len(articles))

    for word in words:
        weights += tfidf_vectorizer_vectors[:, feature_names == word].toarray().flatten()

    for article, weight in zip(articles, weights):
        article.weight += weight


def getSortedArticles(articles):
    return sorted(articles, key=lambda a: a.weight, reverse = True)[:10]
