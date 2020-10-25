import json
import random
from flask import Flask, render_template, request

app = Flask(__name__)


from newsapi.newsapi_client import NewsApiClient
newsapi = NewsApiClient(api_key='93e43dd8864e4a708e5a764fea244b69')


@app.route("/", methods = ["POST", "GET"])
def home():
  if request.method == "POST":
    #request.form["search"]
    #request.form.getlist("categories")
    #if "paywall" in request.form:
    blockPaywall = False
    if "paywall" in request.form:
      blockPaywall = True

    temp = data (request.form.getlist("categories"), str(request.form["search"]), blockPaywall)
  else:
    return render_template("index.html")
    temp = data(["entertainment", "sports", "technology"], "", False)
  
  return temp

def data(category, search, paywall):
  temp = {}
  for i in category:
    b += search(str(i), search, paywall)
  out = ""
  for i in temp["articles"]:
    out += render_template("index.html", content = i["title"])
  return out


#modify JSON or headline to include paywall info
def payInfo(a):
  for i in a["articles"]:
    key = i["source"]["name"] #source we are checking
    toAdd = paywall.get(key, False)
    i["paywall"] = toAdd

  return a


#take JSON of headlines, return all that aren't behind a paywall
def noPay(a):
  for i in a["articles"]:
    if i["paywall"]:
      a.pop(i)
  return a

#returns all headlines in a given category

def search(cat, search, blockPaywall):
  request = newsapi.get_top_headlines( 
  q = search, category=cat,language='en',country='us')
  c = payInfo(request)
  if blockPaywall:
    return noPay(c)

  return c




#List of paywall sites
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


if __name__ == "__main__":  # Makes sure this is the main process
	app.run(# Starts the site
		host='0.0.0.0',  # Establishes the host, required for repl to detect the site
		port=random.randint(2000, 9000),  # Randomly select the port the machine hosts on.
    debug = True
	)

