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
        Homepage with api data

    """
    if request.method == "POST":
        blockPaywall = False
        if "paywall" in request.form:
            blockPaywall = True
        temp = data(
            request.form.getlist("categories"), str(request.form["search"]),
            blockPaywall)
    else:
        temp = data(["entertainment", "sports", "technology"], "", False)

    return render_template("index.html", tableList=combine(temp))


def combine(temp):
    """
    Make api output easy to me 

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

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
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

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
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

    """  
    out = []
    for x in temp:
        for y in x["articles"]:
            out.append(y["url"])

    return out

    
def nameList(temp):
    """
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

    """  
    out = []
    for x in temp:
        for y in x["articles"]:
            out.append(y['source']["name"])

    return out


def headLineList(temp):
    """
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

    """  
    out = []
    for x in temp:
        for y in x["articles"]:
            out.append(y["title"])

    return out


def images(temp):
    """
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

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
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

    """
    out = []
    for x in temp:
        for y in x["articles"]:
            if y["paywall"]:
                out.append("Yes")
            else:
                out.append("No!")

    return out


def data(category, search, paywall):
    """
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

    """
    temp = []
    for i in category:
        temp.append(find(i, search, paywall))  #search for

    return temp


#modify JSON or headline to include paywall info
def payInfo(a):
    """
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

    """
    for i in a["articles"]:
        key = i["source"]["name"]  #source we are checking
        toAdd = paywall.get(
            key, False
        )  #if it's in our list of paywall sites we will add True, if not False
        i["paywall"] = toAdd

    return a


#take JSON (dict) of headlines, return all that aren't behind a paywall
def noPay(a):
    """
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

    """
    out = []
    for i in a["articles"]:
        if not i["paywall"]:
            out.append(i)

    return {"articles": out}


#api call
def find(cat, search, blockPaywall):
    """
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

    """
    request = newsapi.get_top_headlines(
        q=search, category=cat, language='en', country='us')
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

if __name__ == "__main__":  #Flask stuff
    app.run(  # Starts the site
        host=
        '0.0.0.0',  # Establishes the host, required for repl to detect the site
        port=random.randint(
            2000, 9000),  # Randomly select the port the machine hosts on.
        debug=False)
