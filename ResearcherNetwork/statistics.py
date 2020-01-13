import itertools

from ResearcherNetwork.helper_functions import ParserReader
from collections import Counter
import pandas as pd


class StatisticsGrabber:

    def __init__(self, file):
        self.reader = ParserReader(file)
        # self.reader_iterator = iter(reader)
        self.parsed_lines = []
        for line in self.reader:
            self.parsed_lines.append(line)

    def get_statistics(self):
        statistics_dict = {}
        authors_list = []
        authors_dict = {}
        avg_authors_paper_list = []
        year_list = []
        avenue_list = []
        papers_year_count = {}
        papers_avenue_count = {}
        authors_to_print_dict = {}

        for line in self.parsed_lines:
            avg_authors_paper_list.append(len(line['authors']))
            if line['year'] not in year_list:
                year_list.append(line['year'])
                papers_year_count[line['year']] = 1
            else:
                papers_year_count[line['year']] += 1

            for a in line['authors']:
                if a not in authors_dict.keys():
                    authors_dict[a] = 1
                else:
                    authors_dict[a] += 1
                authors_list.append(a)

            if line['avenue'] not in avenue_list:
                avenue_list.append(line['avenue'])
                papers_avenue_count[line['avenue']] = 1
            else:
                papers_avenue_count[line['avenue']] += 1

        print("# Papers : ", len(self.parsed_lines))
        statistics_dict['n_papers'] = len(self.parsed_lines)  # n.of papers
        print("# Distinct Authors : ", len(set(authors_list)))
        statistics_dict['n_authors'] = len(set(authors_list))  # n.of authors
        print("avg number of authors in a paper: ", str(int(sum(avg_authors_paper_list) / len(self.parsed_lines))))
        statistics_dict['avg_authors_paper'] = int(sum(avg_authors_paper_list) /
                                       len(self.parsed_lines))  # avg authors per paper

        authors_dict_sorted = sorted(authors_dict.items(), key=lambda kv: kv[1], reverse=True)
        if len(year_list) > 1:
            time_span_str = "between " + str(min(year_list)) + " and " + str(max(year_list))
        else:
            time_span_str = "in " + str(year_list[0])
        print("Total number of paper by author (first 5 ones) ", time_span_str)
        i = 0
        avg_papers_author = 0
        authors_to_print = []
        for a, c in authors_dict_sorted:
            avg_papers_author = avg_papers_author + c
            if i <= 4:
                authors_to_print_dict[a] = c
                authors_to_print.append(a+" : "+str(c))

            i += 1
        print(authors_to_print)
        statistics_dict['papers_authors_count'] = authors_to_print_dict  # first 5 authors per n. of papers
        avg_papers_author = avg_papers_author / len(authors_dict_sorted)
        print("avg number of paper per author ", str(round(avg_papers_author, 1)), time_span_str)
        statistics_dict['avg_papers_author'] = round(avg_papers_author, 1)  # avg n. papers per author
        print("#papers per year: ", papers_year_count)
        statistics_dict['papers_year_count'] = papers_year_count  # papers per year
        avg_papers_year = round(sum(papers_year_count.values()) / len(papers_year_count.keys()), 1)
        print("avg number of papers per year: ", avg_papers_year)
        statistics_dict['avg_papers_year'] = avg_papers_year  # avg n. papers per year
        print("#papers per avenue: ", papers_avenue_count)
        statistics_dict['papers_avenue'] = papers_avenue_count  # papers per avenue
        return statistics_dict

    # def get_graph_data(self):
    #     nodes = []
    #     edges = []
    #     for line in self.parsed_lines:
    #         authors = line['authors']
    #         year = line['year']
    #         for a in authors:
    #             if a not in nodes:
    #                 nodes.append(a)
    #         collab = list(itertools.combinations(authors, 2))
    #         for c in collab:
    #             if c not in edges:
    #                 edges.append(c)
    #
    #     print(edges)


if __name__ == "__main__":
    stat = StatisticsGrabber("../tests/resources/parser_out_statistics_test.txt")
    #stat = StatisticsGrabber("resources/parser_out.txt")
    #statistics_dict = stat.get_statistics()
    #stat.get_statistics_v2()
    stat.get_graph_data()