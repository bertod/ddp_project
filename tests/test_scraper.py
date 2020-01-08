import pytest
import unicodedata
from ResearcherNetwork.scraper import Scraper


class TestScraper:
    def setup_method(self):
        self.scraper = Scraper()

    def test_get_html_from_url(self):
        url = "https://dblp.org/db/about/team.html"
        response = self.scraper.get_html_from_url(url)
        f = open("tests/resources/html_response.html", "r", encoding="utf8")
        html_response = f.read()
        html_response = remove_control_characters(html_response)
        response = remove_control_characters(response)
        assert response == html_response

    def test_scrape(self):
        f = open("tests/resources/page_html_to_scrape.html", "r")
        html_page = f.read()
        self.scraper.scrape(target_tag='href', html_page=html_page,
                            path_to_save="tests/resources/", target_title="jmlr")
        try:
            f_xml = open("tests/resources/jmlr/ChenLZ15.xml", "r", encoding="utf8")
        except FileNotFoundError:
            print("File not found")
            pytest.fail()
        scrape_result = f_xml.read()
        f_scrape = open("tests/resources/real_scrape_response.xml", "r")
        real_scrape_response = f_scrape.read()
        scrape_result = remove_control_characters(scrape_result)
        real_scrape_response = remove_control_characters(real_scrape_response)
        assert scrape_result == real_scrape_response


def remove_control_characters(s):
    """
    Helper Function for removing control chars from strings
    before comparison
    :param s:
    :return:
    """
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")
