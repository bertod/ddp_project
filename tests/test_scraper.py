import pytest
import unicodedata
import shutil
from ResearcherNetwork.scraper import Scraper
from ResearcherNetwork.scraper import ConcreteScraperDblpCreator
from ResearcherNetwork.helper_functions import remove_control_characters


class TestScraper:
    def setup_method(self):
        self.scraper = ConcreteScraperDblpCreator()

    def test_scrape(self):
        f = open("tests/resources/page_html_to_scrape.html", "r")
        html_page = f.read()
        self.scraper.run_scrape(target_tag='href', html_page=html_page,
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
        f_scrape.close()
        f_xml.close()
        f.close()
        shutil.rmtree("tests/resources/jmlr")
