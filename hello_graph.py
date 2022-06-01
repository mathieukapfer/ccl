import matplotlib.pyplot as plt
import networkx as nx

def test_graph():
    G = nx.Graph()

    G.add_node(1)
    G.add_node(2)
    G.add_node(3)

    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(2, 3)

    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()


# test graphviz wrapper
def test_graphviz_wrapper():
    G = nx.petersen_graph()
    pos = nx.nx_agraph.graphviz_layout(G)
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, width=6)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

    plt.show()


test_graphviz_wrapper()
#test_graph()
