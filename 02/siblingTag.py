# The BeautifulSoup next_siblings() function makes it trivial to collect
# data from tables, especially ones with title rows:

from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://www.pythonscraping.com/pages/page3.html")
bs = BeautifulSoup(html, "html.parser")

for sibling in bs.find("table", {"id": "giftList"}).tr.next_siblings:
    print(sibling)
