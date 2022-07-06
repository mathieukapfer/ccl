import re

# Syntaxe

comment = "#.*$"

sep = "[\s,]+"

sep0 = "[\s,]*"

endofstream = "[\s;]+"

keywords = [
    "CCLtype",
    "phase",
    "action", "elementsize", "runtime", "definition_ID\(arg#\)",
    "observation_ids\(arg#s\)",
    "define", "end_define", "L2toL2", "L2toDDR", "DDRtoL2", "observe_start", "observe_end",
    "defining resource", "define memory offset", "observe memory offset",
    ]

regexp_id = "(\d+)\((\d+)\)"  # 1(2)

keywords_value = {
    "CCLtype":                     "([\w]+)",
    "phase":                       "([\w ,]+)",
    "action":                      "([\w]+)",
    "elementsize":                 "([\d]+)",
    "runtime":                     "([\d]+)",
    "definition_ID\(arg#\)":       "(" + regexp_id + ")",
    "observation_ids\(arg#s\)":    "((" + regexp_id + sep0 + ")+)",
    "define":                      "([\d]+)",
    "end_define":                  "([\d]+)",
    "L2toL2":                      "([\d]+)",
    "L2toDDR":                     "([\d]+)",
    "DDRtoL2":                     "([\d]+)",
    "observe_start":               "([\d]+)",
    "observe_end":                 "([\d]+)",
    "defining resource":           "([\w]+)",
    "define memory offset":        "([-\d]+)",  # maybe negative !
    "observe memory offset":       "([\d]+)",
}


# Grammar

def ccl_item(key):
    """
    return the regexp for one key
    """
    return sep0 + '\[' + sep0 + key + sep0 + "=" + sep0 + keywords_value[key] + sep0 + '\]'


def ccl_item_parser(key, value, node_dict):
    """
    Complete node dictionary with current key and value.
    Refine value if needed

       Input:
          - key & value : current couple of key, value
          - node_dict : current node dictionnary under construction

    """

    # special keys
    if key == 'phase':
        # phase (todo : extract list of phases)
        node_dict[key] = value

    elif key == "definition_ID\(arg#\)":
        # refine value: extract id and position
        m = re.match(keywords_value[key], value)
        node_dict['id'] = m.group(2)
        node_dict['pos'] = m.group(3)

    elif key == "observation_ids\(arg#s\)":
        # refine value: extract list of id and position
        pos = 0
        obs_ids = list(tuple())
        n = re.search(regexp_id, value[pos:])
        while n:
            pos += n.end()
            obs_ids.append((n.group(1), n.group(2)))
            n = re.search(regexp_id, value[pos:])
        node_dict['obs_ids'] = obs_ids
    # other keys
    else:
        node_dict[key] = value


def ccl_file_parser(filename):
    """
    Parse CCL file and return dictionnary of streams
    """

    # read file
    file1 = open(filename, 'r')
    lines = file1.readlines()

    # prepare parsing
    error = False
    nb_keys_found = 0
    node_dict = dict()
    nodes_dict = dict()


    # parse each item and build items dictionnary
    for line in lines:
        pos = 0
        found = True
        # print(line)

        # 0) skip comment
        if line[0] == '#':
            continue

        # 1) search keyword
        while found is True:
            found = False  # simulate do .. while loop
            for key in keywords:
                exp = ccl_item(key)
                # print(exp)
                m = re.match(exp, line[pos:])
                if m:
                    # update loop parameters
                    found = True
                    nb_keys_found += 1
                    print("===>" + key + ":" + m.group(1))

                    # parse node
                    ccl_item_parser(key, m.group(1), node_dict)

                    # move pointer
                    pos += m.end()

        # 2) check rest of line
        if pos < len(line):
            # end of stream : ';'
            m = re.match(endofstream, line[pos:])
            if len(node_dict) > 0 and m:
                pos += m.end()
                nodes_dict[node_dict.get('id', 'none')] = node_dict.copy()
                print(node_dict)
                node_dict.clear()
            # still something ?
            elif not re.match("[\b ,\n]+$", line[pos:]):
                error = True
                print("Skip: " + line[pos:])


    # status
    if error is False:
        print("\n\nNo error found:")
        print(" {} keywords found".format(nb_keys_found))
        print(" {} nodes detected".format(len(nodes_dict)))
        print(nodes_dict)

    return nodes_dict


#if __name__ == "__main__":
def main():
    # d = ccl_file_parser('CCL_file_2cblk.txt')
    d = ccl_file_parser('ccl_file_12May22.txt')
    print(d)

# main()
