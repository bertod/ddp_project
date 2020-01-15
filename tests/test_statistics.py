import pytest
from ResearcherNetwork.helper_functions import remove_control_characters
from ResearcherNetwork.statistics import StatisticsGrabber


class TestStatistics:
    def setup_method(self):
        self.statistics_grabber = StatisticsGrabber("tests/resources/parser_out_statistics_test.txt",
                                                    "tests/resources/statistics_out.txt")

    def test_get_statistics(self):
        statistics_dict = self.statistics_grabber.get_statistics()
        assert statistics_dict['n_papers'] == 12
        assert statistics_dict['n_authors'] == 28
        assert statistics_dict['avg_authors_paper'] == 3
        assert statistics_dict['papers_authors_count'] == [('Manuel Fernandez', 6), ('Ali Rahimi', 5), ('Tao Lin', 4),
                                                           ('Cameron Voloshin', 3), ('Gabriele Abbati', 3),
                                                           ('Ehsan Kazemi 0001', 2), ('David P. Woodruff', 2),
                                                           ('Zhenyu Huang', 1), ('Jiancheng Lv', 1),
                                                           ('Hongyuan Zhu', 1), ('Marko Mitrovic', 1),
                                                           ('Silvio Lattanzi', 1), ('Amin Karbasi', 1),
                                                           ('Rina Panigrahy', 1), ('Geoffrey J. Gordon', 1),
                                                           ('Donghwan Lee 0002', 1), ('Niao He', 1),
                                                           ('EManuel Fernandez', 1), ('Tianle Liu', 1),
                                                           ('Michael I. Jordan', 1),
                                                           ('Anirudh Vemula', 1), ('Hoang Minh Le 0002', 1),
                                                           ('Yisong Yue', 1), ('Taisuke Yasuda 0002', 1),
                                                           ('Philippe Wenk', 1),
                                                           ('Andreas Krause 0001', 1), ('Bernhard Scholkopf', 1),
                                                           ('Stefan Bauer', 1)]

        assert statistics_dict['avg_papers_author'] == 1.6
        assert statistics_dict['papers_year_count'] == {2018: 6, 2019: 6}
        assert statistics_dict['avg_papers_year'] == 6.0
        assert statistics_dict['papers_avenue'] == {'AAAI': 3, 'ICML': 9}
        assert "author_centrality" not in statistics_dict.keys()


