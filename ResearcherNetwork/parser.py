# from __future__ import annotations
from abc import ABC, abstractmethod
from unidecode import unidecode


class ParserCreator:

    @abstractmethod
    def factory_method(self):
        pass

    def run_fast_iter(self, context, collab=[u'inproceedings', u'article'], *args, **kwargs):
        product = self.factory_method()
        product.fast_iter(context, product.process_element, collab, *args, **kwargs)

    def run_process_element(self, elem, fout):
        product = self.factory_method()
        product.process_element(elem, fout)


class Parser(ABC):

    @abstractmethod
    def fast_iter(self, context, func, collab=[u'inproceedings', u'article'], *args, **kwargs):
        pass

    @abstractmethod
    def process_element(self, elem, **kwargs):
        pass


class ConcreteParserDblp(Parser):

    def fast_iter(self, context, func, collab=[u'inproceedings', u'article'], *args, **kwargs):
        """
        :param context: piece of XML file to parse
        :param func: function used to write the output file
        :param collab: type of paper to keep
        :param args: other arguments like out put file reference
        :param kwargs: other arguments
        :return:

        The function parse pieces of XML closed into the same tag (e.g. inproceedings)
        representing the paper. It parses in order to obtain authors,
        name of avenue, year of pub and title.

        """
        # xml categories
        author_array = []
        title = ''
        journal = ''
        year = 0
        years_list = kwargs['years']
        tag = ''
        book = ''
        collaborations = collab
        # read chunk line by line
        # we focus author and title
        for event, elem in context:
            if elem.tag in collaborations and event == "start":
                tag = elem.tag
                # print(elem.tag, event)

            if elem.tag == 'author' and event == "start":
                if elem.text:
                    author_array.append(unidecode(elem.text))

            if elem.tag == 'title' and event == "start":
                if elem.text:
                    title = unidecode(elem.text)
                    title = title.strip()

            if elem.tag == 'journal' and event == "start":
                if elem.text:
                    journal = unidecode(elem.text)

            if elem.tag == 'year' and event == "start":
                if elem.text:
                    year = int(elem.text)

            if elem.tag == 'booktitle' and event == 'start':
                book = unidecode(elem.text)

            if elem.tag in collaborations and year in years_list and event == "end":
                if len(author_array) is not 0 and title is not '':
                    # rejected paper has no author or title
                    # it should be check
                    print(elem.tag, journal, book)

                    authors = ""
                    for a in author_array:
                        authors += a + "||"
                        # write into kv file
                    authors += str(year) + "||"
                    if elem.tag == "article":
                        authors += journal + "||"
                    else:
                        authors += book.upper() + "||"
                    func(authors + title, *args, **kwargs)

                    year = 0
                    journal = ''
                    title = ''
                    book = ''
                    del author_array[:]

            if elem.tag == tag and event == 'end':
                tag = ''
                year = 0
                journal = ''
                title = ''
                book = ''
                del author_array[:]

            if event == "end" and elem.tag != "html":
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        # clear chunks

    # @func: process_element
    # @param elem : parsed data of chunk
    # @param fout : file name to write
    # @desc: It is handler to write content. just write content to file
    def process_element(self, elem, **kwargs):
        """
        :param elem: output row to be written
        :param fout: output file reference
        :return:
        """
        print("writing ... " + elem)
        print(elem, file=kwargs["fout"])


class ConcreteParserDblpCreator(ParserCreator):

    def factory_method(self) -> ConcreteParserDblp:
        return ConcreteParserDblp()
