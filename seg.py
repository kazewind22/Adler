#!/usr/bin/env python3

import csv
import jieba

jieba.set_dictionary('dict/dict.txt.big')
jieba.load_userdict('dict/dict.user')

with open('Article_100_2.csv') as Article:
    reader = csv.reader(Article)
    for row in reader:
        print("Input:\n", row[5])

        out_for_search = jieba.cut_for_search(row[5])
        print("Output:\n", "/ ".join(out_for_search))

        print("-"*60)


