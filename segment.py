#!/usr/bin/env python3

import csv
import jieba
import logging

jieba.set_dictionary('jieba_dict/dict.txt.big')
jieba.load_userdict('jieba_dict/dict.user')

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# load stopwords set
stopwordset = set()
with open('jieba_dict/stopwords.txt','r',encoding='utf-8') as sw:
    for line in sw:
        stopwordset.add(line.strip('\n'))

def segment_zh(doc):
    words = jieba.cut(doc.strip(), cut_all=False)
    output = []
    for word in words:
        if word not in stopwordset:
            output.append(word)
    return output

def main():

    with open('Article_gossiping_100.csv') as Article:
        reader = csv.reader(Article)
        output = open('gossiping_seg_100.txt','w')
        texts_num = 0
        for row in reader:
            seg = segment_zh(row[5])
            for word in seg:
                output.write(word +' ')
            texts_num += 1
            if texts_num % 10 == 0:
                print("Already segmented %d articles" % texts_num)

if __name__ == '__main__':
    main()
