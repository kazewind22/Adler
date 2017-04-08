#!/usr/bin/env python3

import sys
import csv
import logging
import re

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    try:
        if sys.argv[2] == '--hot':
            flag = True
    except Exception as e:
        flag = False

    with open(sys.argv[1]) as Article:
        texts_num = 0
        reader = csv.reader(x.replace('\0', '') for x in Article)
        header = Article.readline()
        output = open(sys.argv[1][:-4]+'_gossip.csv','w')
        output.write(header) # header line
        writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        if flag:
            output_hot = open(sys.argv[1][:-4]+'_gossip_hot.csv','w')
            output_hot.write(header) # header line
            writer_hot = csv.writer(output_hot, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        for row in reader:
            # `board` = 'Gossiping'
            if 'Gossiping' == row[8]:
                row[5] = re.sub(r'http:\\*/\\*/.*?\s', '', row[5], flags=re.MULTILINE)
                row[5] = re.sub(r'https:\\*/\\*/.*?\s', '', row[5], flags=re.MULTILINE)
                row[5] = re.sub('[\s+]','',row[5])
                writer.writerow(row)
                if flag:
                    if int(row[1]) > 100:
                        writer_hot.writerow(row)

            texts_num += 1
            if texts_num % 10000 == 0:
                logging.info("Processed %d articles." % texts_num)

if __name__ == '__main__':
    main()
