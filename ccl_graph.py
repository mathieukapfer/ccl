import matplotlib.pyplot as plt
import networkx as nx

from ccl_check import check_streams_defined


def build_fct_graph():
    """ Build DAG with function as node """
    G = nx.DiGraph()
    (table_param_in, table_param_out, tmp1, tmp2) = check_streams_defined()

    # fct as node, param as edge
    for param in table_param_in:
        for fct in table_param_in[param]:
            # link fct that produce the param to fct that consume it
            G.add_edge(table_param_out[param], fct)
    return G


def build_stream_graph():
    """ Build DAG with stream as node """
    G = nx.DiGraph()
    (tmp1, tmp2, table_fct_in, table_fct_out) = check_streams_defined()

    # param as node, fct as edge
    for fct in table_fct_in:
        for param in table_fct_in[fct]:
            G.add_edge(param, table_fct_out[fct])

    return G


def draw_graph(G, ax='none'):
    """ Draw graph"""

    # nx.draw(G, with_labels=True, font_weight='bold')

    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    nx.draw_networkx_nodes(G, pos, node_size=200)
    nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
    if (ax == 'none'):
        ax = plt.gca()

    ax.margins(0.2)


# figure, axis = plt.subplots(1, 1)
plt.figure(1)
draw_graph(build_fct_graph())

plt.figure(2)
draw_graph(build_stream_graph())

plt.show()
