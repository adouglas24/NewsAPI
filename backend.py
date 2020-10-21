# pip install newsapi-python
import json
from flask import Flask
app = Flask(__name__)
from newsapi.newsapi_client import NewsApiClient
newsapi = NewsApiClient(api_key='93e43dd8864e4a708e5a764fea244b69')


@app.route('/')
#modify JSON or headline to include paywall info
def payInfo(a):
  for i in a["articles"]:
    key = i["source"]["name"] #source we are checking
    toAdd = paywall.get(key, False)
    i["paywall"] = toAdd

  return a


#take JSON of headlines, return all that aren't behind a paywall
def noPay(a):
  return a

#returns all headlines in a given category
def category(a):
  b = newsapi.get_top_headlines( category=a,language='en',country='us')
  return payInfo(b)



def main():
  category("business")
  category("sports")
  category("technology")


#Paywall sites
paywall = {"The Advertiser": True,
"Adweek": True,
"Arabian Business": True,
"Bloomberg News": True,
"Bloomberg": True,
"The Boston Globe": True,
"Boston Globe": True,
"Boston Herald": True,
"The Christian Science Monitor": True,
"The Courier-Mail": True,
"The Daily Telegraph": True,
"The Diplomat": True,
"The Economist": True,
"Fiji Times": True,
"Financial Times": True,
"Geelong Advertiser": True,
"The Globe and Mail": True,
"Globe and Mail": True,
"Herald Sun": True,
"Houston Chronicle": True,
"Irish Independent": True,
"The Irish Times": True,
"Irish Times": True,
"Los Angeles Times": True,
"MIT Technology Review": True,
"National Business Review": True,
"National Post": True,
"The New York Times": True,
"New York Times": True,
"News/North": True,
"Northern News Services": True,
"Northern Territory News": True,
"Orange County Register": True,
"Scientific American": True,
"The Seattle Times": True,
"Seattle Times": True,
"Tech in Asia": True,
"The Athletic": True,
"Athletic": True,
"TheStar.com": True,
"The Times": True,
"Times": True,
"Vanity Fair": True,
"De Volkskrant": True,
"The Wall Street Journal": True,
"Wall Street Journal": True,
"The Washington Post": True,
"Washington Post": True,
"Wired": True,
"Yellowknifer": True,
"The Sunday Times": True,
"Sunday Times": True,
"Kyiv Post": True, 
"Haaretz": True, 
"The Australian": True, 
"Australian": True, 
"Sydney Morning Herald": True,
"The Age": True,
"The Athletic": True,
}
main()