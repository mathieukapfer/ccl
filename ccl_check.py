from ccl_def import *

def check_streams_defined():
    """  Check call graph & streams coherancy """
    # check all 'in' streams are defined
    params_in = set()
    params_out = set()
    for (func, params) in functions_args:
        for (in_out, param) in params:
            if (in_out == "in"):
                params_in.add(param)
            else:
                params_out.add(param)
    # all 'in' items are included in 'out' set
    #   print("in:{}".format(params_in))
    #   print("out:{}".format(params_out))
    if (params_in < params_out):
        print("Check: All streams are defined")
    else:
        print("Error: Stream(s) not defined:{}".format(params_out - params_in ))
        
     

            


