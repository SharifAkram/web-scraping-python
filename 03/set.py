# looks for all links with /wiki/ with recursion counter and limit

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re

pages = set()


def getLinks(pageUrl, max_recursion, current_recursion=0):
    global pages
    if current_recursion >= max_recursion:
        return

    try:
        html = urlopen("https://en.wikipedia.org{}".format(pageUrl))
    except HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        return
    except URLError as e:
        print(f"URL Error: {e.reason}")
        return

    bs = BeautifulSoup(html, "html.parser")
    for link in bs.find_all("a", href=re.compile("^(/wiki/)")):
        if "href" in link.attrs:
            if link.attrs["href"] not in pages:
                # We have encountered a new page
                newPage = link.attrs["href"]
                print(newPage)
                pages.add(newPage)
                getLinks(newPage, max_recursion, current_recursion + 1)


# Returns all links on the first page with level set to 1
getLinks("", max_recursion=1)
