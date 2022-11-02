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
    plt.show(block=False)

    # write dot file
    write_dot_graph(G)


# filename = 'CCL_file_2cblk.txt'
# filename = 'ccl_file_12May22.txt'
# filename = 'CCL_file_orig.txt'
# filename = 'CCL_file_pool.txt'
# filename = "CCL_file_ldpc_exec_pool.txt"
# filename = "data/ToKalray05JUL22/CCL_file.txt"  # working memory
# filename = "data/ToKalray07JUL22/CCL_file.txt"    # Tx
# filename = "data/20JUL22_Cirrus360/CCL_file.txt"    # Tx fixed
# filename = "data/CCL_file_extract.txt"
# filename = "data/20JUL22_Cirrus360/CCL_file.txt"    # Tx fixed
filename = "data/ToKalray04AUG22/CCL_file_RxTx.txt"

ccl_to_graph(filename)
