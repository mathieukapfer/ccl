import matplotlib.pyplot as plt
import networkx as nx

from ccl_check import check_streams_defined
from ccl_def import functions_run_time, functions_args

def build_fct_graph():
    """ Build DAG with function as node """
    G = nx.DiGraph()
    (table_param_in, table_param_out) = check_streams_defined()

    # fct as node, param as edge:
    # for each parameters, link producer and consumer
    for param in table_param_in:
        for fct in table_param_in[param]:
            G.add_edge(table_param_out[param],  # producer
                       fct)                     # consumer
            ## G.add_weighted_edges_from([(table_param_out[param], fct, functions_run_time[fct])])

    # add root procuder(s) (fct with no input)
    for fct in [x for x in G.nodes() if G.out_degree(x) >= 1 and G.in_degree(x) == 0]:
        G.add_edge("start", fct)

    return G


def build_stream_graph():
    """ Build DAG with stream as node """
    G = nx.DiGraph()

    # param as node, fct as edge:
    # for each function, link output parameter (assuming one) and input parameters
    for (fct, params) in functions_args:
        for param_in in [param for (in_out, param) in params if in_out == 'in']:
            for param_out in [param for (in_out, param) in params if in_out == 'out']:
                G.add_edges_from([(param_in, param_out,
                                   {'weight': functions_run_time[fct],
                                    'fct': fct})])
    # add root parameters
    for param in [x for x in G.nodes() if G.out_degree(x) >= 1 and G.in_degree(x) == 0]:
        G.add_edge("start", param)

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
        # draw critical path in red
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

plt.show(block=False)
