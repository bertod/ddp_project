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
        self.file = file
        self.lines = []
        self.pointer = 0

    def __iter__(self):
        f = open(self.file, 'r')
        self.lines = f.readlines()
        f.close()
        return self

    def __next__(self):
        try:
            line = self.lines[self.pointer]
        except:
            raise StopIteration
        tmp = self.__parse_line(line)
        self.pointer += 1
        return tmp

    def __parse_line(self, line):
        line = remove_control_characters(line)
        row_list = line.split("||")
        authors = row_list[:-3]
        year = int(row_list[-3])
        avenue = row_list[-2]
        title = row_list[-1]
        tmp = {'authors': authors, 'year': year, 'avenue': avenue, 'title': title}
        return tmp
