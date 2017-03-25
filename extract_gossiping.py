import sys
import logging
import re

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    with open(sys.argv[1]) as Article:
        output = open(sys.argv[1][:-4]+'_gossiping.csv','w')

        texts_num = 0
        output.write(Article.readline())
        for line in Article:
            if '"Gossiping"' in line:
                output.write(re.sub('[\s+]','',line)+'\n')
            texts_num += 1
            if texts_num % 10000 == 0:
                logging.info("Already extracted %d articles" % texts_num)

if __name__ == '__main__':
    main()
