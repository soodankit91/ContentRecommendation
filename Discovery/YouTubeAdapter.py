from Discovery.AbstractContent import AbstractContentSource
from Recommendation.ESservice import ESservice

class YouTubeAdapter(AbstractContentSource):
    def adaptToES(ids, links, titles, descriptions, tags):
        dataList = []
        for j in range(len(titles)):
            jsonDict = {}
            jsonDict['id'] = 'youtube_' + ids[j]
            jsonDict['title'] = titles[j]
            jsonDict['description'] = descriptions[j]
            jsonDict['tags'] = None
            jsonDict['url'] = links[j]
            jsonDict['source'] = 'YouTube'
            jsonDict['mediaType'] = 'video'

            dataList.append(jsonDict)
            print(jsonDict)

        ESservice.insertSingle(ESservice.getInstance(), dataList)

