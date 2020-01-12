import unicodedata


def remove_control_characters(s):
    """
    Helper Function for removing control chars from strings
    before comparison
    :param s:
    :return:
    """
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")


class ParserReader:

    def __init__(self, file):
        self.f = open(file, 'r')
        self.lines = []
        self.pointer = 0

    def __iter__(self):
        self.lines = self.f.readlines()
        return self

    def __next__(self):
        line = self.lines[self.pointer]
        tmp = self.parse_line(line)
        self.pointer += 1
        if self.pointer >= len(self.lines):
            raise StopIteration
        return tmp

    def parse_line(self, line):
        line = remove_control_characters(line)
        row_list = line.split("||")
        authors = row_list[:-3]
        year = int(row_list[-3])
        avenue = row_list[-2]
        title = row_list[-1]
        tmp = {'authors': authors, 'year': year, 'avenue': avenue, 'title': title}
        return tmp
