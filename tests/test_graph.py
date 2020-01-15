import pytest
import os
import itertools
from ResearcherNetwork.graph import GraphBuilder


class TestGraph:

    def setup_method(self):
        self.g = GraphBuilder("tests/resources/graph_test.txt", output="tests/resources/", authors=['Roberto Navigli'])
        self.expected_authors = ['Giovanni Amendola', 'Francesco Ricca', 'Miroslaw Truszczynski', 'Tommaso Pasini',
                        'Roberto Navigli']
        self.expected_edges = [('Giovanni Amendola', 'Francesco Ricca'), ('Giovanni Amendola', 'Miroslaw Truszczynski'),
                               ('Francesco Ricca', 'Miroslaw Truszczynski'), ('Tommaso Pasini', 'Roberto Navigli')]
        self.expected_networkx_file = "tests/resources/networkx_graph.png"
        self.expected_gt_file = "tests/resources/graphtool_graph.png"
        self.expected_bokeh_file = "tests/resources/interactive_graph_bokeh.html"

    def test_parsed_data(self):
        assert self.g.nodes == self.expected_authors
        assert self.g.edges == self.expected_edges

    def test_networkx(self):
        self.g.build_networkx(bokeh=False)
        assert self.g.networkx_graph is not None
        assert self.g.networkx_graph_bokeh is None
        assert self.g.graphtool_graph is None
        assert list(self.g.networkx_graph.nodes) == self.expected_authors
        assert list(self.g.networkx_graph.edges) == self.expected_edges

    def test_graph_tool(self):
        self.g.build_graphtool()
        assert self.g.networkx_graph is None
        assert self.g.networkx_graph_bokeh is None
        assert self.g.graphtool_graph is not None
        # Graph Tool uses its own internal naming for nodes, hence we keep track of the translation with two
        # dictionaries, conv and conv_rev. We check that the number of nodes and edges is the same as what we expect
        # and that all the authors are present as keys in conv.
        assert len(list(self.g.graphtool_graph.vertices())) == len(self.expected_authors)
        assert len(list(self.g.graphtool_graph.edges())) == len(self.expected_edges)
        assert len(list(self.g.conv.keys())) == len(self.expected_authors)
        for author in self.expected_authors:
            assert author in self.g.conv.keys()

    def test_bokeh(self):
        self.g.build_networkx(bokeh=True)
        assert self.g.networkx_graph is None
        assert self.g.networkx_graph_bokeh is not None
        assert self.g.graphtool_graph is None
        assert list(self.g.networkx_graph_bokeh.nodes) == self.expected_authors
        assert list(self.g.networkx_graph_bokeh.edges) == self.expected_edges

    def test_networkx_wanted(self):
        self.g.build_networkx()
        assert list(self.g.networkx_labels.keys()) == ['Roberto Navigli']
        assert self.g.networkx_labels['Roberto Navigli'] == 'Roberto Navigli'

    def test_bokeh_wanted(self):
        self.g.build_networkx(bokeh=True)
        assert self.g.networkx_graph_bokeh.nodes['Roberto Navigli']['name'] == 'Roberto Navigli'
        assert self.g.networkx_graph_bokeh.nodes['Roberto Navigli']['node_color'] == 'red'
        assert self.g.networkx_graph_bokeh.nodes['Roberto Navigli']['size'] == 20

    def test_gt_wanted(self):
        self.g.draw_with_graphtool()
        assert self.g.v_label[self.g.conv['Roberto Navigli']] == 'Roberto Navigli'


    def test_snap_networkx(self):
        self.g.snap_with_networkx()
        assert os.path.isfile(self.expected_networkx_file)
        os.remove(self.expected_networkx_file)

    def test_snap_graphtool(self):
        self.g.snap_with_graphtool()
        assert os.path.isfile(self.expected_gt_file)
        os.remove(self.expected_gt_file)

    def test_draw_bokeh(self):
        self.g.draw_with_bokeh()
        assert os.path.isfile(self.expected_bokeh_file)
        os.remove(self.expected_bokeh_file)


