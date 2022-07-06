import re

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from ccl_parser.ccl_parse2 import ccl_file_parser


def get_cluster(ressource_string):
    """
    Return last digit of 'define resource' known as cluster
    """
    m = re.match("([\w]+)_(\d)", ressource_string) # 'pe3_9'
    cluster = int(m[2])
    return cluster


def draw_svg(nodes):
    """
    Draw SMEM usage in svg format x:time, y:space
    """
    #d = draw.Drawing(2000, 2000, origin=(0,0), displayInline=False)
    fig = plt.figure()
    ax_cluster1 = fig.add_subplot(211)
    ax_cluster2 = fig.add_subplot(212)
    plt.style.use('seaborn')

    ax_cluster = [ax_cluster1, ax_cluster2]

    for index in nodes:
        node = nodes[index]

        # identify define cluster
        cluster_define = get_cluster(node.get('defining resource'))

        # define color
        print(node)
        name = "{}({})".format(node.get('action'),node.get('id'))

        if(node.get('phase') == '0'):
            color_define = 'blue'
            color_observe = 'red'
        elif(node.get('phase') == '1'):
            color_define = 'cyan'
            color_observe = 'pink'
        else:  # assuming 0,1
            color_define = 'blue'
            color_observe = 'pink'

        print("{}:".format(name))

        # draw define buffer
        x1 = int(node.get('define', 0))
        y1 = int(node.get('define memory offset', 0))
        x2 = int(node.get('end_define', 0))
        y2 = y1 + int(node.get('elementsize', 0))

        print("cluster:{} ({},{}) ({},{})".format(cluster_define, x1, y1, x2, y2))
        ax_cluster[cluster_define].scatter(
            (x1, x2), (y1, y2), c=color_define, marker=',', s=0.1)
        ax_cluster[cluster_define].add_patch(Rectangle((x1, y1),
                               x2-x1, y2-y1,
                               fc=color_define,
                               ec=color_define,
                               #lw=10
        ))
        plt.show(block=False)

        # identify observer's cluster
        cluster_observes = list()
        if node.get('observe memory offset', []):
            # search observer localisation
            for key_obs in nodes:
                obs_list = nodes[key_obs].get('obs_ids', [])
                for (obs, pos) in obs_list:
                    if obs == node.get('id'):
                        resource = nodes[key_obs]['defining resource']
                        print("found obs {} run on {}".format(nodes[key_obs]['id'], resource))
                        cluster_observes.append(get_cluster(resource))
        else:
            # no data mvt, observer(s) are in the same cluster as definer
            cluster_observes.append(cluster_define)

        # draw observer buffer
        for cluster_observe in list(set(cluster_observes)):

            # observed bloc
            x1 = int(node.get('observe_start', 0))
            y1 = int(node.get('observe memory offset', node.get('define memory offset', 0)))
            x2 = int(node.get('observe_end', 0))
            y2 = y1 + int(node.get('elementsize', 0))

            print("cluster:{} ({},{}) ({},{})".format(cluster_observe, x1, y1, x2, y2))
            ax_cluster[cluster_observe].scatter(
                (x1, x2), (y1, y2), c=color_observe, marker=',', s=0.1)
            ax_cluster[cluster_observe].add_patch(Rectangle((x1, y1),
                                   x2-x1, y2-y1,
                                   fc=color_observe,
                                   ec=color_observe,
                                   #lw=10
            ))
            plt.show(block=False)

            # arrow
            # r = draw.Line(
            #     x1/ratio_x, y1/ratio_y, x2/ratio_x, y2/ratio_y, width=10
            # )
            #print("Line: ({},{}) ({},{})".format(
            #    x1/ratio_x, y1/ratio_y, x2/ratio_x, y2/ratio_y,
            #))

        input("Press one key to continue")


filename = 'CCL_file_2cblk.txt'
# filename = 'ccl_file_12May22.txt'
# filename = 'CCL_file_test_smem_svg.txt'

# parse ccl file: produce nodes dictionnary
def test_draw_smem_layout():
    nodes = ccl_file_parser(filename)
    draw_svg(nodes)


test_draw_smem_layout()
