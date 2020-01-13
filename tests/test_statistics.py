import pytest
from ResearcherNetwork.helper_functions import remove_control_characters
from ResearcherNetwork.statistics import StatisticsGrabber


class TestStatistics:
    def setup_method(self):
        self.statistics_grabber = StatisticsGrabber("tests/resources/parser_out_statistics_test.txt")

    def test_get_statistics(self):
        statistics_dict = self.statistics_grabber.get_statistics()
        assert statistics_dict['n_papers'] == 11
        assert statistics_dict['n_authors'] == 24
        assert statistics_dict['avg_authors_paper'] == 3
        assert statistics_dict['papers_authors_count'] == {'Manuel Fernandez': 6,
                                                           'Ali Rahimi': 4,
                                                           'Tao Lin': 4,
                                                           'Cameron Voloshin': 3,
                                                           'Ehsan Kazemi 0001': 2}
        assert statistics_dict['avg_papers_author'] == 1.7
        assert statistics_dict['papers_year_count'] == {2018: 6, 2019: 5}
        assert statistics_dict['avg_papers_year'] == 5.5
        assert statistics_dict['papers_avenue'] == {'AAAI': 3, 'ICML': 8}
