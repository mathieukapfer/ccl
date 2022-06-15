import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(G, ax='none', critical_path='none'):
    """ Draw graph"""

    # nx.draw(G, with_labels=True, font_weight='bold')

    # placement thank to graphviz
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

    # draw node
    if (critical_path == 'none'):
        nx.draw_networkx_nodes(G, pos, node_size=300)
    else:
        # draw critical path in red
        critical_path = nx.dag_longest_path(G, weight='weight')
        print("Info: Longest Path: ", nx.dag_longest_path_length(G, weight='weight'))
        print(critical_path)
        node_color = ["red" if n in critical_path else "blue" for n in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_color=node_color, node_size=300)

    # draw edge
    nx.draw_networkx_edges(G, pos, width=2)

    # draw label
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

    # figure and axes
    if ax == 'none':
        ax = plt.gca()

    # margin
    ax.margins(0.2)
