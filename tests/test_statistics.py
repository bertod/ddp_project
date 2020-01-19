import pytest
from ResearcherNetwork.helper_functions import remove_control_characters
from ResearcherNetwork.statistics import StatisticsGrabber
from ResearcherNetwork.graph import GraphBuilder


class TestStatistics:
    def setup_method(self):
        self.statistics_grabber = StatisticsGrabber("tests/resources/parser_out_statistics_test.txt",
                                                    "tests/resources/statistics_out.txt")

    def test_get_statistics(self):
        statistics_dict = self.statistics_grabber.get_statistics()
        assert statistics_dict['n_papers']['value'] == 12
        assert statistics_dict['n_authors']['value'] == 28
        assert statistics_dict['avg_authors_paper']['value'] == 3
        assert statistics_dict['papers_authors_count']['value'] == [('Manuel Fernandez', 6), ('Ali Rahimi', 5),
                                                                    ('Tao Lin', 4),
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
                                                                    ('Andreas Krause 0001', 1),
                                                                    ('Bernhard Scholkopf', 1),
                                                                    ('Stefan Bauer', 1)]

        assert statistics_dict['avg_papers_author']['value'] == 1
        assert statistics_dict['papers_year_count']['value'] == {2018: 6, 2019: 6}
        assert statistics_dict['avg_papers_year']['value'] == 6
        assert statistics_dict['papers_avenue']['value'] == {'AAAI': 3, 'ICML': 9}
        assert "author_centrality" not in statistics_dict.keys()

    def test_get_graph_statistics(self):
        g = GraphBuilder("tests/resources/parser_out_statistics_test.txt", output="tests/resources/", authors=[])
        statistics_dict = self.statistics_grabber.get_statistics(graph_builder=g)
        assert statistics_dict['n_papers']['value'] == 12
        assert statistics_dict['n_authors']['value'] == 28
        assert statistics_dict['avg_authors_paper']['value'] == 3
        assert statistics_dict['papers_authors_count']['value'] == [('Manuel Fernandez', 6), ('Ali Rahimi', 5),
                                                                    ('Tao Lin', 4),
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
                                                                    ('Andreas Krause 0001', 1),
                                                                    ('Bernhard Scholkopf', 1),
                                                                    ('Stefan Bauer', 1)]

        assert statistics_dict['avg_papers_author']['value'] == 1
        assert statistics_dict['papers_year_count']['value'] == {2018: 6, 2019: 6}
        assert statistics_dict['avg_papers_year']['value'] == 6
        assert statistics_dict['papers_avenue']['value'] == {'AAAI': 3, 'ICML': 9}
        assert "author_centrality" in statistics_dict.keys()
        assert statistics_dict['author_centrality']['value'] == {'Manuel Fernandez': 0.56,
                                                                 'Zhenyu Huang': 0.15,
                                                                 'Jiancheng Lv': 0.15,
                                                                 'Hongyuan Zhu': 0.15,
                                                                 'Ali Rahimi': 0.63,
                                                                 'Ehsan Kazemi 0001': 0.26,
                                                                 'Marko Mitrovic': 0.15,
                                                                 'Silvio Lattanzi': 0.15,
                                                                 'Amin Karbasi': 0.15,
                                                                 'Tao Lin': 0.37,
                                                                 'Rina Panigrahy': 0.11,
                                                                 'David P. Woodruff': 0.19,
                                                                 'Geoffrey J. Gordon': 0.11,
                                                                 'Donghwan Lee 0002': 0.04,
                                                                 'Niao He': 0.04,
                                                                 'Cameron Voloshin': 0.26,
                                                                 'EManuel Fernandez': 0.07,
                                                                 'Gabriele Abbati': 0.3,
                                                                 'Tianle Liu': 0.11,
                                                                 'Michael I. Jordan': 0.11,
                                                                 'Anirudh Vemula': 0.11,
                                                                 'Hoang Minh Le 0002': 0.07,
                                                                 'Yisong Yue': 0.07,
                                                                 'Taisuke Yasuda 0002': 0.07,
                                                                 'Philippe Wenk': 0.19,
                                                                 'Andreas Krause 0001': 0.19,
                                                                 'Bernhard Scholkopf': 0.19,
                                                                 'Stefan Bauer': 0.19}

