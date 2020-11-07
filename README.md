# Capital One NewsAPI Project


## View Web App

View live [site](http://www.capitalone.alexdouglas.me/)

If you want to run locally, all dependencies are listed in requirements.txt

## What it does
When the user opens the web app, there are news articles arleady populating the output table. These include 20 top headlines from each entertainment, sports, and technology. The user can then input custom search queries--they can input keywords to be searched for, limit the categories that articles will be shown from, and opt to not include articles from sites that are known to have paywalls.

The search results are limited to articles from the "get_top_headlines" News API query, as this is the only way to also limit searches to specific categories. More technical details are in the following section.


## How I built it
My web app uses flask to integrate a python backend with my html frontend. 

Backend details (app.py)
The program first completes News API call(s), based on user input or default settings, if there has been no user input. If multiple categories were selected, multiple API calls are completed. After the dictionary/JSON is retrieved from News API, the program adds "paywall" information to each articles, based on a hardcoded dictionary containing a list of news sites known to have soft or hard paywalls. I found this list from multiple sources ([1](https://en.wikipedia.org/wiki/Category:Websites_utilizing_paywalls), [2](https://www.reddit.com/r/worldnews/wiki/paywalls)) and my own investigation. I use a dict rather than a set to store this information so that this feature has O(1) lookup time. If the user requested no paywall sites to be shown, a new dict is made without sources marked as having a paywall. 

Once the API call and paywall modification is complete, the progam has a list containing 1-3 dicts each with 0-20 articles. To make the backend work easier, the program then converts this into a list of lists, with each list containing one row of output information. 

Front end details (/templates/index.html)
The list of lists is passed to the backend using flask. The backend primarily uses bootstrap templates, including a heaader (with the Capital One logo, of course), the data input forms, and the output table. Using a for loop, the data passed to the backend is added to the table. After searching, the page is loaded with previous query still in the forms (through a very hacky method of passing the POST variables back to the html through flask). 


## What I learned (the narrative) 
Coming into this project, I had no experience doing front-end development. My coding experience was limited to creating programs that only needed to be used by myself (or group members). So, in doing this project I learned a ton. I used the technologies I had been told were most intuitive to pick up (flask and html). I began by working on my back-end functionality--making functions that can make a NewsAPI call based on specific queries. Then, I learned how to use flask to setup a basic web app and how to use html and to style said web app. After many YouTube series watched and pages of documentation read, I had a web app that was working--in Repl.it, that is. I learned that getting a web app working on a production server is not quite getting a web app deployed. I learned how to setup my flask project in a virtual environment that would then be compatible with heroku hosting and, finally, I got my site working. 

I now feel fairly comfortable creating simple web apps and making them actually work, skills that I am thrilled to have learned over these past few weeks. 
