import requests
import urllib.request
import time
from bs4 import BeautifulSoup


class Scraper:

    def get_html_from_url(self, url: str):
        #f = open("response.txt","w")
        #f.write(requests.get(url).text)
        return requests.get(url).text

    def scrape(self, target_tag: str, html_page: str) -> None:
        # Parse HTML and save to BeautifulSoup object
        soup = BeautifulSoup(html_page, "html.parser")
        # To download the whole data set, let's do a for loop through all a tags
        a_tags = soup.findAll('a')
        for a in a_tags:
            link = a[target_tag]
            if ".xml" in link:
                download_url = link
                filename = link[link.find('/jmlr') + 1:]
                # filename = link
                print(link, "----", filename)
                urllib.request.urlretrieve(download_url, './' + filename)
            else:
                continue
            # time.sleep(1) #pause the code for a sec

