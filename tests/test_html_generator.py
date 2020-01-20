import pytest
from ResearcherNetwork.graph import GraphBuilder
from ResearcherNetwork.html_generator import StaticHtml
from ResearcherNetwork.statistics import StatisticsGrabber
from ResearcherNetwork.helper_functions import remove_control_characters


class TestHtmlGenerator:
    def setup_method(self):
        self.parser_output_file_path = "tests/resources/parser_out_statistics_test.txt"
        # self.parser_output_file_path = "tests/resources/parser_out.txt"
        self.scraper_output_path = "tests/resources/"
        self.html_generator = StaticHtml(datasource="dblp",
                                         html_output_file="static.html", year_list=[2016], avenue_list=['DDPJ'])

    def test_html_generation(self):
        g = GraphBuilder(self.parser_output_file_path, authors=['Gabriele Abbati'], output=self.scraper_output_path)
        g.snap_with_networkx()
        s = StatisticsGrabber(self.parser_output_file_path)
        statistics_dict = s.get_statistics(g)
        self.html_generator.write_statistics(statistics_dict)
        self.html_generator.add_graph_image(lib_name="networkx", output_path=g.output_path)
        self.html_generator.close_page()
        gen_html_expected_file = open("tests/resources/html_generator_expected.html", "r")
        gen_html_expected = gen_html_expected_file.read()
        gen_html_expected = remove_control_characters(gen_html_expected)
        gen_html_real_file = open(self.html_generator.html_output_file, "r")
        gen_html_real = remove_control_characters(gen_html_real_file.read())
        assert gen_html_real == gen_html_expected
