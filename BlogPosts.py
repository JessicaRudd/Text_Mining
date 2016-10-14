# coding=utf-8
import numpy
import pandas as pd
import nltk
import re
import os
import codecs

import time
from sklearn import feature_extraction
import mpld3
import io
import json


def save_json(filename, data):
    # type: (object, object) -> object
    with io.open('{0}.json'.format(filename),
                 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False)))


def load_json(filename):
    with io.open('{0}.json'.format(filename),
                 encoding='utf-8') as f:
        return json.load(f)

import feedparser
from bs4 import BeautifulSoup

FEED_URL = 'http://feeds.feedburner.com/oreilly/radar/atom'

def cleanHtml(html):
    soup = BeautifulSoup(html, "lxml")
    return soup.get_text()

fp = feedparser.parse(FEED_URL)

print "Fetched %s entries from '%s'" % (len(fp.entries[0].title), fp.feed.title)

blog_posts = []
for e in fp.entries:
    blog_posts.append({'title': e.title, 'content'
    : cleanHtml(e.content[0].value), 'link': e.links[0].href})
print blog_posts[0]

save_json('blog', blog_posts)

# Download nltk packages used in this example
nltk.download('stopwords')

stop_words = nltk.corpus.stopwords.words('english') + [
    '.',
    ',',
    '--',
    '\'s',
    '?',
    ')',
    '(',
    ':',
    '\'',
    '\'re',
    '"',
    '-',
    '}',
    '{',
    u'—',
    ]

blog_data = load_json('blog')

for post in blog_data:
    sentences = nltk.tokenize.sent_tokenize(post['content'])

    words = [w.lower() for sentence in sentences for w in
             nltk.tokenize.word_tokenize(sentence)]
    fdist = nltk.FreqDist(words)

    # Basic stats

    num_words = sum([i[1] for i in fdist.items()])
    num_unique_words = len(fdist.keys())

    # Hapaxes are words that appear only once

    num_hapaxes = len(fdist.hapaxes())

    top_10_words_sans_stop_words = [w for w in fdist.items() if w[0]
                                    not in stop_words][:10]

    print post['title']
    print '\tNum Sentences:'.ljust(25), len(sentences)
    print '\tNum Words:'.ljust(25), num_words
    print '\tNum Unique Words:'.ljust(25), num_unique_words
    print '\tNum Hapaxes:'.ljust(25), num_hapaxes
    print '\tTop 10 Most Frequent Words (sans stop words):\n\t\t', \
            '\n\t\t'.join(['%s (%s)'
            % (w[0], w[1]) for w in top_10_words_sans_stop_words])
    print

from sklearn.feature_extraction.text import TfidfVectorizer
vect = TfidfVectorizer(min_df=1)
tfidf = vect.fit_transform(sentences)

print(tfidf)

cosine=(tfidf * tfidf.T).A
print cosine

from nltk.cluster import KMeansClusterer, euclidean_distance
#import nltk.stem
#stemmer_func = nltk.stem.snowball.SnowballStemmer("english").stem
#stopwords = set(nltk.corpus.stopwords.words('english'))

#def normalize_word(word):
#    return stemmer_func(word.lower())

#def get_words(blogs):
 #   words = set()
  #  for post in sentences:
   #     for word in post.split():
    #        words.add(normalize_word(word))
    #return list(words)

def vectorspaced(post):
    #post_components = [normalize_word(word) for word in post.split()]
    return numpy.array([
        word in words and not word in stop_words
        for word in words], numpy.short)

#words = get_words(sentences)

cluster = KMeansClusterer(7, euclidean_distance)
cluster.cluster([vectorspaced(post) for post in blog_data if post])
classified_examples = [cluster.classify(vectorspaced(post)) for post in blog_data]

for cluster_id, post in sorted(zip(classified_examples, blog_data)):
    print cluster_id, post