import requests
from Discovery.YouTubeAdapter import YouTubeAdapter
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from operator import itemgetter

class YouTube:

    API_KEY = ''
    keywords = []

    def __init__(self, API_KEY, keywords):
        self.API_KEY = API_KEY
        self.keywords = keywords

    def requestVideos(self):
        videos = []
        links = []
        titles = []
        descriptions = []
        linkTags = []
        ids = []

        parameters = {'key': self.API_KEY, 'q': self.keywords, 'maxResults': '50', 'order': 'relevance', 'part': 'snippet',
                      'type': 'video', 'videoCaption': 'any', 'safeSearch': 'moderate'}
        response = (requests.get('https://www.googleapis.com/youtube/v3/search?', params=parameters).json())
        print(response)
        videos.append(response['items'])
        print('calling page... ', parameters.get('page'))
        print ((videos))
        print("printed")

        for video in videos :
            print ("video = ",video)

            ids.append(video[0]['id']['videoId'])
            titles.append(video[0]['snippet']['title'])
            descriptions.append(video[0]['snippet']['description'])
            links.append('https://www.youtube.com/watch?v='+video[0]['id']['videoId'])

        YouTubeAdapter.adaptToES(ids,links,titles,descriptions,linkTags)


if __name__ == '__main__':
    YouTube('AIzaSyAIlV0RK3GsPRoJReMflOMPCLeU6ilgW8E', ['tourism', 'India', 'winters']).requestVideos()