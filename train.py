#!/usr/bin/env python3

from gensim.models import word2vec
import logging

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    sentences = word2vec.Text8Corpus("Article_gossip_seg_zhtw.txt")
    model = word2vec.Word2Vec(sentences, size=500)

    #save model
    model.save("med500.model_gossiping.bin")

if __name__ == "__main__":
    main()
