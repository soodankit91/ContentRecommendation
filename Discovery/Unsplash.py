import requests
from Discovery.UnsplashAdapter import UnsplashAdapter

class Unsplash:
    API_KEY = ''
    keywords = []

    def __init__(self, API_KEY, keywords):
        self.API_KEY = API_KEY
        self.keywords = keywords

    def requestImagess(self):
        images = []
        links = []
        titles = []
        descriptions = []
        linkTags = []
        ids = []
        i = 0
        while(i < 10):
            parameters = {'client_id': self.API_KEY, 'query': self.keywords, 'page': (i + 1), 'per_page': '50'}
            try:
                images.append(requests.get('https://api.unsplash.com/search/photos?', params=parameters).json())
                print('calling page... ', parameters.get('page'))
            except:
                break
            i += 1

        print(images)


        for image in images :
            for img in image['results']:
                ids.append(img['id'])
                descriptions.append(img['description'])
                links.append(img['urls']['regular'])
                titleTags = set()
                for tag in img['tags']:
                    titleTags.add(tag['title'])
                for tag in img['photo_tags']:
                    titleTags.add(tag['title'])
                linkTags.append(list(titleTags))

        UnsplashAdapter.adaptToES(ids, links, titles, descriptions, linkTags)

if __name__ == '__main__':
    Unsplash('<Your API key>', ['tourism', 'India', 'winters']).requestImagess()
