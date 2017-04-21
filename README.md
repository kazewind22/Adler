Enviroment: Python3
Libraries used: jieba, gensim, opencc

1. Download all Articles as csv format.
$ ls Article.csv

2. Extract articles from board Gossiping
$ python3 extract_gossip.py Article.csv
$ ls Article_gossip.csv

	2-1. To test similarity, you need to extract hot articles at the same time
	$ python3 extract_gossip.py Article.csv --hot
	$ ls Article_gossip.csv Article_gossip_hot.csv

3. Segment Gossiping articles by jieba
$ python3 segment.py Article_gossip.csv
$ ls Article_gossip_seg.txt

	3-1. To test similarity, you need to segment the hot articles
	$ python3 segment.py Article_gossip_hot.csv
	$ ls Article_gossip_hot_seg.txt

4. Preprocess corpus
$ python3 corpus.py --init
$ python3 corpus.py --hot

	4-1. Use --hot argument to preprocess hot gossip corpus
	$ python3 corpus.py --hot

	4-2. Use --add argument to update the corpus and dictionary
	[Demo]
	$ python3 extract_HatePolitics.py Article.csv
	$ python3 segment Article_HatePolitics.csv
	$ python3 corpus.py --add Article_HatePolitics

5. Train word2vec model
$ opencc -i _Article__gossip_seg.txt -o Article_gossip_seg_zhtw.txt -c s2tw.json
$ python3 train.py

6. [Demo]
$ python3 similarity.py
