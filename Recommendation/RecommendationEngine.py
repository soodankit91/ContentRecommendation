from Recommendation.ESservice import ESservice
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import Recommendation.wordVector as wV
import operator


class RecommendationEngine:

    lemmatizer = WordNetLemmatizer()
    stop = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r'\w+')
    available_MediaTypes = ['text','images','videos']
    available_Sources_MediaTypes = {'text':['WordPress','Medium'],'image':['Unsplash'],'video':['YouTube']}
    mediaList = []
    sourceList = []

    def __init__(self, mediaList, sourceList):
        self.mediaList = mediaList
        self.sourceList = sourceList

    def searchRecommendations(self, searchWords, mediaTypes = None, sources = []):

        es = ESservice.getConnection(ESservice())
        articlesList = []

        # select all media types if no media type is specified
        if mediaTypes is None:
            mediaTypes = ['text','image','video']
        #if no source is specified, select all sources corresponding to the selected media types
        if not sources:
            for media in mediaTypes:
                sources.extend(self.available_Sources_MediaTypes[media])
        #make sure that only the sources corressponding to the selected media types get chosen
        else:
            for source in sources:
                for key, value in self.available_Sources_MediaTypes.items():
                    if key not in mediaTypes:
                        if source in value:
                            sources.remove(source)

        for word in searchWords:
            searchQuery = {
                'query': {
                    'bool': {
                        'must': {
                            'multi_match': {
                                "query": word,
                                "fields": ["title", "tags", "description"]
                            }
                        },
                        'filter' : {
                            'terms' :   {
                                "sources":sources
                             },
                            'terms': {
                                "mediaType": mediaTypes
                            }
                        }
                    }
                }
            }

            response= es.search(index='discovery', doc_type='media',body=searchQuery)
            articlesList.extend(response['hits']['hits'])

        return articlesList


    def getRelevance(self, esJson, keywords):
        description = []
        if esJson['_source'] is not None:
            wordList = []
            if ('title' in esJson['_source']):
                wordList.extend(self.tokenizer.tokenize(esJson['_source']['title']))
            if ('description' in esJson['_source']):
                wordList.extend(self.tokenizer.tokenize(esJson['_source']['description']))
            if ('tags' in esJson['_source'] and esJson['_source']['tags'] is not None):
                wordList.extend(esJson['_source']['tags'])

            for word in wordList:
                if word not in self.stop:
                    word = self.lemmatizer.lemmatize(word)
                    description.append(word)

        description = list(set(description))
        keywords = [self.lemmatizer.lemmatize(word) for word in keywords]

        similarity_score = wV.vectorSimilarity(description, keywords)

        return (esJson['_source']['url'], similarity_score)

    def getRecommendations(self, searchWords):
        articlesList = self.searchRecommendations(searchWords,self.mediaList , self.sourceList)
        recommendations = list()
        for article in articlesList:
            recommendations.append(self.getRelevance(article,searchWords))

        recommendations.sort(key=operator.itemgetter(1), reverse=True)

        return recommendations


if __name__ == '__main__':
    queryList = ['tourism','India','winter','food']
    print ("recommended list = ", RecommendationEngine(['image', 'video'], ['YouTube', 'Unsplash']).getRecommendations(queryList))