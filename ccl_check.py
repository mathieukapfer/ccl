from ccl_def import functions_args


# Check all 'in' streams are defined i.e. exist as 'out' streams somewhere
def check_streams_defined():
    '''
    Check all 'in' parameters is defined and
    return dict of in and out parameters

         input:   functions_args
         returns: 4 dictionnary (see below)

    '''
    # set of in and out paramters
    params_in = set()
    params_out = set()

    # dict of parameters vs functions
    table_param_in = dict()
    table_param_out = dict()

    for (fct, params) in functions_args:
        for (in_out, param) in params:
            if (in_out == "in"):
                params_in.add(param)
                # append to dict val
                table_param_in[param] = table_param_in.get(param, []) + [fct]
            else:
                params_out.add(param)
                # set to dict val (assuming one)
                table_param_out[param] = fct

    # test if all 'in' param is existing in 'out' set
    if (params_in <= params_out):
        print("Check: All streams are defined")
    else:
        print("Error: Stream(s) not defined: {}".format(params_out - params_in))
        print(" in:  {} ".format(params_in))
        print(" out: {} ".format(params_out))

    # return dict
    return (table_param_in,   # key: param, val: fct consumer
            table_param_out  # key: param, val: fct producer (assuming one only)
            )
