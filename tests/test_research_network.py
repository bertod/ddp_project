import shutil

import pytest
import os
import research_network as rn


class TestResearchNetwork:

    def test_main(self):
        scraper_output_path = "tests/resources/"
        links_file_path = "tests/resources/links.csv"
        output_file_path = "tests/resources/parser_out.txt"
        f_expected = open("tests/resources/expected_output.txt", "r")
        expected = f_expected.read()
        rn.run(scraper_output_path, links_file_path, output_file_path)
        f = open(output_file_path, "r")
        content = f.read()
        assert expected == content
        f_expected.close()
        f.close()
        os.remove(output_file_path)
        shutil.rmtree("tests/resources/ai")
