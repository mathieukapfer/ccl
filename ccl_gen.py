from ccl_graph import build_stream_graph, draw_my_graph
from ccl_def import functions_execution_model


def gen_execution_model_from_node(node_name, G, consumed_node, level):
    """ process one node """
    level += 1
    for node in list(G.successors(node_name)):
        if node not in consumed_node:
            print('[{}]node:'.format(level) + node)
            consumed_node.append(node)
            gen_execution_model_from_node(node, G, consumed_node, level)


def gen_execution_model():
    G = build_stream_graph(True)
    consumed_node = list()
    gen_execution_model_from_node('start', G, consumed_node, 0)


draw_my_graph()
gen_execution_model()
