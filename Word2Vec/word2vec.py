#wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ja.300.vec.gz
import gensim
model = gensim.models.KeyedVectors.load_word2vec_format('cc.ja.300.vec.gz', binary=False) # gensim形式のモデルをロードします
print("ダウンロード完了")
kwds=model.most_similar(positive=['猫'])

