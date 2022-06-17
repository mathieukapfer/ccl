import matplotlib.pyplot as plt
import networkx as nx

from ccl_parser.ccl_graph2 import build_stream_graph, write_dot_graph
from ccl_parser.ccl_parse2 import ccl_file_parser

from ccl_graph.ccl_graph_viewer import draw_graph


# build graph from ccl file
def main(filename):
    """
    Build graph from ccl file.

    Output
       - out_ccl_raw.dot : graph in graphviz format (use xdot as viewer)
       - matplotlib window with networkx graph representation

    """
    (G, nodes_name_dict) = build_stream_graph(ccl_file_parser(filename))

    # color critical path
    critical_path = nx.dag_longest_path(G, weight='weight')
    for node in critical_path:
        G.nodes[node]['color'] = 'red'

    # draw with matplotlib
    draw_graph(G, critical_path='no')
    plt.show(block=False)

    # save graph in dot format
    # nx.relabel_nodes(G, nodes_name_dict, copy=False)

    write_dot_graph(G)


filename = 'CCL_file_2cblk.txt'
# filename = 'ccl_file_12May22.txt'

main(filename)
