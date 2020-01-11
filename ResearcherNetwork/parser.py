from lxml import etree
from unidecode import unidecode


class Parser:

    def __init__(self, collab=[u'inproceedings', u'article'],
                 years=[2016, 2017, 2018, 2019],
                 conferences=[u'ijcai', u'aaai', u'icml'],
                 books=[u'IJCAI', u'AAAI', u'ICML'],
                 journals=[u'J. Artif. Intell. Res.', u'Journal of Machine Learning Research', u'Artif. Intell.']):
        self.collaborations = collab
        self.years = years
        self.confs = conferences
        self.books = books
        self.journals = journals

    def fast_iter(self, context, func, *args, **kwargs):
        # xml categories
        author_array = []
        title = ''
        journal = ''
        year = 0
        tag = ''
        book = ''

        # read chunk line by line
        # we focus author and title
        for event, elem in context:

            if elem.tag in self.collaborations and event == "start":
                tag = elem.tag
                print(elem.tag, event)

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

            if elem.tag in self.collaborations and year in self.years and (
                    journal in self.journals or book in self.books) and event == "end":
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
                # print(elem.tag,event)

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
    def process_element(self, elem, fout):
        print("writing ... " + elem)
        print(elem, file=fout)
