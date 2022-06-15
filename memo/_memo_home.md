
# leaf:

  param in [x for x in G.nodes() if G.out_degree(x) >= 1 and G.in_degree(x) == 0]

# create node

## way 1

G.add_nodes_from([ (param_out, {
    'size': streams[param_out],
    'fct': fct,
    }
), ])

## way 2

G.nodes[param_out]['size'] = streams[param_out]
G.nodes[param_out]['fct'] = fct
