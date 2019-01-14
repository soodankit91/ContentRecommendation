from gensim.models.keyedvectors import KeyedVectors

model = KeyedVectors.load_word2vec_format('../resources/GoogleNews-vectors-negative300.bin', binary=True)

def vectorSimilarity(list1, list2, threshold=0.3):
    sim = 0.0
    for word1 in list1:
        for word2 in list2:
            try:
                simScore = model.similarity(word1,word2)
            except:
                continue 
            if simScore > threshold:
                sim += simScore
    
    return sim

def getSimilarity(word1, word2):
    return model.similarity(word1,word2)