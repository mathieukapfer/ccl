import matplotlib.pyplot as plt
import networkx as nx

from ccl_def import *
from ccl_check import check_streams_defined


def build_fct_graph():
    """ Build DAG with function as node """
    G = nx.DiGraph()
    (table_param_in, table_param_out, table_fct_in, table_fct_out) = check_streams_defined()

    # fct as node, param as edge
    for param in table_param_in:
        for fct in table_param_in[param]:
            # link fct that produce the param to fct that consume it
            G.add_edge(table_param_out[param], fct)

    #pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility
    #edge_labels = nx.get_edge_attributes(G, "label")
    #nx.draw_networkx_edge_labels(G, pos, edge_labels)

    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()

def build_stream_graph():
    """ Build DAG with stream as node """
    G = nx.DiGraph()
    (table_param_in, table_param_out, table_fct_in, table_fct_out) = check_streams_defined()

    # param as node, fct as edge
    for fct in table_fct_in:
        for param in table_fct_in[fct]:
            G.add_edge(param, table_fct_out[fct])

    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()
