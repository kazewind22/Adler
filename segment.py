#!/usr/bin/env python3

import sys
import csv
import logging
import jieba

jieba.set_dictionary('jieba_dict/dict.txt.big')
jieba.load_userdict('jieba_dict/dict.user')

# load stopwords set
stopwordset = set()
with open('jieba_dict/stopwords.txt','r',encoding='utf-8') as sw:
    for line in sw:
        stopwordset.add(line.strip('\n'))
sw.close()

def segment_zh(doc):
    words = jieba.cut(doc.strip(), cut_all=False)
    output = []
    for word in words:
        if word not in stopwordset:
            output.append(word)
    return output

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    with open(sys.argv[1]) as Article:
        Article.readline() #dismiss column titles
        reader = csv.reader(Article)
        output = open(sys.argv[1][:-4]+'_seg.txt','w')
        texts_num = 0
        for row in reader:
            seg = segment_zh(row[5].strip()) #segment articles
            for word in seg:
                output.write(word +' ')
            output.write('\n')
            texts_num += 1
            if texts_num % 10000 == 0:
                logging.info("Segmented %d articles" % texts_num)

if __name__ == '__main__':
    main()
