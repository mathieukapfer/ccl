# source: https://www.malinga.me/networkx-visualization-with-graphviz-example/

import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edges_from([('A', 'B'), ('A', 'C'), ('A', 'D'), ('E', 'D'), ('D', 'F'), ('E', 'C'), ('E', 'G'), ('B', 'H'), ('H', 'F')])

def random_layout():
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos)
    plt.show()

def graphviz_layout():
    pos = nx.nx_pydot.graphviz_layout(G)
    nx.draw_networkx(G, pos)
    plt.show()
    #plt.savefig('networkx_graph.png')

def graphviz_viewer():
    A = nx.nx_agraph.to_agraph(G)
    A.layout()
    A.draw('networkx_graph.png')

def my_gz():
    GZ = nx.nx_pydot.to_pydot(G)
    GZ.to_string()
    GZ.write_dot("my.dot")
    return GZ
