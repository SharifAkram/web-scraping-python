# A program that creates a random path through Wikipedia articles.

from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

"""
html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
bs = BeautifulSoup(html, "html.parser")
for link in bs.find_all("a"):
    if "href" in link.attrs:
        print(link.attrs["href"])


html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
bs = BeautifulSoup(html, "html.parser")
for link in bs.find("div", {"id": "bodyContent"}).find_all(
    "a", href=re.compile("^(/wiki/)((?!:).)*$")
):
    if "href" in link.attrs:
        print(link.attrs["href"])
"""


def getLinks(articleUrl):
    try:
        html = urlopen("https://en.wikipedia.org{}".format(articleUrl))
        bs = BeautifulSoup(html, "html.parser")
        return bs.find("div", {"id": "bodyContent"}).find_all(
            "a", href=re.compile("^(/wiki/)((?!:).)*$")
        )
    except Exception as e:
        print("An error occurred:", e)
        return []


try:
    current_time = datetime.datetime.now()
    timestamp_float = current_time.timestamp()
    random.seed(timestamp_float)

    links = getLinks("/wiki/Kazakhstan")
    while len(links) > 0:
        newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
        print(newArticle)
        links = getLinks(newArticle)
except KeyboardInterrupt:
    print("Execution interrupted by user.")
