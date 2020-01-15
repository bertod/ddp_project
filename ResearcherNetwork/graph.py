import itertools
import matplotlib.pyplot as plt
import networkx as nx
# noinspection PyUnresolvedReferences
from helper_functions import ParserReader
from graph_tool.all import *

from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool
from bokeh.models.graphs import from_networkx


class GraphBuilder:

    def __init__(self, parser_input, authors=[], output="../resources/"):
        self.nodes = []
        self.edges = []
        self.wanted_authors = authors
        self.input_file = ParserReader(parser_input)
        self.networkx_graph = None
        self.networkx_graph_layout = None
        self.networkx_labels = {}
        self.graphtool_graph = None
        self.networkx_graph_bokeh = None
        self.networkx_graph_bokeh_layout = None
        self.conv = {}
        self.conv_rev = {}
        self.output_path = output
        self.v_label = None

        for row in self.input_file:
            authors = row['authors']
            for a in authors:
                if a not in self.nodes:
                    self.nodes.append(a)
            collab = list(itertools.combinations(authors, 2))
            for c in collab:
                if c not in self.edges:
                    self.edges.append(c)

    def build_networkx(self, bokeh=False):
        if not bokeh:
            self.networkx_graph = nx.Graph()
            for author in self.nodes:
                self.networkx_graph.add_node(author)
                if author in self.wanted_authors:
                    self.networkx_labels[author] = author
            self.networkx_graph.add_edges_from(self.edges)
            self.networkx_graph_layout = nx.spring_layout(self.networkx_graph)
        else:
            self.networkx_graph_bokeh = nx.Graph()
            for author in self.nodes:
                if author in self.wanted_authors:
                    self.networkx_graph_bokeh.add_node(author, name=author, node_color='red', size=20)
                else:
                    self.networkx_graph_bokeh.add_node(author, name=author, node_color='blue', size=10)
            self.networkx_graph_bokeh.add_edges_from(self.edges)
            self.networkx_graph_bokeh_layout = nx.spring_layout(self.networkx_graph_bokeh)

    def build_graphtool(self):
        self.graphtool_graph = Graph(directed=False)
        for a in self.nodes:
            c = self.graphtool_graph.add_vertex()
            self.conv[a] = c
            self.conv_rev[c] = a
        for e in self.edges:
            self.graphtool_graph.add_edge(self.conv[e[0]], self.conv[e[1]])

    def snap_with_networkx(self):
        if self.networkx_graph is None:
            self.build_networkx()
        plt.figure(figsize=(20,20))
        nx.draw(self.networkx_graph, pos=self.networkx_graph_layout,
                with_labels=False, node_size=10, label="NetworkX Graph")
        for author in self.wanted_authors:
            nx.draw_networkx_nodes(self.networkx_graph, pos=self.networkx_graph_layout,
                                   nodelist=[author], node_color='r', node_size=100, edgecolors=['black'])
        nx.draw_networkx_labels(self.networkx_graph, pos=self.networkx_graph_layout,
                                labels=self.networkx_labels, font_size=7, font_color='black')
        plt.savefig("{}networkx_graph.png".format(self.output_path))
        print("Image saved at {}networkx_graph.png".format(self.output_path))

    def snap_with_graphtool(self):
        if self.graphtool_graph is None:
            self.build_graphtool()
        graph_draw(self.graphtool_graph, output_size=(1920, 1080), output="{}graphtool_graph.png".format(self.output_path))
        print("Image saved at {}graphtool_graph.png".format(self.output_path))

    def draw_with_networkx(self):
        if self.networkx_graph is None:
            self.build_networkx()
        nx.draw(self.networkx_graph, pos=self.networkx_graph_layout,
                with_labels=False, node_size=10, label="NetworkX Graph")
        for author in self.wanted_authors:
            nx.draw_networkx_nodes(self.networkx_graph, pos=self.networkx_graph_layout,
                                   nodelist=[author], node_color='r', node_size=100, edgecolors=['black'])
        nx.draw_networkx_labels(self.networkx_graph, pos=self.networkx_graph_layout,
                                labels=self.networkx_labels, font_size=7, font_color='black')
        plt.show()

    def draw_with_graphtool(self):
        if self.graphtool_graph is None:
            self.build_graphtool()
        self.v_label = self.graphtool_graph.new_vertex_property("string")
        for a in self.nodes:
            if a in self.wanted_authors:
                self.v_label[self.conv[a]] = self.conv_rev[self.conv[a]]
        graph_tool.draw.interactive_window(self.graphtool_graph, vertex_text=self.v_label, vertex_font_size=6,
                                           geometry=(1920, 1080))

    def draw_with_bokeh(self):
        self.build_networkx(bokeh=True)
        plot = Plot(plot_width=1820, plot_height=880,
                    x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
        plot.title.text = "Researcher Network Graph"

        node_hover_tool = HoverTool(tooltips=[("Name", "@name")])
        plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

        graph_renderer = from_networkx(self.networkx_graph_bokeh, self.networkx_graph_bokeh_layout, scale=1, center=(0, 0))

        graph_renderer.node_renderer.glyph = Circle(size='size', fill_color='node_color')
        graph_renderer.edge_renderer.glyph = MultiLine(line_alpha=0.8, line_width=1)
        plot.renderers.append(graph_renderer)

        output_file("{}interactive_graph_bokeh.html".format(self.output_path))
        show(plot)
