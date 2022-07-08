import re

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import ConnectionPatch

from ccl_parser.ccl_parse2 import ccl_file_parser


def draw_rectangle(ax, color, x1, y1, x2, y2):
    """
    Plot corner and adding rectangle as patch above
    """
    ax.scatter(
        (x1, x2), (y1, y2), c=color, marker=',', s=0.1)
    ax.add_patch(
        Rectangle((x1, y1),
                  x2-x1, y2-y1,
                  fc=color,
                  ec=color,
                  # lw=10
        ))
    print("({},{}) ({},{})".format(x1, y1, x2, y2))


def draw_arrow(fig, last_axes, axes_tail, axes_head, x1, y1, x2, y2, style):
    """
    Draw cross figure arrow
    https://matplotlib.org/3.1.0/gallery/userdemo/connect_simple01.html
    """
    con = ConnectionPatch(xyA=(x1, y1), coordsA='data', axesA=axes_tail,  # shrinkB=5
                          xyB=(x2, y2), coordsB='data', axesB=axes_head,
                          connectionstyle=style['connectionstyle'],
                          arrowstyle=style['arrowstyle'],
                          color=style['color']
    )
    print('Arrow {},{}->{},{}'.format(x1, y1, x2, y2))
    last_axes.add_artist(con)


def arrow_style(node):
    """
    Return style of arrow depending of node
    """
    # default value
    connectionstyle = "arc3,rad=0.2"
    arrowstyle = "->"
    color = 'black'

    # specific value
    if int(node.get('L2toL2', -1)) > 0:
        connectionstyle = "arc3,rad=0.1"
        arrowstyle = "->"
        color = 'black'
    elif int(node.get('L2toDDR', -1)) > 0:
        connectionstyle = "arc3,rad=0.3"
        arrowstyle = "->"
        color = 'red'
    return {
        'connectionstyle': connectionstyle,
        'arrowstyle': arrowstyle,
        'color': color
    }

def get_cluster(ressource_string):
    """
    Return last digit of 'define resource' known as cluster
    """
    m = re.match("([\w]+)_(\d)", ressource_string) # 'pe3_9'
    cluster = int(m[2])
    return cluster


def draw_svg(nodes):
    """
    Draw SMEM usage: x:time, y:addr
    """

    fig = plt.figure()
    ax_cluster1 = fig.add_subplot(211)
    ax_cluster2 = fig.add_subplot(212)
    plt.style.use('seaborn')

    ax_cluster = [ax_cluster1, ax_cluster2]

    for index in nodes:
        node = nodes[index]

        # identify define cluster
        cluster_define = get_cluster(node.get('defining resource'))

        print(node)

        # name = "{}({})".format(node.get('action'),node.get('id'))
        name_def = "{}({})".format(node.get('id'), node.get('phase-def'))
        name_obs = ">{}({})".format(node.get('id'), node.get('phase-obs'))

        # define color
        if(node.get('phase-def') == 0):
            color_define = '#FF0000'
        elif(node.get('phase') == 1):
            color_define = '#FF3333'
        else:  # assuming 2
            color_define = '#FF6666'

        if(node.get('phase-obs') == 0):
            color_observe = '#0000FF'
        elif(node.get('phase-obs') == 1):
            color_observe = '#3333FF'
        else:  # assuming 2
            color_observe = '#6666FF'

        #print("{}:".format(name))

        # draw define bloc
        x1 = int(node.get('define', 0))
        y1 = int(node.get('define memory offset', 0))
        x2 = int(node.get('end_define', 0))
        y2 = y1 + int(node.get('elementsize', 0))

        if y1 > 0:
            print("Define: cluster:{}".format(cluster_define))
            draw_rectangle(ax_cluster[cluster_define], color_define, x1, y1, x2, y2)
            ax_cluster[cluster_define].annotate(name_def, (x1, y1), fontsize=7)

        # draw working buffer bloc :
        # same timing as 'define bloc (x) , just other memory offset and size (y)
        y1m = int(node.get('internal memory offset', 0))
        y2m = y1m + int(node.get('internal memory', 0))

        if y1m > 0:
            print("Working buffer: cluster:{}".format(cluster_define))
            draw_rectangle(ax_cluster[cluster_define], 'green', x1, y1m, x2, y2m)
            ax_cluster[cluster_define].annotate(name_def, (x1, y1m), fontsize=7)

        # draw shadow region
        # same memory position (y) as 'define' bloc, just other timing(x)
        # - move to DDR:           end_define -> L2toDDR,
        # - move to other cluster: end_define -> L2toL2,
        # - same cluster:          end_define -> observe_start
        x1 = x2
        x2 = int(node.get('L2toL2', node.get('L2toDDR', node.get('observe_start'))))

        if y1 > 0:
            print("Shadow: cluster:{}".format(cluster_define))
            draw_rectangle(ax_cluster[cluster_define], 'gray', x1, y1, x2, y2)

        # keep data to draw arrow later
        def_x2 = x2
        def_y1 = y1

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

        # draw observer items
        for cluster_observe in list(set(cluster_observes)):

            # observer bloc
            x1 = int(node.get('observe_start', 0))
            y1 = int(node.get('observe memory offset', node.get('define memory offset', -1)))
            x2 = int(node.get('observe_end', 0))
            y2 = y1 + int(node.get('elementsize', 0))

            if y1 >= 0:
                print("Observe: cluster:{}".format(cluster_observe))
                draw_rectangle(ax_cluster[cluster_observe], color_observe, x1, y1, x2, y2)

            # draw shadow region & arrow
            # - move from DDR:           DDRtoL2 -> observe_start
            # - move from other cluster: L2toL2  -> observe_start
            # note that y1 and y2 is the same as previous ones
            x1 = int(node.get('L2toL2', node.get('DDRtoL2', -1)))
            x2 = int(node.get('observe_start', 0))
            if x1 >= 0:
                print("Shadow: cluster:{}".format(cluster_observe))
                # rectangle
                draw_rectangle(ax_cluster[cluster_observe], 'gray', x1, y1, x2, y2)
                # text
                ax_cluster[cluster_observe].annotate(name_obs, (x1, y1), fontsize=7)
                # arrow
                if def_y1 > 0:  # remove erroneous broadcast display [TMP]
                    draw_arrow(fig, ax_cluster[1],
                               ax_cluster[cluster_define], ax_cluster[cluster_observe],
                               def_x2, def_y1, x1, y1,
                               arrow_style(node)
                )

        plt.show(block=False)

        # input("Press one key to continue")


filename = "data/CCL_file_phase3.txt"
#filename = 'data/CCL_file_2cblk.txt'
# filename = 'data/ccl_file_12May22.txt'
# filename = 'data/CCL_file_test_smem_svg.txt'


def test_draw_smem_layout():
    """
    Display SMEM layout of CCLfile named 'filename'
    """
    nodes = ccl_file_parser(filename)
    draw_svg(nodes)


test_draw_smem_layout()
