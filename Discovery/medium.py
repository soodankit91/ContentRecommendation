import requests
import json
from Discovery.mediumAdapter import MediumAdapter

class MediumUpdate:
    url_pre = "https://medium.com/"
    url_post = "/latest"

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Cache-Control': "no-cache",
    }

    def __init__(self, mediumID):
        self.mediumID = mediumID

    def constructURL(self):
        return self.url_pre + str(self.mediumID) + self.url_post

    def getResponseList(self):
        url = self.constructURL()
        response = requests.request("GET", url, headers=self.headers)

        print(response.text)

        pos = response.text.find("{")
        json_response = json.loads(response.text[pos:len(response.text)])
        postIds = []

        for itr in json_response['payload']['streamItems']:
            if 'postPreview' in itr:
                postIds.append(itr['postPreview']['postId'])
        # print(json_response['payload']['references']['Post'])
        # print(postIds)

        dataList = []
        links = []
        titles = []
        descriptions = []
        linkTags = []
        ids = []
        id = 0

        for postId in postIds:
            id += 1

            post = json_response['payload']['references']['Post'][postId]
            ids.append(post['id'])
            titles.append(post['title'])
            descriptions.append(str(post['content']['subtitle']))
            tags = []
            for tag in post['virtuals']['tags']:
                tags.append(tag['name'])
            linkTags.append(tags)
            links.append("https://medium.com/" + json_response['payload']['user']['username'] + '/' + post['id'])


        MediumAdapter.adaptToES(ids,links,titles,descriptions,linkTags)

    def adaptAndInsert(self):
        self.getResponseList()



if __name__ == '__main__':
    MediumUpdate('@space10').adaptAndInsert()
