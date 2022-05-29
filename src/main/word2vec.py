# wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ja.300.vec.gz
import gensim
import torch
import itertools
from einops import rearrange
import numpy as np


class Word2Vec:
    '''
    初期化に5分ほどかかると思われます。
    使う関数はtopicsです。
    '''

    def __init__(self):
        self.model = gensim.models.KeyedVectors.load_word2vec_format(
            'cc.ja.300.vec.gz', binary=False)

    def subject_step(self,p,n,topn):
        words=[]
        try:
            lis_tup=self.model.most_similar(positive=p,negative=n,topn=topn)
            for tup in lis_tup:
                words.append(tup[0])
        except KeyError:
            p=list(p)
            for i in range(len(p)):
                if not p[i] in self.model:
                    p[i]='趣味'
            lis_tup=self.model.most_similar(positive=p,negative=n,topn=topn)
            for tup in lis_tup:
                words.append(tup[0])
        return words

    def subject_loop(self, p, n, topn, steps=1):
        for i in range(steps):
            p = self.subject_step(p, n, topn)
        return p

    def p_pairs(self, p):
        return list(itertools.combinations(p, 2))

    def clean_up(self, words):
        topic = []
        for word in words:
            if (word in topic):
                continue
            topic.append(word)
        return topic

    def topics(self, p, n=None, topn=7):
        """
        p: 単語のリスト（日本語）を入力

        n: 単語ベクトルのマイナスしたいもの。defaultはNone
        topn: 数が大きい方が出力単語数が増える。defaultは7

        出力:類似単語のリスト
        """
        pairs = self.p_pairs(p)
        topics = []
        for pair in pairs:
            topics.append(self.subject_loop(pair, n, topn))
        return self.clean_up(rearrange(np.array(topics), 'pairs topn -> (pairs topn)'))
