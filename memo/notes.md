
# graph content

## items
G.nodes()
G.edges()
G.number_of_edges()
G.number_of_nodes()

## degree

G.degree['soft_bits_per_ue']
==> 1

G.degree['blp_info_per_ue']
==> 2

>>> G.degree(list(G.nodes))
DiDegreeView({'soft_bits_per_ue': 1, 'descramble_soft_bits_per_ue': 3, 'blp_info_per_ue': 2, 'data_cblk_list': 5, 'soft_bits_data_cblk': 3, 'rate_dematch': 3, 'dbit': 4, 'buffer_ldpc': 1, 'tblk': 5, 'buffer_rate1_cfunc': 1, 'buffer_rate2_cfunc': 1, 'end': 1})
>>> G.in_degree(list(G.nodes))
InDegreeView({'soft_bits_per_ue': 0, 'descramble_soft_bits_per_ue': 2, 'blp_info_per_ue': 0, 'data_cblk_list': 1, 'soft_bits_data_cblk': 2, 'rate_dematch': 2, 'dbit': 3, 'buffer_ldpc': 0, 'tblk': 4, 'buffer_rate1_cfunc': 0, 'buffer_rate2_cfunc': 0, 'end': 1})
>>> G.out_degree(list(G.nodes))
OutDegreeView({'soft_bits_per_ue': 1, 'descramble_soft_bits_per_ue': 1, 'blp_info_per_ue': 2, 'data_cblk_list': 4, 'soft_bits_data_cblk': 1, 'rate_dematch': 1, 'dbit': 1, 'buffer_ldpc': 1, 'tblk': 1, 'buffer_rate1_cfunc': 1, 'buffer_rate2_cfunc': 1, 'end': 0})


## leafs
[x for x in G.nodes() if G.out_degree(x)==0 and G.in_degree(x)==1]
==> ['end']

[x for x in G.nodes() if G.out_degree(x)==1 and G.in_degree(x)==0]
==> ['soft_bits_per_ue', 'buffer_ldpc', 'buffer_rate1_cfunc', 'buffer_rate2_cfunc']

# node navigation
list(G.predecessors('descramble_soft_bits_per_ue'))


# attributes

## graph attributes
nx.get_edge_attributes(G, "fct")
nx.get_edge_attributes(G, "weight")

## edge attributes
G.edges[('soft_bits_per_ue', 'descramble_soft_bits_per_ue')]
{'weight': 40000, 'fct': 'descrambler_cfunc'}





# function list parser

for (func, param) in functions_list:
...   param
... 
[]
[]
[]
[]
[]
[]
[('table', 2)]
[('table', 2)]
[('phase', [0, 1])]
[('phase', [1])]
[('phase', [1])]
[('phase', [1])]
>>> for (func, params) in functions_list:
...   for param in params:
...     param
... 
('table', 2)
('table', 2)
('phase', [0, 1])
('phase', [1])
('phase', [1])
('phase', [1])
>>> for (func, params) in functions_list:
...   for param in [val for (name, val) in params if name='table']
...   for param in [val for (name, val) in params if name='table']
  File "<stdin>", line 3
    for param in [val for (name, val) in params if name='table']
      ^
IndentationError: expected an indented block
>>> for (func, params) in functions_list:
...   for param in params:
...       for param in [val for (name, val) in params if name='table']:
  File "<stdin>", line 3
    for param in [val for (name, val) in params if name='table']:
                                                       ^
SyntaxError: invalid syntax
>>> for (func, params) in functions_list:
...   for param in params:
...       for param in [val for (name, val) in params if name=='table']:
...         param
... 
2
2
