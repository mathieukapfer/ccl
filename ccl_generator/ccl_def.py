# Should replace rdsl & system constraint file

# - functions runtime
functions_run_time = {
    "getSoftBitsData_cfunc": 1280,
    "getUserBLPInfo_cfunc": 1500,
    "extract_data_cblk_info_cfunc": 2000,
    "descrambler_cfunc": 40000,
    "soft_bits_data_demux_cfunc": 7000,
    "ldpc_decoder_cfunc": 2000000,
    "rate_dematch_cfunc": 200000,
    "extract_data_tblk_info_cfunc": 1000,
    "cbl_concat_tblkcrc_generate_cfunc": 40000,
    "putUserTBLKData_cfunc": 1162,
    # buf stub
    "buffer_ldpc_cfunc": 2000,
    "stub_rate0_cfunc": 2000,
    "stub_rate1_cfunc": 2000,
}

# - streams definition
streams = {
    # bufs
    "buffer_ldpc": 183168,
    "buffer_rate0": 1456,
    "buffer_rate1": 1456,
    # streams
    "soft_bits_per_ue": 27600,
    "blp_info_per_ue": 256,
    "descramble_soft_bits_per_ue": 36668,
    "data_cblk_list": 256,
    "soft_bits_data_cblk_1": 18334,
    "soft_bits_data_cblk_2": 18334,
    "data_cblk_list": 256,
    "rate_dematch_1": 16848,
    "rate_dematch_2": 16848,
    "dbit_1": 16848,
    "dbit_2": 16848,
    "data_tblk_info": 256,
    "tblk": 36668,
    "end": 0,
}


# - function prototypes
functions_args = [
    # buffers creation
    ("buffer_ldpc_cfunc",            [("out", "buffer_ldpc")]),
    ("stub_rate0_cfunc",             [("out", "buffer_rate0")]),
    ("stub_rate1_cfunc",             [("out", "buffer_rate1")]),

    # steams compute
    ("getSoftBitsData_cfunc",        [("out", "soft_bits_per_ue")]),
    ("getUserBLPInfo_cfunc",         [("out", "blp_info_per_ue")]),
    ("descrambler_cfunc",            [("in", "soft_bits_per_ue"), ("in", "blp_info_per_ue"), ("out", "descramble_soft_bits_per_ue")]),
    ("extract_data_cblk_info_cfunc", [("in", "blp_info_per_ue"), ("out", "data_cblk_list")]),
    ("soft_bits_data_demux_cfunc",   [("in", "descramble_soft_bits_per_ue"), ("in", "data_cblk_list"), ("out", "soft_bits_data_cblk_1"), ("out", "soft_bits_data_cblk_2")]),

    # block 1
    ("rate_dematch_cfunc",           [("in", "soft_bits_data_cblk_1"), ("in", "data_cblk_list"), ("in", "buffer_rate0"), ("in", "buffer_rate1"), ("out", "rate_dematch_1")]),
    ("ldpc_decoder_cfunc",           [("in", "data_cblk_list"), ("in", "rate_dematch_1"), ("in", "buffer_ldpc"), ("out", "dbit_1")]),
    # bloc 2
    ("rate_dematch_cfunc",           [("in", "soft_bits_data_cblk_2"), ("in", "data_cblk_list"), ("in", "buffer_rate0"), ("in", "buffer_rate1"), ("out", "rate_dematch_2")]),
    ("ldpc_decoder_cfunc",           [("in", "data_cblk_list"), ("in", "rate_dematch_2"), ("in", "buffer_ldpc"), ("out", "dbit_2")]),

    # concat blocks
    ("extract_data_tblk_info_cfunc", [("in", "data_cblk_list"), ("out", "data_tblk_info")]),
    ("cbl_concat_tblkcrc_generate_cfunc", [("in", "dbit_1"), ("in", "dbit_2"), ("in", "data_tblk_info"), ("out", "tblk")]),
    ("putUserTBLKData_cfunc",        [("in", "tblk"), ("out", "none")]),
    ]


# - functions execution model
functions_execution_model = {
    'buffer_ldpc_cfunc':                    {},
    'stub_rate0_cfunc':                     {},
    'stub_rate1_cfunc':                     {},
    'getSoftBitsData_cfunc':                {},
    'getUserBLPInfo_cfunc':                 {},
    'descrambler_cfunc':                    {},
    'extract_data_cblk_info_cfunc':         {'table': 2},  # generate two streams
    'soft_bits_data_demux_cfunc':           {'table': 2},  # generate two streams
    'rate_dematch_cfunc':                   {'table': 2, 'phase': [0, 1]},
    'ldpc_decoder_cfunc':                   {'table': 2, 'phase': [1]},
    'cbl_concat_tblkcrc_generate_cfunc':    {'phase': [1]},
    'putUserTBLKData_cfunc':                {'phase': [1]},
}
