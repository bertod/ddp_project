import itertools
from ResearcherNetwork.graph import GraphBuilder
from ResearcherNetwork.helper_functions import ParserReader
from collections import Counter


class StatisticsGrabber:

    def __init__(self, file, output_file_path="resources/statistics_out.txt"):
        self.file = file
        self.output_file_path = output_file_path
        self.reader = ParserReader(self.file)
        self.graph_builder = None

    def get_statistics(self, graph_builder: GraphBuilder = None):
        self.graph_builder = graph_builder
        statistics_dict = {}
        authors_list = []
        authors_dict = {}
        avg_authors_paper_list = []
        year_list = []
        avenue_list = []
        papers_year_count = {}
        papers_avenue_count = {}
        n_papers = 0
        for line in self.reader:
            n_papers += 1
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

        # print("# Papers : ", n_papers)
        statistics_dict['n_papers'] = n_papers  # n.of papers
        # print("# Distinct Authors : ", len(set(authors_list)))
        statistics_dict['n_authors'] = len(set(authors_list))  # n.of authors
        # print("avg number of authors in a paper: ", str(int(sum(avg_authors_paper_list) / n_papers)))
        statistics_dict['avg_authors_paper'] = int(sum(avg_authors_paper_list) /
                                                   n_papers)  # avg authors per paper

        authors_dict_sorted = sorted(authors_dict.items(), key=lambda kv: kv[1], reverse=True)
        if len(year_list) > 1:
            time_span_str = "between " + str(min(year_list)) + " and " + str(max(year_list))
        else:
            time_span_str = "in " + str(year_list[0])
        # print("Total number of paper by author (first 5 ones) ", time_span_str)
        avg_papers_author = 0
        for a, c in authors_dict_sorted:
            avg_papers_author = avg_papers_author + c
        statistics_dict['papers_authors_count'] = authors_dict_sorted
        avg_papers_author = avg_papers_author / len(authors_dict_sorted)
        # print("avg number of paper per author ", str(round(avg_papers_author, 1)), time_span_str)
        statistics_dict['avg_papers_author'] = round(avg_papers_author, 1)  # avg n. papers per author
        # print("#papers per year: ", papers_year_count)
        statistics_dict['papers_year_count'] = papers_year_count  # papers per year
        avg_papers_year = round(sum(papers_year_count.values()) / len(papers_year_count.keys()), 1)
        # print("avg number of papers per year: ", avg_papers_year)
        statistics_dict['avg_papers_year'] = avg_papers_year  # avg n. papers per year
        # print("#papers per avenue: ", papers_avenue_count)
        statistics_dict['papers_avenue'] = papers_avenue_count  # papers per avenue

        if isinstance(self.graph_builder, GraphBuilder):
            statistics_dict['author_centrality'] = self.get_graph_data()
        # f_out = open("resources/statistics_out.txt", "w")
        f_out = open(self.output_file_path, "w")
        print(statistics_dict, file=f_out)
        f_out.close()
        return statistics_dict

    def get_graph_data(self):
        nodes = self.graph_builder.nodes
        edges = self.graph_builder.edges
        egdes_list = []
        centrality_dict = {}
        for t in edges:
            egdes_list += list(t)
        counts = Counter(egdes_list)
        for a in nodes:
            if a not in counts.keys():
                counts[a] = 0
            centrality_dict[a] = counts[a] / (len(nodes) - 1)
        # print(centrality_dict)
        return centrality_dict
