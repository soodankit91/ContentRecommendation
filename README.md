# Content Recommendation
## A NLP based framework for content recommendation
   
   Please refer [this blog](https://medium.com/social-media-help-support/a-nlp-based-framework-for-content-recommendation-e49a73d12220) on a detailed description of the framework. 

## Using the framework 

### Adding a new data source : 

1. Write a class in the Discovery package to retrieve content from the data source.
   For instance, in the code base, YouTube is a data source.

2. Write an adapter for the class by extending the class AbstractContentSource (AbstractContent.py).
   YouTubeAdapter is the adapter for YouTube.
   
3. Ensure that the adapted data is sent to the ElasticSearch store.
   YouTubeAdapter adapts the data from YouTube and populates in the ElasticSearch.

### Populating the ElasticSearch data source

This is an important step as the performance of the recommender will depend upon how good and exhaustive the data store is.

1. Provide the desired keywords and URLs (for web scrapping or API calls).
   For instance, in the current code, in order to populate YouTube's data for video recommendation, one needs to instantiate      the YouTube class by passing an API key and a list of keywords(for recommendation) to its constructor.
   
2. Collect relevant data from the data source.
   For instance, we call requestVideos() method of YouTube class to obatin data relevant to the keywords provided.
   
3. Adapt data and feed into the Elastic search data store
   Every data source has an adapter, for instance YouTube has YouTubeAdapter, which "adapts" the data collected into a format    compatible with our data store.
   
Note that the class ESservice, responsible for inserting data in ElasticSearch, is a singleton class.
   
### Recommending Desired Content

It is to be noted that only the content present in our ElasticSearch data store shall be recommended 

1. Download word2vec from [here](https://code.google.com/archive/p/word2vec/) and place it inside the resources folder.
2. Instantiate RecommendationEngine by passing a list of media types and a list of content sources to its constructor. 
3. Call the method getRecommendations() using the instance created in step 2 and pass to it a list of keywords for which a        recommendation is desired. 
