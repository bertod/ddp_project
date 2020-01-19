import shutil
import mock
import pytest
import os
import research_network as rn
from ResearcherNetwork.statistics import StatisticsGrabber
from ResearcherNetwork.graph import GraphBuilder

import sys
from contextlib import contextmanager
from io import StringIO


@contextmanager
def replace_stdin(target):
    orig = sys.stdin
    sys.stdin = target
    yield
    sys.stdin = orig


class TestResearchNetwork:

    def test_main(self):
        with replace_stdin(StringIO("1\n1\nq")):
            scraper_output_path = "tests/resources/"
            links_file_path = "tests/resources/links.csv"
            output_file_path = "tests/resources/parser_out.txt"
            f_expected = open("tests/resources/expected_output.txt", "r")
            expected = f_expected.read()
            rn.run(scraper_output_path, links_file_path, output_file_path)
            f = open(output_file_path, "r")
            content = f.read()
            assert expected == content
            assert os.path.isfile(scraper_output_path + "/statistics_out.txt")
            assert os.path.isfile(scraper_output_path + "/networkx_graph.png")
            os.remove(scraper_output_path + "/statistics_out.txt")
            os.remove(scraper_output_path + "/networkx_graph.png")
            f_expected.close()
            f.close()
            os.remove(output_file_path)
            shutil.rmtree("tests/resources/ai")

