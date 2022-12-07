import argparse
import logging

import matplotlib.pyplot as plt

from ccl_parser.ccl_graph2 import build_stream_graph, write_dot_graph
from ccl_parser.ccl_parse2 import ccl_file_parser

from ccl_graph.ccl_graph_viewer import draw_graph


# build graph from ccl file
def ccl_to_graph(filename):
    """
    Build graph from ccl file.

    Output
       - out_ccl_raw.dot : graph in graphviz format (use xdot as viewer)
       - matplotlib window with networkx graph representation

    """

    # parse ccl file: produce nodes dictionnary
    nodes = ccl_file_parser(filename)

    # build networkx graphw from nodes dictionnary
    G = build_stream_graph(nodes)

    # draw networkx graph with matplotlib
    draw_graph(G, critical_path='yes')
    # plt.show(block=False)
    plt.show()

    # write dot file
    write_dot_graph(G)


if __name__ == "__main__":

    # ccl_to_graph(sys.argv[1])

    # declare parser
    parser = argparse.ArgumentParser(description='Display CCL file diagram')
    parser.add_argument('filename', nargs=1, help='The CCL file to parse')
    parser.add_argument('-v', dest='verbose', action='store_const',
                        const=1, default=0, help='enable verbose mode (including backtrace)')

    # parse
    args = parser.parse_args()

    if args.verbose == 1:
        logging.basicConfig(level=logging.DEBUG)

    # go !
    ccl_to_graph(args.filename[0])
