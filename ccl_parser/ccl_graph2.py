import matplotlib.pyplot as plt
import networkx as nx

from ccl_parser.ccl_parse2 import ccl_file_parser
from ccl_graph.ccl_graph_viewer import draw_graph


def format_node_name(node):
    """
    Format node name
       input: node dictionary
       return string of long name of the given node
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
    Build graph from nodes dictionary
       input: dictionary of nodes where
               - obs_id : is the observed id
               - id: is the node_id
               => edge is create to mark the dependencies from one id to its observed id
       return tuple (networkx graph, dictionary of nodes name)
    """
    G = nx.DiGraph()

    nodes_name_dict = dict()

    for node_id in nodes_dict:
        node = nodes_dict[node_id]

        # Create node
        #G.add_node(node_id)
        G.add_nodes_from([(node_id, {
            'label': format_node_name(node),
        }
        ), ])

        # Create edge
        for obs_id in node.get('obs_ids', []):
            # G.add_edge(obs_id[0], node_id)
            G.add_edges_from([(obs_id[0], node_id, {
                'weight': int(node['runtime']),
                # 'phase': node['phase'],
            }
            ), ])

    print("\n {}".format(nodes_name_dict))

    return (G, nodes_name_dict)


def write_dot_graph(G):
    """
    Create dot file that can be dispplay with xdot
    """
    ccl_dot = nx.nx_pydot.to_pydot(G)
    ccl_dot.write_raw("out_ccl_raw.dot")


#if __name__ == '__main__':
def main():
    # build graph from ccl file
    filename = 'CCL_file_2cblk.txt'
    #filename = 'ccl_file_12May22.txt'

    (G, nodes_name_dict) = build_stream_graph(ccl_file_parser(filename))

    # color critical path
    critical_path = nx.dag_longest_path(G, weight='weight')
    for node in critical_path:
        G.nodes[node]['color'] = 'red'

    # draw with matplotlib
    draw_graph(G, critical_path='no')
    plt.show(block=False)

    # save graph in dot format
    # nx.relabel_nodes(G, nodes_name_dict, copy=False)

    write_dot_graph(G)


main()
