import matplotlib.pyplot as plt
import networkx as nx


from ccl_generator.ccl_check import check_streams_defined
from ccl_generator.ccl_def import functions_run_time, functions_args, streams
from ccl_graph.ccl_graph_viewer import draw_graph


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


def build_stream_graph(display=False):
    """ Build DAG with stream as node """
    G = nx.DiGraph()

    # param as node, fct as edge:
    # for each function, link output parameter and input parameters
    for (fct, params) in functions_args:
        param_in_list = [param for (in_out, param) in params if in_out == 'in']

        if len(param_in_list) == 0:
            # no input parameter => add node 'start'
            param_in_list = ['start']

        for param_in in param_in_list:
            for param_out in [param for (in_out, param) in params if in_out == 'out']:
                # create 'stream' node with producer and size
                G.add_nodes_from([ (param_out, {
                    'size': streams.get(param_out, "unknown"),  # G.nodes[param_out]['size'] = streams[param_out]
                    'label': fct,                  # G.nodes[param_out]['fct'] = fct
                }
                ), ])

                # create edges with producer run time
                G.add_edges_from([ (param_in, param_out, {
                    'weight': functions_run_time[fct]
                }
                ), ])

    # display
    if (display):
        print("nodes:{}".format(G.nodes(data=True)))
        print("edges:{}".format(G.edges(data=True)))

    return G


def draw_my_graph():
    """ draw fct and data graph """
    # figure, axis = plt.subplots(1, 1)
    plt.figure(1)
    draw_graph(build_fct_graph(), critical_path='none')

    plt.figure(2)
    draw_graph(build_stream_graph(), critical_path='yes')

    plt.show(block=False)


def write_dot(G):
    """
    Save networkx graph in dot file format.
    Use 'xdot out.dot' command to display it

       input: G: graph in networkx fomat to be converted

    """
    my_dot = nx.nx_pydot.to_pydot(G)
    my_dot.write_raw("out_raw.dot")



write_dot(build_stream_graph(display=True))
#draw_my_graph()
