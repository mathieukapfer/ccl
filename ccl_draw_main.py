import matplotlib.pyplot as plt

from ccl_parser.ccl_parse2 import ccl_file_parser
from ccl_draw.ccl_draw_smem import draw_smem_map
from ccl_draw.ccl_draw_stat import draw_stat


def ccl_draw():
    """
    """

    # parse ccl file
    nodes = ccl_file_parser(filename)

    # check nb clusters
    nb_cluster=0
    for node_index in nodes:
        node = nodes[node_index]
        if node['cluster'] > nb_cluster:
            nb_cluster = node['cluster']
    print("nb cluster: {}".format(nb_cluster))


    # build fig spec according to nb clusters
    mosaic = [[], [], []]  # SMEM, stat, dma
    width_ratios = []

    # If nb_cluster=2, generate:
    # - mosaic= [['cluster 1', 'cluster 2'],
    #            ['stat1', 'stat2'],
    #            ['dma1', 'dma2']]
    # - width_ratios = [1, 1]
    for i in range(0, nb_cluster + 1):  # first cluster has number '0'
        mosaic[0].append('cluster {}'.format(i+1))  # TODO: remove +1
        mosaic[1].append('stat{}'.format(i+1))
        mosaic[2].append('dma{}'.format(i+1))
        width_ratios.append(1)

    # print("mosaic: {}".format(mosaic))

    # define style
    plt.style.use('seaborn')
    # plt.style.use('classic')

    # define ratio
    gs_kw = dict(width_ratios=width_ratios, height_ratios=[5, 1, 1], wspace=0.05, hspace=0.1)

    # create fig and axes
    fig, axd = plt.subplot_mosaic(mosaic,
                                  gridspec_kw=gs_kw,
                                  #figsize=(5.5, 3.5),
                                  #constrained_layout=True
    )


    # change properties
    for cluster in range(0, nb_cluster + 1):
        smem = 'cluster {}'.format(cluster+1)
        stat = 'stat{}'.format(cluster+1)
        dma = 'dma{}'.format(cluster+1)

        # - shared x axes
        axd[smem].tick_params('x', labelbottom=False)
        axd[stat].tick_params('x', labelbottom=False)
        axd[stat].get_shared_x_axes().join(axd[stat], axd[smem])
        axd[dma].get_shared_x_axes().join(axd[dma], axd[smem])

        # same y limit for all cluster (SMEM)
        axd[smem].set_ylim([0, 2*1024*1024])

        # change axes zorder to not overload arrow inter axis [not working yet!]
        axd[smem].set_axisbelow(True)
        axd[stat].set_axisbelow(True)
        axd[dma].set_axisbelow(True)

        # add axes label and title
        axd[smem].set_title(smem)

        if cluster > 0:
            # - remove inner tick and label
            axd[smem].tick_params('y', labelleft=False)


    # draw smem usage
    draw_smem_map(nodes, fig, axd['cluster 1'],  # last axes (needed for arrow inter-axis)
                  [axd['cluster 1'], axd['cluster 2']])

    # draw statistic
    axis = draw_stat(nodes, [axd['stat1'], axd['stat2'], axd['dma1'], axd['dma2']])

    # remove inner y tick and label
    # - remove Stat right scale of cluster 0
    axis[0][1].set_ylabel("")
    axis[0][1].tick_params('y', labelright=False)

    # - remove Stat left scale of cluster 1
    axis[1][0].set_ylabel("")
    axis[1][0].tick_params('y', labelleft=False)

    # - remove DMA left scale of cluster 1
    axis[1][2].set_ylabel("")
    axis[1][2].tick_params('y', labelleft=False)

    # same range for DMA event for all clusters
    ymin = min(axis[0][2].get_ylim()[0], axis[1][2].get_ylim()[0])
    ymax = max(axis[0][2].get_ylim()[1], axis[1][2].get_ylim()[1])
    axis[0][2].set_ylim([ymin, ymax])
    axis[1][2].set_ylim([ymin, ymax])

    # display
    plt.show(block=False)


filename = "data/CCL_file_phase3.txt"
# filename = "data/ToKalray12JUL22/CCL_file.txt"  # RX v2
# filename = "data/ToKalray05JUL22/CCL_file.txt"  # RX working memory
# filename = "data/ToKalray07JUL22/CCL_file.txt"  # Tx
# filename = "data/ToKalray07JUL22/CCL_file_extract_broadcast.txt"
# filename = 'data/CCL_file_2cblk.txt'
# filename = 'data/ccl_file_12May22.txt'
# filename = 'data/CCL_file_test_smem_svg.txt'


ccl_draw()
