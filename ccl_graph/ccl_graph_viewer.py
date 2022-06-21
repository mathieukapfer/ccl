import matplotlib.pyplot as plt
import networkx as nx


def colorize_path(G, path, color):
    """
    Color critical path of G in red
    """

    # colorize graphviz (use label 'color')
    # - node
    for node in path:
        G.nodes[node]['color'] = color

    # - edges
    for index in range(0, len(path)-1):
        G.edges[path[index], path[index + 1]]['color'] = 'red'


def draw_graph(G, ax='none', critical_path='no'):
    """ Draw networkx graph"""

    # nx.draw(G, with_labels=True, font_weight='bold')

    # placement thank to graphviz
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

    # draw node
    if (critical_path == 'no'):
        nx.draw_networkx_nodes(G, pos, node_size=300)
    else:
        critical_path = nx.dag_longest_path(G, weight='weight')
        print("Info: Longest Path: ",
              nx.dag_longest_path_length(G, weight='weight'))
        print(critical_path)

        # colorize graphviz (i.e add label 'color' in edge and node)
        colorize_path(G, critical_path, 'red')

        # colorize networkx (only node)
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
