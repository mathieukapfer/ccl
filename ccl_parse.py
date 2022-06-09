import re
import networkx as nx


def parse_action(line, keys, cur_dict):
    """
    Parse line:
    [phase = 0, 1]
    [action = cbl_concat_tblkcrc_generate_cfunc], [elementsize = 36668],[runtime = 40000], [definition_ID(arg#) = 3(4)],

       Input:
          - line to parse
          - key to parse
          - cur_dict to complete with  [ key, val ]

       return: True if one key is found

    """
    ret = False
    for key in keys:
        m = re.search("\[" + key + " = " + "([\w ,]+)", line)
        if m:
            ret = True
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


def ccl_parser():
    """
    Parse CCL file
    """

    file1 = open('CCL_file_2cblk.txt', 'r')
    lines = file1.readlines()

    G = nx.DiGraph()

    relabel_dict = dict()
    stream_dict = dict()

    for line in lines:

        # first parse 'phase'
        if parse_action(line, ["phase"], stream_dict):
            continue

        # second parse 'action'
        if parse_action(line, ["action", "elementsize", "runtime"], stream_dict):
            # same line parse 'definition_ID'
            parse_definition_ID(line, stream_dict)

        print(line)
        print(stream_dict)

        if(len(stream_dict) >= 6):  # all key defined
            print(line)
            print(stream_dict)
            # build dic for rename node : replace number by procuder name
            # print(">>> #" + stream_dict.get('id', ''))
            # print(">>> name" + stream_dict.get('action', ''))
            relabel_dict[stream_dict.get('id','none')] = "{}\n ({})\n phase:{}".format( #\n size:{} \n runtime:{}
                stream_dict.get('action'),
                stream_dict.get('id'),
                stream_dict.get('phase'),
                # stream_dict.get('elementsize'),
                # stream_dict.get('runtime'),
            )

            G.add_node(stream_dict.get('id','none'))


        # third, parse 'observation_ids' (maybe same line!)
        ids = parse_observation_ids(line)
        if len(ids):
            print(line)
            print(ids)
            print (stream_dict)

            # build graph
            for (stream, pos) in ids:
                print("{} -> {}({})".format(
                    stream, stream_dict['action'], stream_dict.get('id','none')))
                G.add_edge(stream, stream_dict.get('id', 'end'))

            # reset dict
            stream_dict = dict()


    print(relabel_dict)

    nx.relabel_nodes(G, relabel_dict, copy=False)

    return G


G = ccl_parser()
ccl_dot = nx.nx_pydot.to_pydot(G)
ccl_dot.write_raw("out_ccl_raw.dot")
