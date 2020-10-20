# pip install newsapi-python
rom flask import Flask
app = Flask(__name__)
from newsapi import NewsApiClient

@app.route('/')
def main():
    # Init
    newsapi = NewsApiClient(api_key='93e43dd8864e4a708e5a764fea244b69')

    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines( category='technology',
                                            language='en',
                                            country='us')

    # /v2/everything
    top_headlines1 = newsapi.get_top_headlines( category='entertainment',
                                            language='en',
                                            country='us')

    top_headlines2 = newsapi.get_top_headlines( category='sports',
                                            language='en',
                                            country='us')
    # /v2/sources
    sources = newsapi.get_sources()
    print(top_headlines2)

main()