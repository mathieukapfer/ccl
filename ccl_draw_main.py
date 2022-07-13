import matplotlib.pyplot as plt

from ccl_parser.ccl_parse2 import ccl_file_parser
from ccl_draw.ccl_draw_smem import draw_smem_map
from ccl_draw.ccl_draw_stat import draw_stat


def ccl_draw():
    """
    """
    # define style
    plt.style.use('seaborn')

    # define ratio
    gs_kw = dict(width_ratios=[1], height_ratios=[5, 1, 5, 1])

    # create fig and axes
    fig, axd = plt.subplot_mosaic([['cluster 1'], ['stat1'],
                                   ['cluster 2'], ['stat2']],
                                  gridspec_kw=gs_kw,
                                  #figsize=(5.5, 3.5),
                                  #constrained_layout=True
    )


    # change properties
    # - shared x axes for cluster 1
    axd['cluster 1'].tick_params('x', labelbottom=False)
    axd['stat1'].get_shared_x_axes().join(axd['stat1'], axd['cluster 1'])
    # - shared x axes for cluster 2
    axd['cluster 2'].tick_params('x', labelbottom=False)
    axd['stat2'].get_shared_x_axes().join(axd['stat2'], axd['cluster 2'])

    # add label
    axd['cluster 1'].set_ylabel("cluster1\nSMEM addr")
    axd['stat1'].set_ylabel("cluster1\nnb PEs")
    axd['cluster 2'].set_ylabel("cluster2\nSMEM addr")
    axd['stat2'].set_ylabel("cluster2\nnb PEs")

    # legend
    #plt.title("Timeline")
    #plt.legend(title='Parameter where:')

    # parse ccl file
    nodes = ccl_file_parser(filename)

    # draw statistic
    draw_stat(nodes, [axd['stat1'], axd['stat2']])

    # draw smem usage
    draw_smem_map(nodes, fig, axd['cluster 1'],  # last axes (needed for arrow inter-axis)
                  [axd['cluster 1'], axd['cluster 2']])

    # display
    plt.show(block=False)


# filename = "data/CCL_file_phase3.txt"
filename = "data/ToKalray05JUL22/CCL_file.txt"  # working memory
# filename = "data/ToKalray07JUL22/CCL_file.txt"  # Tx
# filename = "data/ToKalray07JUL22/CCL_file_extract_broadcast.txt"
# filename = 'data/CCL_file_2cblk.txt'
# filename = 'data/ccl_file_12May22.txt'
# filename = 'data/CCL_file_test_smem_svg.txt'


ccl_draw()
