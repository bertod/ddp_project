import requests
import urllib.request
import os
import time
from bs4 import BeautifulSoup


class Scraper:

    def get_html_from_url(self, url: str):
        # f = open("response.txt","w")
        # f.write(requests.get(url).text)
        return requests.get(url).text

    def scrape(self, target_tag: str, html_page: str,
               target_title: str, path_to_save: str = "ResearcherNetwork/resources/") -> None:
        """
        :param target_tag: HTML tag you want to get from scraping
        :param html_page: HTML Code obtained from the get_html_from_url method
        :param path_to_save: the directory path where you want to save results
        :param target_title: the name of the journal or conference you are looking for
        :return:
        """
        if not path_to_save:
            path_to_save = ""
        if not os.path.exists(path_to_save+'/'+target_title):
            os.makedirs(path_to_save+'/'+target_title)
        soup = BeautifulSoup(html_page, "html.parser")
        a_tags = soup.findAll('a')
        for a in a_tags:
            try:
                link = a[target_tag]
            except KeyError:
                continue
            if ".xml" in link:
                download_url = link
                filename = path_to_save+link[link.find('/'+target_title) + 1:]
                if not os.path.exists(filename):
                    print(link, "----", filename)
                    urllib.request.urlretrieve(download_url, './' + filename)
            else:
                continue
            # time.sleep(1) #pause the code for a sec

