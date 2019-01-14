from bs4 import BeautifulSoup
import requests
import time
from Discovery.wordPressAdapter import wordPressAdapter

class wordPress:

    url = ''

    def __init__(self,url):
        self.url = url

    def constructUrl(self,postfix=''):
        return self.url+postfix

    def scrapeWebsite(self, page_link ):
        links = []
        titles = []
        descriptions = []
        linkTags = []
        ids = []

        page_response = requests.get(page_link, timeout=5)

        page_content = BeautifulSoup(page_response.content, "html.parser")

        for entry in page_content.findAll(class_='site-main'):
            for title in entry.findAll(class_='entry-title'):
                titles.append(title.find('a').text)
                links.append(title.find('a')['href'])

            for id in entry.findAll('article'):
                ids.append(id['id'])
                tags = []
                for tag in id['class']:
                    if (str(tag).startswith("tag-")):
                        splitTags = str(tag).split('-')
                        currTagSplit = ''
                        for i in range (1,len(splitTags)):
                            currTagSplit = currTagSplit + splitTags[i] + ' '
                            currTagSplit = currTagSplit.strip()
                        tags.append(currTagSplit)
                linkTags.append(tags)

            for content in entry.findAll(class_='entry-content'):
                if (content.find('p') is not None):
                    descriptions.append(content.find('p').text)
                else :
                    descriptions.append(' ')

        return ids, links, titles, descriptions, linkTags, page_response.status_code

    def adaptAndInsert(self):
        dataList = []
        i = 1
        while(True):
            time.sleep(10)
            search_link = self.constructUrl('page/' + str(i))

            ids, links, titles, descriptions, linkTags, status_code = self.scrapeWebsite(search_link)
            if (status_code == 404):
                break
            scrapeMore = wordPressAdapter.adaptToES(ids, links, titles, descriptions, linkTags)
            if (not scrapeMore):
                break
            i += 1

        return dataList

if __name__== '__main__':
    wordPress('https://hungrypandadiaries.wordpress.com/').adaptAndInsert()