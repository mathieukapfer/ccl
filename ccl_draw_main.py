import matplotlib.pyplot as plt

from ccl_parser.ccl_parse2 import ccl_file_parser
from ccl_draw.ccl_draw_smem import draw_smem_map
from ccl_draw.ccl_draw_stat import draw_stat


def ccl_draw():
    """
    """
    # define style
    plt.style.use('seaborn')
    # plt.style.use('classic')

    # define ratio
    gs_kw = dict(width_ratios=[1, 1], height_ratios=[5, 1, 1], wspace=0.05, hspace=0.1)

    # create fig and axes
    fig, axd = plt.subplot_mosaic([['cluster 1', 'cluster 2'],
                                   ['stat1', 'stat2'],
                                   ['dma1', 'dma2']],
                                  gridspec_kw=gs_kw,
                                  #figsize=(5.5, 3.5),
                                  #constrained_layout=True
    )


    # change properties
    # - shared x axes for cluster 1
    axd['cluster 1'].tick_params('x', labelbottom=False)
    axd['stat1'].tick_params('x', labelbottom=False)
    axd['stat1'].get_shared_x_axes().join(axd['stat1'], axd['cluster 1'])
    axd['dma1'].get_shared_x_axes().join(axd['dma1'], axd['cluster 1'])
    # - shared x axes for cluster 2
    axd['cluster 2'].tick_params('x', labelbottom=False)
    axd['stat2'].tick_params('x', labelbottom=False)
    axd['stat2'].get_shared_x_axes().join(axd['stat2'], axd['cluster 2'])
    axd['dma2'].get_shared_x_axes().join(axd['dma2'], axd['cluster 2'])

    # same y limit for all cluster (SMEM)
    axd['cluster 1'].set_ylim([0, 2*1024*1024])
    axd['cluster 2'].set_ylim([0, 2*1024*1024])

    # change axes zorder to not overload arrow inter axis [not working yet!]
    axd['stat1'].set_axisbelow(True)
    axd['cluster 1'].set_axisbelow(True)
    axd['stat2'].set_axisbelow(True)
    axd['cluster 2'].set_axisbelow(True)

    # add axes label and title
    axd['cluster 1'].set_title("cluster 1")
    axd['cluster 2'].set_title("cluster 2")
    axd['cluster 1'].set_ylabel("SMEM addr")
    # - remove inner tick and label
    axd['cluster 2'].tick_params('y', labelleft=False)

    # axd['stat1'].set_ylabel("cluster1\nnb PEs")
    # axd['cluster 2'].set_ylabel("cluster2\nSMEM addr")
    # axd['stat2'].set_ylabel("cluster2\nnb PEs")

    # legend
    #plt.title("Timeline")
    #plt.legend(title='Parameter where:')

    # parse ccl file
    nodes = ccl_file_parser(filename)

    # draw smem usage
    draw_smem_map(nodes, fig, axd['cluster 1'],  # last axes (needed for arrow inter-axis)
                  [axd['cluster 1'], axd['cluster 2']])

    # draw statistic
    axis = draw_stat(nodes, [axd['stat1'], axd['stat2'], axd['dma1'], axd['dma2']])
    print("Stat Axis: {}".format(axis))
    # remove inner y tick and label
    axis[0][1].set_ylabel("")
    axis[0][1].tick_params('y', labelright=False)
    axis[1][0].set_ylabel("")
    axis[1][0].tick_params('y', labelleft=False)
    print("Stat Axis: {}".format(axis))

    # display
    plt.show(block=False)


# filename = "data/CCL_file_phase3.txt"
filename = "data/ToKalray12JUL22/CCL_file.txt"  # RX v2
# filename = "data/ToKalray05JUL22/CCL_file.txt"  # RX working memory
# filename = "data/ToKalray07JUL22/CCL_file.txt"  # Tx
# filename = "data/ToKalray07JUL22/CCL_file_extract_broadcast.txt"
# filename = 'data/CCL_file_2cblk.txt'
# filename = 'data/ccl_file_12May22.txt'
# filename = 'data/CCL_file_test_smem_svg.txt'


ccl_draw()
