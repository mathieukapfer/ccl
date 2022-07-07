import networkx as nx


def format_node_name(node):
    """
    Format node name
       input: node dictionary
       return string of long name of the given node
    """
    # phase
    if node.get('phase-obs') == node.get('phase-def'):
        phase_str = node.get('phase-def')
    else:
        phase_str = "{}->{}".format(node.get('phase-def'),
                                    node.get('phase-obs'))
    print(node)
    print(phase_str)

    return "{}\n ({})\n phase{}".format(
        #\n size:{} \n runtime:{}
        node.get('action'),
        node.get('id'),
        phase_str,
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
       return graph in networkx
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
                'label': "(" + obs_id[1] + ")",
                # 'phase': node['phase'],
            }
            ), ])

    print("\n {}".format(nodes_name_dict))

    return G


def write_dot_graph(G):
    """
    Create dot file that can be display with xdot
       input: graph in networkx format
    """
    ccl_dot = nx.nx_pydot.to_pydot(G)
    ccl_dot.write_raw("out_ccl_raw.dot")
