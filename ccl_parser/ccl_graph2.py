import matplotlib.pyplot as plt
import networkx as nx

from ccl_parse2 import ccl_file_parser


def format_node_name(node):
    """
    return long name of given node as sting
    """
    return "{}\n ({})\n phase{}".format(
        #\n size:{} \n runtime:{}
        node.get('action'),
        node.get('id'),
        node.get('phase'),
        # node_description.get('elementsize'),
        # node_description.get('runtime'),
        )


def build_stream_graph(nodes_dict):
    """
    """
    G = nx.DiGraph()

    nodes_name_dict = dict()

    for node_id in nodes_dict:
        node = nodes_dict[node_id]

        # Append node name dict
        nodes_name_dict[node_id] = format_node_name(node)

        # Create node
        G.add_node(node_id)

        # Create edge
        for obs_id in node.get('obs_ids',[]):
            G.add_edge(obs_id[0], node_id)

    print("\n {}".format(nodes_name_dict))
    nx.relabel_nodes(G, nodes_name_dict, copy=False)

    return G


def display_graph(G):
    """
    """
    ccl_dot = nx.nx_pydot.to_pydot(G)
    ccl_dot.write_raw("out_ccl_raw.dot")


display_graph(build_stream_graph(ccl_file_parser()))
