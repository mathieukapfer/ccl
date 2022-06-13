import re
import networkx as nx


def parse_keys(line, keys, cur_dict, clear=False):
    """
    Parse line:
    [phase = 0, 1]
    [action = cbl_concat_tblkcrc_generate_cfunc], [elementsize = 36668], [runtime = 40000], [definition_ID(arg#) = 3(4)],

       Input:
          - line to parse
          - keys list to parse
          - cur_dict to be completed with  [ key, val ]

       return: True if one key is found

    """
    ret = False
    for key in keys:
        m = re.search("\[" + key + " = " + "([\w ,]+)", line)
        if m:
            ret = True
            if clear is True:
                cur_dict.clear()
            cur_dict[key] = m.group(1)
            print(">>>" + key + ":" + m.group(1))

    return ret


def parse_definition_ID(line, dict_action):
    """
    Parse line:
    ... [definition_ID(arg#) = 3(4)],

       return: dictionay of [ name, val ]

    """

    # parse def_id
    ret = False
    m = re.search("definition_ID\(arg#\)" + " = ", line)
    if m:
        n = re.search("(\d+)\((\d+)\)", line[m.end():])
        dict_action['id'] = n.group(1)
        dict_action['pos'] = n.group(2)

    return ret


def parse_observation_ids(line):
    """
    Parse line:
    [observation_ids(arg#s) = 12(1), 13(1), 102(2), 31(3)],

       return: a list of (arg, pos)

    """

    obs_ids = list(tuple())
    m = re.search("\[" + "observation_ids\(arg#s\)" + " = ", line)
    if m:
        # print(line)
        # print(line[m.start():m.end()])
        pos = m.end();
        # n = re.search("(\d+)\((d+)\)", line)
        # n = re.search("(\d+)(\(d+\))", line[m.end()])
        n = re.search("(\d+)\((\d+)\)", line[pos:])
        while n:
            pos += n.end()
            obs_ids.append((n.group(1), n.group(2)))
            # print("arg:{}, pos:{}".format(n.group(1), n.group(2)))
            n = re.search("(\d+)\((\d+)\)", line[pos:])
    return obs_ids


def format_node_name(nodes_name, node_description):
    """
    Append to nodes dict a new entry to convert
      - node id (the number of id) to
      - node content: full name with producer action and other parameters
    NOTE: this dictionary can be use to rename node tree with 'full name'

       Input:
         - nodes_name : the dictinnary of all node names to update
         - node_description: the description of current node to add


    """
    # build dic for rename node : replace number by procuder name
    print("\n Add node Node #{} : {}".format(node_description.get('id', 'unknown'),node_description.get('action', 'unknown')))
    nodes_name[node_description.get('id','none')] = "{}\n ({})\n phase{}".format(
        #\n size:{} \n runtime:{}
        node_description.get('action'),
        node_description.get('id'),
        node_description.get('phase'),
        # node_description.get('elementsize'),
        # node_description.get('runtime'),
    )


def ccl_parser():
    """
    Parse CCL file
    """

    file1 = open('CCL_file_2cblk.txt', 'r')
    lines = file1.readlines()

    G = nx.DiGraph()

    nodes_name_dict = dict()
    node_dict = dict()
    nodes_dict = dict()

    step = 1

    for line in lines:

        # 0) skip comment
        if line[0] == '#':
            continue

        # 1) parse phase parameters
        # [phase = 0,1],
        if step == 1 and parse_keys(line, ["phase"], node_dict, clear=True):
            step += 1
            continue

        # 2) parse action paremeters
        # [action = stub_rate1_cfunc], [elementsize = 52224],[runtime = 2000],
        if step == 2 and parse_keys(line, ["action", "elementsize", "runtime"], node_dict):
            step += 1

            # same line parse 'definition_ID'
            # ..  [definition_ID(arg#) = 101(0)],
            parse_definition_ID(line, node_dict)

            # format full name of node
            format_node_name(nodes_name_dict, node_dict)
            # create node for the current stream
            G.add_node(node_dict.get('id','none'))
            # next line
            continue


        # 3) parse 'observation_ids' (maybe same line!)
        if step == 3: # optional step => no step incrementation
            ids = parse_observation_ids(line)
            if len(ids):
                print(line)
                print(ids)
                print(node_dict)

                # create edge for each observed streams -> current stream
                for (stream, pos) in ids:
                    print("{} -> {}({})".format(
                        stream, node_dict['action'], node_dict.get('id','none')))
                    G.add_edge(stream, node_dict.get('id', 'end'))


        # 4) parse timing parameters
        # [define = 283], [end_define = 290], [L2toDDR = 498], [DDRtoL2 = 0], [observe_start = 3], [observe_end = 305],
        if step == 3 and (parse_keys(line, ["define", "end_define", "L2toDDR", "DDRtoL2", "observe_start", "observe_end"], node_dict)):
            # next line
            step += 1
            continue


        # 5) parse resources parameters
        # [defining resource = pe0_0], [define memory offset = 92232], [observe memory offset = 73386];
        if step == 4 and (parse_keys(line, ["defining resource", "define memory offset", "observe memory offset"], node_dict)):

            # complete node dict
            nodes_dict[node_dict.get('id','unknown')] = node_dict
            print(node_dict)

            # next line
            step = 1
            continue


    print(nodes_name_dict)
    print(nodes_dict)

    nx.relabel_nodes(G, nodes_name_dict, copy=False)

    return G


G = ccl_parser()
ccl_dot = nx.nx_pydot.to_pydot(G)
ccl_dot.write_raw("out_ccl_raw.dot")
