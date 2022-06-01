
# Should replace rdsl & system constraint file

# - functions runtime
functions_run_time = [
    ("getSoftBitsData_cfunc", 1280),
    ("getUserBLPInfo_cfunc", 1500),
    ("extract_data_cblk_info_cfunc", 2000),
    ("descrambler_cfunc", 40000),
    ("soft_bits_data_demux_cfunc", 7000),
    ("ldpc_decoder_cfunc", 2000000),
    ("rate_dematch_cfunc", 200000)]

# - streams definition
streams = [
    ("buffer_ldpc", 183168),
    ('soft_bits_per_ue', 27600),
    ('blp_info_per_ue', 256),
    ('descramble_soft_bits_per_ue', 36668),
    ('data_cblk_list', 256),
    ('soft_bits_data_cblk', 18334),
    ('data_cblk_list', 256),
    ('rate_dematch', 16848),
    ('dbit', 16848)]


# - functions list
functions_list = [
        "getSoftBitsData_cfunc"
        "getUserBLPInfo_cfunc",
        "extract_data_cblk_info_cfunc",
        "descrambler_cfunc",
        "soft_bits_data_demux_cfunc",
        "ldpc_decoder_cfunc",
        "rate_dematch_cfunc",
]

# - function prototypes
functions_args = [
    ("buffer_ldpc_cfunc",            [("out", "buffer_ldpc")]),
    ("getSoftBitsData_cfunc",        [("out", "soft_bits_per_ue")]),
    ("getUserBLPInfo_cfunc",         [("out", "blp_info_per_ue")]),
    ("descrambler_cfunc",            [("in", "soft_bits_per_ue"), ("in", "blp_info_per_ue"), ("out", "descramble_soft_bits_per_ue")]),
    ("extract_data_cblk_info_cfunc", [("in", "blp_info_per_ue"), ("out", "data_cblk_list")]),
    ("soft_bits_data_demux_cfunc",   [("in", "descramble_soft_bits_per_ue"), ("in", "data_cblk_list"), ("out", "soft_bits_data_cblk")]),
    ("rate_dematch_cfunc",           [("in", "soft_bits_data_cblk"), ("in", "data_cblk_list"), ("out", "rate_dematch")]),
    ("ldpc_decoder_cfunc",           [("in", "data_cblk_list"), ("in", "rate_dematch"), ("in", "buffer_ldpc"), ("out", "dbit")]),
    ]


