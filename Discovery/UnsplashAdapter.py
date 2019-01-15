from Discovery.AbstractContent import AbstractContentSource
from Recommendation.ESservice import ESservice

class UnsplashAdapter(AbstractContentSource):
    def adaptToES(ids, links, titles, descriptions, tags):
        dataList = []
        for j in range(len(ids)):
            jsonDict = {}
            jsonDict['id'] = 'unsplash_' + ids[j]
            jsonDict['description'] = descriptions[j]
            jsonDict['tags'] = None
            jsonDict['url'] = links[j]
            jsonDict['source'] = 'unsplash'
            jsonDict['mediaType'] = 'image'

            dataList.append(jsonDict)
        ESservice.insertSingle(ESservice.getInstance(), dataList)

