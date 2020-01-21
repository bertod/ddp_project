from ResearcherNetwork.graph import GraphBuilder
from ResearcherNetwork.helper_functions import ParserReader
from collections import Counter


class StatisticsGrabber:

    def __init__(self, file: str, output_file_path: str = "resources/statistics_out.txt"):
        self.file = file
        self.output_file_path = output_file_path
        self.reader = ParserReader(self.file)
        self.graph_builder = None

    def get_statistics(self, graph_builder: GraphBuilder = None) -> dict:
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

        tmp_dict = {'title': "Total Number of Papers", 'value': n_papers}
        statistics_dict['n_papers'] = tmp_dict  # n.of papers
        tmp_dict = {'title': "Total Number of Authors", 'value': len(set(authors_list))}
        statistics_dict['n_authors'] = tmp_dict  # n.of authors
        tmp_dict = {'title': "Average Number of Authors per Paper", 'value': int(sum(avg_authors_paper_list) /
                                                                                 n_papers)}
        statistics_dict['avg_authors_paper'] = tmp_dict

        authors_dict_sorted = sorted(authors_dict.items(), key=lambda kv: kv[1], reverse=True)
        avg_papers_author = 0
        for a, c in authors_dict_sorted:
            avg_papers_author = avg_papers_author + c

        tmp_dict = {'title': "Number Papers for each Author", 'value': authors_dict_sorted}
        statistics_dict['papers_authors_count'] = tmp_dict
        avg_papers_author = avg_papers_author / len(authors_dict_sorted)
        tmp_dict = {'title': "Average number of Papers per Author", 'value': int(avg_papers_author)}
        statistics_dict['avg_papers_author'] = tmp_dict  # avg n. papers per author
        tmp_dict = {'title': "Number of Papers per year", 'value': papers_year_count}
        statistics_dict['papers_year_count'] = tmp_dict  # papers per year
        avg_papers_year = round(sum(papers_year_count.values()) / len(papers_year_count.keys()), 1)
        tmp_dict = {'title': "Average Number of Papers per year", 'value': int(avg_papers_year)}
        statistics_dict['avg_papers_year'] = tmp_dict  # avg n. papers per year
        tmp_dict = {'title': "Number of Papers per Avenue", 'value': papers_avenue_count}
        statistics_dict['papers_avenue'] = tmp_dict  # papers per avenue

        if isinstance(self.graph_builder, GraphBuilder):
            tmp_dict = {'title': "Centrality measure for each author", 'value': self.get_graph_data()}
            statistics_dict['author_centrality'] = tmp_dict
        f_out = open(self.output_file_path, "w")
        print(statistics_dict, file=f_out)
        f_out.close()
        return statistics_dict

    def get_graph_data(self) -> dict:
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
            centrality_dict[a] = round((counts[a] / (len(nodes) - 1)), 5)
        # print(centrality_dict)
        return centrality_dict
