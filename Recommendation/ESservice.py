from elasticsearch import Elasticsearch

class ESservice:
    __instance = None

    @staticmethod
    def getInstance():
        if ESservice.__instance == None:
            ESservice()
        return ESservice.__instance

    def __init__(self):
        if ESservice.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ESservice.__instance = self

    def getConnection(self):
        return Elasticsearch([{"host": "localhost", "port": 9200}])


    def createIndex(self,numShards=1, numReplicas=1):
        request_body = {
            "settings": {
                "number_of_shards": numShards,
                "number_of_replicas": numReplicas
            }

        }
        es = self.getConnection()
        es.indices.create(index="discovery", body=request_body)


    def createMapping(self,docType = "media", indexName="discovery"):
        myMap = {
            "media": {
                "properties": {
                    "title": {"type": "text","analyzer": "snowball"},
                    "description": {"type": "text","analyzer": "snowball"},
                    "id": {"type": "text"},
                    "tags": {"type": "text","analyzer": "snowball"},
                    "url": {"type": "keyword"},
                    "source": {"type": "keyword"},  # website name
                    "topic": {"type": "keyword"},  # list of topics like food, travel etc
                    "mediaType": {"type": "text"}  # image, video or text
                }}
        }

        es = self.getConnection()
        es.indices.put_mapping(index=indexName, doc_type=docType, body=myMap)


    def insertSingle(self,data, indexName="discovery", docType="media"):
        es = self.getConnection()
        for dataItem in data :
            if (not self.alreadyInserted(dataItem['id'])):
                res = es.index(index=indexName, doc_type=docType, body=dataItem)
            else :
                return False
        return True

    def alreadyInserted(self, id):
        searchQuery = {
            'query': {
                'simple_query_string': {
                    "query": id,
                    "fields": ["id"]
                }
            }
        }
        res = self.getConnection().search(index='discovery', doc_type='media', body=searchQuery)
        if (res['hits']['total'] == 0):
            return False
        return True


    def deleteData(self):
        es = self.getConnection()
        res = es.indices.delete(index="discovery")

    def main(self):
        print("main called")
        self.createIndex()
        self.createMapping()
        #self.deleteData()

if __name__== "__main__":
    ESservice().main()