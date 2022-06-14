import re

comment = "#.*$"

sep = "[\s,]+"

sep0 = "[\s,]*"

keywords = [
    "phase",
    "action", "elementsize", "runtime", "definition_ID\(arg#\)",
    "observation_ids\(arg#s\)",
    "define", "end_define", "L2toL2", "L2toDDR", "DDRtoL2", "observe_start", "observe_end",
    "defining resource", "define memory offset", "observe memory offset",
    ]

keywords_value = {
    "phase":                       "([\w ,]+)",
    "action":                      "([\w]+)",
    "elementsize":                 "([\d]+)",
    "runtime":                     "([\d]+)",
    "definition_ID\(arg#\)":       "(\d+)\((\d+)\)",
    "observation_ids\(arg#s\)":    "((\d+)\((\d+)\)[, ]*)+",  # list of "(\d+)\((\d+)\)",
    "define":                      "([\d]+)",
    "end_define":                  "([\d]+)",
    "L2toL2":                      "([\d]+)",
    "L2toDDR":                     "([\d]+)",
    "DDRtoL2":                     "([\d]+)",
    "observe_start":               "([\d]+)",
    "observe_end":                 "([\d]+)",
    "defining resource":           "([\w]+)",
    "define memory offset":        "([-\d]+)",  # maybe negative
    "observe memory offset":       "([\d]+)",
}


def ccl_parser():
    """
    Parse CCL file
    """

    file1 = open('CCL_file_2cblk.txt', 'r')
    lines = file1.readlines()
    error = False
    nb_keys_found = 0

    for line in lines:
        pos = 0
        found = True
        # print(line)

        # 0) skip comment
        if line[0] == '#':
            continue

        # 1) search keyword
        while found is True:
            found = False
            for key in keywords:
                exp = sep0 + '\[' + sep0 + key + sep0 + "=" + sep0 + keywords_value[key] + sep0 + '\]'
                # print(exp)
                m = re.match(exp, line[pos:])
                if m:
                    found = True
                    nb_keys_found += 1
                    # print("===>" + key + ":" + m.group(1))
                    pos += m.end()

        # 2) check rest of line
        if pos < len(line):
            if not re.match("[\b ,;\n]+$", line[pos:]):
                error = True
                print("Skip: " + line[pos:])

    if error is False:
        print("No error found, {} keywords found".format(nb_keys_found))


ccl_parser()
