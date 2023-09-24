from urllib.request import urlopen, HTTPError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random
import requests


"""
It initializes various variables, including sets to store visited pages (pages),
all external links (allExtLinks), and all internal links (allIntLinks).
It also gets the current timestamp and seeds the random number generator
with it to ensure randomization in link selection.
"""


pages = set()
allExtLinks = set()
allIntLinks = set()
current_time = datetime.datetime.now()
timestamp_float = current_time.timestamp()
random.seed(timestamp_float)


# Retrieves a list of all Internal links (within the same domain) found on a page
def getInternalLinks(bs, includeUrl):
    includeUrl = "{}://{}".format(
        urlparse(includeUrl).scheme, urlparse(includeUrl).netloc
    )
    internalLinks = []
    # Finds all links that begin with a "/"
    for link in bs.find_all("a", href=re.compile("^(/|.*" + includeUrl + ")")):
        if link.attrs["href"] is not None:
            if link.attrs["href"] not in internalLinks:
                if link.attrs["href"].startswith("/"):
                    internalLinks.append(includeUrl + link.attrs["href"])
                else:
                    internalLinks.append(link.attrs["href"])
    return internalLinks


# Retrieves a list of all external links (outside the current domain) found on
# a page
def getExternalLinks(bs, excludeUrl):
    externalLinks = []
    # Finds all links that start with "http" or "www" that do
    # not contain the current URL
    for link in bs.find_all(
        "a", href=re.compile("^(http|www)((?!" + excludeUrl + ").)*$")
    ):
        if link.attrs["href"] is not None:
            if link.attrs["href"] not in externalLinks:
                externalLinks.append(link.attrs["href"])
    return externalLinks


"""
Fetches the HTML content of the starting URL, parses it with BeautifulSoup,
and retrieves external links from that page. If there are no external links,
it recursively looks for external links on internal pages. It returns a
random external link from the list.
"""


def getRandomExternalLink(startingPage):
    try:
        html = urlopen(startingPage)
        bs = BeautifulSoup(html, "html.parser")
        externalLinks = getExternalLinks(bs, urlparse(startingPage).netloc)
        if len(externalLinks) == 0:
            print("No external links, looking around the site for one")
            domain = "{}://{}".format(
                urlparse(startingPage).scheme, urlparse(startingPage).netloc
            )
            internalLinks = getInternalLinks(bs, domain)
            return getRandomExternalLink(
                internalLinks[random.randint(0, len(internalLinks) - 1)]
            )
        else:
            return externalLinks[random.randint(0, len(externalLinks) - 1)]

    except HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason} - {startingPage}")
        return None
    except Exception as e:
        print(f"An error occurred while fetching {startingPage}: {e}")
        return None


"""
It uses the getRandomExternalLink function to select a random external
link and follows it. The process continues recursively until the specified
depth is reached or there are no external links.
"""


def followExternalOnly(startingSite, maxDepth=3):
    if maxDepth <= 0:
        return
    externalLink = getRandomExternalLink(startingSite)
    if externalLink:
        print("Random external link is: {}".format(externalLink))
        followExternalOnly(externalLink)


"""
1) It fetches the HTML content of the site, parses it with BeautifulSoup,
and extracts both internal and external links.
2) It adds the external links to the allExtLinks set and prints them.
3) It also adds internal links to the allIntLinks set and recursively
follows external links on internal pages.
"""


def getAllExternalLinks(siteUrl):
    try:
        html = urlopen(siteUrl)
        domain = "{}://{}".format(urlparse(siteUrl).scheme, urlparse(siteUrl).netloc)
        bs = BeautifulSoup(html, "html.parser")
        internalLinks = getInternalLinks(bs, domain)
        externalLinks = getExternalLinks(bs, domain)

        for link in externalLinks:
            if link not in allExtLinks:
                allExtLinks.add(link)
                print(link)
        for link in internalLinks:
            if link not in allIntLinks:
                allIntLinks.add(link)
                getExternalLinks(link, domain)

    except HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason} - {siteUrl}")
        return None
    except Exception as e:
        print(f"An error occurred while fetching {siteUrl}: {e}")
        return None


"""
1) The script adds the page URL to the allIntLinks set.
2) It calls the getAllExternalLinks function to start crawling external
links from the Wikipedia main page.
3) It includes exception handling for HTTP errors and other exceptions.
4) If the user interrupts the script with a KeyboardInterrupt (Ctrl+C),
it prints a message and exits gracefully.
"""


try:
    allIntLinks.add("https://www.oreilly.com/")
    getAllExternalLinks("https://www.oreilly.com/")
except KeyboardInterrupt:
    print("Execution interrupted by user.")
except Exception as e:
    print(f"An error ocurred: {e}")
