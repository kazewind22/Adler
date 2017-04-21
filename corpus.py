#!/usr/bin/env python3

from gensim import corpora, models
from six import iteritems
import logging
import argparse
import os.path

def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action='store_true',default = False)
    parser.add_argument('--hot', action='store_true', default = False)
    parser.add_argument('--add')
    return vars(parser.parse_args())

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
    args = parser_args()

    if args['init']:
        gossip_corpus = Corpus(corpus_path = 'Article_gossip_seg.txt')
        gossip_corpus.dictionary.save('gossip.dict')
        corpora.MmCorpus.serialize('gossip_corpus.mm', gossip_corpus)  # store to disk, for later use
        tfidf = models.TfidfModel(gossip_corpus)
        tfidf.save('gossip_model.tfidf')

    if args['hot']:
        if os.path.exists('gossip.dict')==False:
            print("You need to initialize first:\n$ python3 corpus.py --init")
            return
        hot_gossip_corpus = Corpus(corpus_path = 'Article_gossip_hot_seg.txt',dictionary_path = 'gossip.dict')
        corpora.MmCorpus.serialize('hot_gossip_corpus.mm', hot_gossip_corpus)  # store to disk, for later use
        tfidf = models.TfidfModel(hot_gossip_corpus)
        tfidf.save('hot_gossip_model.tfidf')

    if args['add']:
        if os.path.exists('gossip.dict')==False:
            print("You need to initialize first:\n$ python3 corpus.py --init")
            return

        dictionary = corpora.Dictionary.load('gossip.dict')
        dictionary.add_documents(line.split() for line in open(args['add']+'_seg.txt', errors='ignore'))
        dictionary.save('gossip.dict')

        with open('Update_Article_gossip_seg.txt', 'w') as f:
            seg_origin = open('Article_gossip_seg.txt', 'r')
            seg_new = open(args['add']+'_seg.txt', 'r')
            f.write(seg_origin.read())
            f.write(seg_new.read())
            seg_origin.close()
            seg_new.close()

        with open('Update_Article_gossip.csv', 'w') as f:
            csv_origin = open('Article_gossip.csv', 'r')
            csv_new = open(args['add']+'.csv', 'r')
            f.write(csv_origin.read())
            csv_new.readline() #skip header
            f.write(csv_new.read())
            csv_origin.close()
            csv_new.close()

        new_gossip_corpus = Corpus(corpus_path = 'Update_Article_gossip_seg.txt',dictionary_path = 'gossip.dict')
        corpora.MmCorpus.serialize('update_gossip_corpus.mm', new_gossip_corpus)  # store to disk, for later use
        tfidf = models.TfidfModel(new_gossip_corpus)
        tfidf.save('update_gossip_model.tfidf')

if __name__ == '__main__':
    main()
