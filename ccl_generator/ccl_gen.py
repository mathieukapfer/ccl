import networkx as nx
import matplotlib.pyplot as plt

from ccl_graph.ccl_graph_viewer import draw_graph
from ccl_generator.ccl_graph import build_stream_graph
from ccl_generator.ccl_def import functions_execution_model

def gen_execution_model_from_node(node_name, G, consumed_node, level, exec_G):
    """ process one node """
    level += 1
    for node in list(G.successors(node_name)):
        if node not in consumed_node:

            # analyse node
            fct_producer = G.nodes[node]['fct']
            execution_model = functions_execution_model[fct_producer]
            print('[{}]node:{} produce by \t {} with {}'.format(level, node, fct_producer, execution_model))
            # fork ?
            nb_execution = functions_execution_model[fct_producer].get('table',1)

            # create execution graph
            for index in range(0, nb_execution):
                print(node_name + ':' + str(nb_execution))
                exec_G.add_edge(node_name, node if nb_execution < 2 else node + str(index))

                # call recusively
                consumed_node.append(node)
                gen_execution_model_from_node(node, G, consumed_node, level, exec_G)


def gen_execution_model():
    stream_G = build_stream_graph(True)
    exec_G = nx.DiGraph();

    consumed_node = list()
    gen_execution_model_from_node('start', stream_G, consumed_node, 0, exec_G)

    draw_graph(exec_G);
    return exec_G


def draw_exec_graph():
    plt.figure(1)
    draw_graph(gen_execution_model(), critical_path='none')

    plt.show(block=False)


draw_exec_graph()
