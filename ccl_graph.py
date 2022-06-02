import matplotlib.pyplot as plt
import networkx as nx

from ccl_check import check_streams_defined
from ccl_def import functions_run_time


def build_fct_graph():
    """ Build DAG with function as node """
    G = nx.DiGraph()
    (table_param_in, table_param_out, tmp1, tmp2) = check_streams_defined()

    # fct as node, param as edge
    for param in table_param_in:
        for fct in table_param_in[param]:
            # link fct that produce the param to fct that consume it
            G.add_edge(table_param_out[param], fct)
            ## G.add_weighted_edges_from([(table_param_out[param], fct, functions_run_time[fct])])

    return G


def build_stream_graph():
    """ Build DAG with stream as node """
    G = nx.DiGraph()
    (tmp1, tmp2, table_fct_in, table_fct_out) = check_streams_defined()

    # param as node, fct as edge
    for fct in table_fct_in:
        for param in table_fct_in[fct]:
            ## G.add_edge(param, table_fct_out[fct])
            G.add_weighted_edges_from([(param, table_fct_out[fct], functions_run_time[fct])])
    return G


def draw_graph(G, ax='none', critical_path='none'):
    """ Draw graph"""

    # nx.draw(G, with_labels=True, font_weight='bold')

    # placement thank to graphviz
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

    # draw node
    if (critical_path == 'none'):
        nx.draw_networkx_nodes(G, pos, node_size=200)
    else:
        critical_path = nx.dag_longest_path(G, weight='weight')
        print("Info: Longest Path: ", nx.dag_longest_path_length(G, weight='weight'))
        node_color = ["red" if n in critical_path else "blue" for n in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_color=node_color, node_size=200)
    # draw edge
    nx.draw_networkx_edges(G, pos, width=2)
    # draw label
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

    # figure and axes
    if (ax == 'none'):
        ax = plt.gca()
    # margin
    ax.margins(0.2)


# figure, axis = plt.subplots(1, 1)
plt.figure(1)
draw_graph(build_fct_graph(), critical_path='none')

plt.figure(2)
draw_graph(build_stream_graph(), critical_path='yes')

plt.show()
