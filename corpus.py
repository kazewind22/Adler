#!/usr/bin/env python3

from gensim import corpora, models
from six import iteritems
import logging

class Corpus:
    def __init__(self, *args, **kwargs):
        self.cpath = kwargs['corpus_path']
        if 'dictionary_path' in kwargs:
            self.dictionary = corpora.Dictionary.load(kwargs['dictionary_path'])
        else:
            self.dictionary = corpora.Dictionary(line.split() for line in open(self.cpath, errors='ignore'))
    def __iter__(self):
        for line in open(self.cpath):
            yield self.dictionary.doc2bow(line.split())

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    #gossip_corpus = Corpus(corpus_path = '_Article_gossiping_seg.txt')
    #gossip_corpus.dictionary.save('gossip.dictionary')
    #corpora.MmCorpus.serialize('gossip_corpus.mm', gossip_corpus)  # store to disk, for later use
    #tfidf = models.TfidfModel(gossip_corpus)
    #tfidf.save('gossip_model.tfidf')

    hot_gossip_corpus = Corpus(corpus_path = '_hot_Article_gossiping_seg.txt',dictionary_path = 'gossip.dict')
    corpora.MmCorpus.serialize('hot_gossip_corpus.mm', hot_gossip_corpus)  # store to disk, for later use
    tfidf = models.TfidfModel(hot_gossip_corpus)
    tfidf.save('hot_gossip_model.tfidf')

if __name__ == '__main__':
    main()
