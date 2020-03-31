from gensim.models import KeyedVectors

model_path = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\GoogleNews-vectors-negative300.bin"
model = KeyedVectors.load_word2vec_format(model_path, binary=True,limit=1000000)
model.save("word2vec.model")