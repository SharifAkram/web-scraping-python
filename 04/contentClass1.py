import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body


def getPage(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, "html.parser")


def scrapeNYTimes(url):
    bs = getPage(url)
    # Find the title within the correct element, e.g., <title>
    title = bs.find("title").text if bs.find("title") else "Title not found"

    # Find the article content within the correct element, e.g., <article>
    article = bs.find("article")
    if article:
        paragraphs = article.find_all("p")
        body = "\n".join([p.text for p in paragraphs])
    else:
        body = "Body not found"

    return Content(url, title, body)


def scrapeBrookings(url):
    bs = getPage(url)
    title = bs.find("h1").text
    post_body = bs.find("div", {"class": "post-body"})
    if post_body:
        body = post_body.text
    else:
        body = "Body not found"
    return Content(url, title, body)


url = "https://www.brookings.edu/blog/future-development/2018/01/26/delivering-inclusive-urban-access-3-uncomfortable-truths/"
content = scrapeBrookings(url)
print("Title: {}".format(content.title))
print("URL: {}\n".format(content.url))
print(content.body)

url = "https://www.nytimes.com/2017/05/13/business/china-railway-one-belt-one-road-1-trillion-plan.html"
content = scrapeNYTimes(url)
print("\nTitle: {}".format(content.title))
print("URL: {}\n".format(content.url))
print(content.body)
