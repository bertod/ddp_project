import unicodedata

import pytest
import os
from lxml import etree
from ResearcherNetwork.parser import ConcreteParserDblpCreator
from ResearcherNetwork.helper_functions import remove_control_characters


class TestParser:

    def setup_method(self):
        self.parser = ConcreteParserDblpCreator()

    def test_write_to_file(self):
        test_string = "This is a test string"
        fout = open('tests/resources/test.txt', 'w')
        self.parser.run_process_element(test_string, fout)
        fout.close()
        with open('tests/resources/test.txt', 'r') as f:
            assert remove_control_characters(f.read()) == test_string
        os.remove('tests/resources/test.txt')

    def test_parse(self):
        expected = "Dev Team 1||Dev Team 2||2019||XML_TEST||Test XML file"
        fout = open('tests/resources/xml_out.txt', 'w')
        context = etree.iterparse("tests/resources/test.xml", load_dtd=True, html=True, events=["start", "end"])
        self.parser.run_fast_iter(context, self.parser.run_process_element, fout=fout)
        fout.close()
        with open('tests/resources/xml_out.txt', 'r') as f:
            assert remove_control_characters(f.read()) == expected
        os.remove('tests/resources/xml_out.txt')

    def test_parse_multiline(self):
        expected = "Dev Team 1||Dev Team 2||2019||XML_TEST||Append\n"\
                   "Dev Team 1||Dev Team 2||2019||XML_TEST||Append\n"
        fout = open('tests/resources/xml_out.txt', 'w')
        context = etree.iterparse("tests/resources/test_append.xml", load_dtd=True, html=True, events=["start", "end"])
        self.parser.run_fast_iter(context, self.parser.run_process_element, fout=fout)
        fout.close()
        fout = open('tests/resources/xml_out.txt', 'a')
        context = etree.iterparse("tests/resources/test_append.xml", load_dtd=True, html=True, events=["start", "end"])
        self.parser.run_fast_iter(context, self.parser.run_process_element, fout=fout)
        fout.close()
        with open('tests/resources/xml_out.txt', 'r') as f:
            assert f.read() == expected
        os.remove('tests/resources/xml_out.txt')
