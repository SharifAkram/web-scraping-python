from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()


def getLinks(pageUrl):
    global pages
    try:
        html = urlopen("https://en.wikipedia.org{}".format(pageUrl))
        bs = BeautifulSoup(html, "html.parser")
        try:
            print(bs.h1.get_text())
            print(bs.find(id="mw-content-text").find_all("p")[0])
            print(bs.find(id="ca-edit").find("span").find("a").attrs["href"])
        except AttributeError:
            print("this page is missing something! Continuing.")

        for link in bs.find_all("a", href=re.compile("^(/wiki/)")):
            if "href" in link.attrs:
                if link.attrs["href"] not in pages:
                    # We have encountered a new page
                    newPage = link.attrs["href"]
                    print("-" * 20)
                    print(newPage)
                    pages.add(newPage)
                    getLinks(newPage)

    except Exception as e:
        print(f"An error occurred: {e}")


getLinks("")
