import random
from flask import Flask, render_template, request

app = Flask(__name__)

from newsapi.newsapi_client import NewsApiClient
newsapi = NewsApiClient(api_key='78b9d599c4f94f8fa3afb1a5458928d6')


@app.route("/", methods=["POST", "GET"])
def home():
    """
    Homepage and site control

    Returns
    -------
    html
        Defult: top 20 entertainment, sports, and technology news articles
        After query input: Homepage with api call results

    """
    if request.method == "POST":
        blockPaywall = False
        if "paywall" in request.form:
            blockPaywall = True
        search = str(request.form["search"])
        categories = request.form.getlist("categories")

        temp = data(categories, search, blockPaywall)

        #values to send back to html
        prevSearch = str(request.form["search"])
        prevPaywall = blockPaywall
        checked = False
        if "checkbox" in request.form:
            checked = True
        entertainment = "Entertainment" in categories
        sports = "Sports" in categories
        technology = "Technology" in categories
    else:
        temp = data(["entertainment", "sports", "technology"], "", False)

        #default form values to send to html
        prevSearch = ""
        prevPaywall = False
        checked = False
        entertainment = True
        sports = True
        technology = True

    return render_template("index.html", tableList=combine(temp), 
    prev = prevSearch, paywallinfo = prevPaywall, check = checked, ent = entertainment, sport = sports, tech = technology)


def combine(temp):
    """
    Makes api output html friendly

    Parameters
    ----------
    temp : array of dicts
        API call(s) results

    Returns
    -------
    2-d list
        List of lists containing each output line to be put in the results table

    """
    Names = nameList(temp)
    Headlines = headLineList(temp)
    Images = images(temp)
    Paywalls = paywallList(temp)
    URL = urlList(temp)
    Date = dateList(temp)
    out = []
    for i in range(len(Names)):
        temp = []
        temp.append(Names[i])
        temp.append(Headlines[i])
        temp.append(URL[i])
        temp.append(Images[i])
        temp.append(Paywalls[i])
        temp.append(Date[i])
        out.append(temp)

    return out


def dateList(temp):
    """
    Returns a list of all dates from the API call(s)

    Parameters
    ----------
    temp : array of dicts
        API call(s) results

    Returns
    -------
    list
        All dates from the API results, formatted for output

    """  
    out = []
    for x in temp:
        for y in x["articles"]:
            dateTemp = str(y["publishedAt"])
            end = dateTemp.index("T")
            dateTemp = dateTemp[5:7] + "/" + dateTemp[8:end] + "/" + dateTemp[
                2:4]
            out.append(dateTemp)

    return out


def urlList(temp):
    """
    Returns a list of all urls from the API call(s)

    Parameters
    ----------
    temp : array of dicts
        API call(s) results

    Returns
    -------
    list
        All urls from the API results

    """  
    out = []
    for x in temp:
        for y in x["articles"]:
            out.append(y["url"])

    return out

    
def nameList(temp):
    """
    Returns a list of all sours names from the API call(s)

    Parameters
    ----------
    temp : array of dicts
        API call(s) results

    Returns
    -------
    list
        All source names from the API results
    """   
    out = []
    for x in temp:
        for y in x["articles"]:
            out.append(y['source']["name"])

    return out


def headLineList(temp):
    """
    Returns a list of all headlines from the API call(s)

    Parameters
    ----------
    temp : array of dicts
        API call(s) results

    Returns
    -------
    list
        All headlines from the API results,

    """  
    out = []
    for x in temp:
        for y in x["articles"]:
            out.append(y["title"])

    return out


def images(temp):
    """
    Returns a list of all image urls from the API call(s)

    Parameters
    ----------
    temp : array of dicts
        API call(s) results

    Returns
    -------
    list
        All image urls from the API results. If there was no image url, includes default placeholder image

    """  
    out = []
    for x in temp:
        for y in x["articles"]:
            if str(y["urlToImage"]) == "None":
                out.append(
                    "https://via.placeholder.com/128/343a40/FFFFFF/?text=No%20Image"
                )
            else:
                out.append(y["urlToImage"])

    return out


def paywallList(temp):
    """
    Returns a list of all paywall information pertaining to the API call(s)

    Parameters
    ----------
    temp : array of dicts
        API call(s) results

    Returns
    -------
    list
        All paywall information pertaining to the API results, formatted for output

    """  
    out = []
    for x in temp:
        for y in x["articles"]:
            if y["paywall"]:
                out.append("Yes")
            else:
                out.append("None spotted!")

    return out


def data(category, search, paywall):
    """
    Calls API function for each category queried 

    Parameters
    ----------
    category : list
        List of all categories to search
    search : str
        Search query (or "" if none input)
    paywall : bool
        True if the user wants to block paywall sites
      
    Returns
    -------
    List of dicts
      API call(s) results
        
    """
    temp = []
    for i in category:
        temp.append(find(i.lower(), search, paywall))  

    return temp


def payInfo(a):
    """
    Adds bool value for whether the source is expected to have a paywall to the dict returned from NewsAPI

    Parameters
    ----------
    a : dict
        Result returned from API call

    Returns
    -------
    dict
        API call result with a "paywall" entry

    """
    for i in a["articles"]:
        key = i["source"]["name"]  
        toAdd = paywall.get(
            key, False
        ) 
        i["paywall"] = toAdd

    return a



def noPay(a):
    """
    If the user doesn't want to see paywall information, this removes all results thought to have paywalls.

    Parameters
    ----------
    a : dict
        Result returned from API call with paywall information added

    Returns
    -------
    dict
        Dict containing list of articles not behind a paywall

    """
    out = []
    for i in a["articles"]:
        if not i["paywall"]:
            out.append(i)

    return {"articles": out}



def find(categ, search, blockPaywall):
    """
    Completes API call for specified query.

    Parameters
    ----------
    category : string
        Category to search
    search : str
        Search query (or "" if none input)
    blockPaywall : bool
        True if the user wants to block paywall sites

    Returns
    -------
    dict
        Results of API call and paywall modification

    """
    request = newsapi.get_top_headlines(
        q=search, category=categ, language='en', country='us')
    withPaywall = payInfo(request)  #add paywall info to dict
    if blockPaywall:
        return noPay(withPaywall)  #deletes all entries that have paywall

    return request


#List of paywall sites (dict has more efficient lookup than set)
paywall = {
    "The Advertiser": True,
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
