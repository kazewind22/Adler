#!/usr/bin/env python3

import logging
import csv
import sys
from gensim import corpora, models, similarities
from segment import segment_zh

def query_merge(_q1, _q2):
    query = []
    q1 = _q1.copy()
    q2 = _q2.copy()
    q1.append((sys.maxsize,0))
    q2.append((sys.maxsize,0))
    i = 0
    j = 0
    while i + j < len(q1)+len(q2):
        if q1[i][0] < q2[j][0]:
            query.append(q1[i])
            i += 1
        elif q1[i][0] > q2[j][0]:
            query.append(q2[j])
            j += 1
        else:
            query.append((q1[i][0], q1[i][1]+q2[j][1]))
            i += 1
            j += 1
    query.pop()
    return query

def query_scale(q, n):
    return [(p[0],p[1]*n) for p in q]

def main():
    #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    corpus = corpora.MmCorpus('hot_gossip_corpus.mm')
    dictionary = corpora.Dictionary.load('gossip.dict')
    tfidf = models.TfidfModel.load('hot_gossip_model.tfidf')
    index = similarities.Similarity('hot_gossip_tfidf.index', tfidf[corpus], corpus.num_terms, num_best = 10)
    #index.save('hot_gossip_tfidf.index')
    #index = similarities.Similarity.load('hot_gossip_tfidf.index')
    model = models.word2vec.Word2Vec.load('med500.model_gossiping.bin')

    dict_id2title = {}
    with open('_hot_Article_gossiping.csv') as Article:
        Article.readline() #dismiss column titles
        reader = csv.reader(Article)
        count = 0
        for row in reader:
            dict_id2title[count] = (row[3], row[5].strip())
            count += 1

    while True:
        try:
            print('='*110)
            print("請輸入關鍵字：", end='')
            query = input()
            #query_split = list(query)+[query[i:i+2] for i in range(len(query)-1)]
            query_split = segment_zh(query)
            print("關鍵字斷詞：")
            w2v = []
            for word in query_split:
                res = model.most_similar(word,topn = 5)
                w2v = w2v + [item[0] for item in res]
                print(word+': '+ ' / '.join(item[0] for item in res))

            query_bow = dictionary.doc2bow(query_split)
            query_tfidf = tfidf[query_bow]
            #print(query_tfidf)
            sims = index[query_tfidf]

            w2v_bow = dictionary.doc2bow(w2v)
            w2v_tfidf = tfidf[w2v_bow]
            #print(w2v_tfidf)
            #print(query_merge(query_tfidf, query_scale(w2v_tfidf, 0.2)))
            w2v_sims = index[query_merge(query_tfidf, query_scale(w2v_tfidf, 0.2))]

            for i in range(len(sims)):
                #print('No.'+str(i)+', '+str(sims[i])+', '+dict_id2title[sims[i][0]][0])
                print('No.'+str(i)+', '+dict_id2title[sims[i][0]][0])
            print(' --'*35)

            for i in range(len(w2v_sims)):
                #print('No.'+str(i)+', '+str(w2v_sims[i])+', '+dict_id2title[w2v_sims[i][0]][0])
                print('No.'+str(i)+', '+dict_id2title[w2v_sims[i][0]][0])
            print(' --'*35)

            print("Select an article: ", end='')
            option = int(input())
            article = dict_id2title[sims[option][0]]
            print(article[0])
            print(article[1]+'\n')
            print("Articles you may want to know:")
            rel_bow = dictionary.doc2bow(segment_zh(article[1]))
            rel_tfidf = tfidf[rel_bow]
            rel_sims = index[rel_tfidf]
            for i in range(min(5,len(rel_sims))):
                #print('No.'+str(i)+', '+str(rel_sims[i])+', '+dict_id2title[rel_sims[i][0]][0])
                print('No.'+str(i)+', '+dict_id2title[rel_sims[i][0]][0])


            #for word in query_split:
            #    res = model.most_similar(word,topn = 10)
            #    for item in res:
            #        print(item[0]+","+str(item[1]))
        except Exception as e:
            print(repr(e))

if __name__ == '__main__':
    main()
