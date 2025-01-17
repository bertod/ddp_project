# from __future__ import annotations
from abc import ABC, abstractmethod
import requests
import urllib.request
import os
import time
from bs4 import BeautifulSoup


class ScraperCreator(ABC):

    @abstractmethod
    def factory_method(self):
        pass

    def run_scrape(self, target_tag: str, url: str, html_page: str,
                   target_title: str, path_to_save: str = "ResearcherNetwork/resources/"):
        product = self.factory_method()

        if url:
            html_page = product.get_html_from_url(url)

        return product.scrape(target_tag, html_page,
                              target_title, path_to_save)


class Scraper(ABC):
    """
        :param target_tag: HTML tag you want to get from scraping
        :param html_page: HTML Code obtained from the get_html_from_url method
        :param path_to_save: the directory path where you want to save results
        :param target_title: the name of the journal or conference you are looking for
        :return:
        """
    @abstractmethod
    def get_html_from_url(self, url: str) -> str:
        pass

    @abstractmethod
    def scrape(self, target_tag: str, html_page: str,
               target_title: str, path_to_save: str = "ResearcherNetwork/resources/") -> None:
        pass


class ConcreteScraperDblp(Scraper):

    def get_html_from_url(self, url: str) -> str:
        """
        :param url: url to fetch
        :return: the HTML of the requested url
        """
        return requests.get(url).text

    def scrape(self, target_tag: str, html_page: str,
               target_title: str, path_to_save: str = "ResearcherNetwork/resources/") -> None:
        """
        :param target_tag: attribute of HTML tag we know we'll find what we are looking for (e.g. href)
        :param html_page: HTML code obtained by get_html_from_url
        :param target_title: the title (possibly the abbreviation) of avenue (e.g. icml)
        :param path_to_save: where the scraper must locate the downloaded files
        :return:
        """
        if not path_to_save:
            path_to_save = ""
        if not os.path.exists(path_to_save + '/' + target_title):
            os.makedirs(path_to_save + '/' + target_title)
        soup = BeautifulSoup(html_page, "html.parser")
        a_tags = soup.findAll('a')
        count_requests = 0
        for a in a_tags:
            try:
                link = a[target_tag]
            except KeyError:
                continue
            if ".xml" in link:
                download_url = link
                filename = path_to_save + link[link.find('/' + target_title) + 1:]
                if not os.path.exists(filename):
                    print(link, "----", filename)
                    urllib.request.urlretrieve(download_url, './' + filename)
                    count_requests += 1
            else:
                continue
            if count_requests == 300:
                print("-- I need to stop for 60secs before downloading other data, "
                      "otherwise the server would block us for DDos attack")
                time.sleep(60)
                count_requests = 0
            # time.sleep(1)  # pause the code for a sec


class ConcreteScraperDblpCreator(ScraperCreator):

    def factory_method(self) -> ConcreteScraperDblp:
        return ConcreteScraperDblp()