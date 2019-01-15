from Discovery.AbstractContent import AbstractContentSource
from Recommendation.ESservice import ESservice

class MediumAdapter(AbstractContentSource):
    def adaptToES(ids, links, titles, descriptions, tags):
        dataList = []
        for j in range(len(titles)):
            jsonDict = {}
            jsonDict['id'] = 'medium_' + ids[j]
            jsonDict['title'] = titles[j]
            jsonDict['description'] = descriptions[j]
            jsonDict['tags'] = tags[j]
            jsonDict['url'] = links[j]
            jsonDict['source'] = 'medium'
            jsonDict['mediaType'] = 'text'

            dataList.append(jsonDict)
            print(jsonDict)

        ESservice.insertSingle(ESservice.getInstance(), dataList)

