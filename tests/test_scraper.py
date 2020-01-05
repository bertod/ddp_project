import pytest
from ResearcherNetwork.scraper import Scraper


class TestScraper:
    def setup_method(self):
        self.scraper = Scraper()

    def test_get_html_from_url(self):
        url = "https://dblp.org/db/about/team.html"
        response = self.scraper.get_html_from_url(url)
        f = open("html_response.html", "r", encoding="utf8")
        html_response = f.read()
        assert response == html_response

    # def test_scrape(self):
    #     f = open("page_html_to_scrape.html", "r")
    #     html_page = f.read()
    #     #print(html_page)
    #     self.scraper.scrape(target_tag='href', html_page=html_page)

