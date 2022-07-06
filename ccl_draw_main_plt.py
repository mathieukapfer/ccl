import re

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Rectangle

from ccl_parser.ccl_parse2 import ccl_file_parser


def draw_rectangle(ax, color, x1, y1, x2, y2):
    """
    Draw plot and rectangle as patch
    """
    ax.scatter(
        (x1, x2), (y1, y2), c=color, marker=',', s=0.1)
    ax.add_patch(
        Rectangle((x1, y1),
                  x2-x1, y2-y1,
                  fc=color,
                  ec=color,
                  #lw=10
                  ))
    print("({},{}) ({},{})".format(x1, y1, x2, y2))


def push_draw_arrow_request(queue, cluster_tail, cluster_head, x1, y1, x2, y2):
    """
    Push arrow request to be draw at the end
    """
    queue.append((cluster_tail, cluster_head, x1, y1, x2, y2))
    return queue


def draw_arrow(fig, cluster_tail, cluster_head, x1, y1, x2, y2):
    """
    Draw cross figure arrow
    see: https://www.cilyan.org/blog/2016/01/23/matplotlib-draw-between-subplots/
    """
    # Create the arrow
    # 1. Get transformation operators for axis and figure
    ax0tr = cluster_tail.transData  # Axis 0 -> Display
    ax1tr = cluster_head.transData  # Axis 1 -> Display
    figtr = fig.transFigure.inverted()  # Display -> Figure
    # 2. Transform arrow start point from axis 0 to figure coordinates
    ptB = figtr.transform(ax0tr.transform((x1, y1)))
    # 3. Transform arrow end point from axis 1 to figure coordinates
    ptE = figtr.transform(ax1tr.transform((x2, y2)))
    # 4. Create the patch
    arrow = mpl.patches.FancyArrowPatch(
        ptB, ptE, transform=fig.transFigure,  # Place arrow in figure coord system
        fc = "g", connectionstyle="arc3,rad=0.2", arrowstyle='simple', alpha = 0.3,
        mutation_scale = 40.
    )
    # 5. Add patch to list of objects to draw onto the figure
    fig.patches.append(arrow)


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
    arrows = list()

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

        print("Define: cluster:{}".format(cluster_define))
        draw_rectangle(ax_cluster[cluster_define], color_define, x1, y1, x2, y2)
        plt.show(block=False)

        # draw shadow region
        # - move to DDR:           end_define -> L2toDDR,
        # - move to other cluster: end_define -> L2toL2,
        # - same cluster:          end_define -> observe_start
        x1 = x2
        x2 = int(node.get('L2toL2', node.get('L2toDDR', node.get('observe_start'))))
        print("Shadow: cluster:{}".format(cluster_define))
        draw_rectangle(ax_cluster[cluster_define], 'gray', x1, y1, x2, y2)

        # keep data to draw arrow
        def_x2 = x2
        def_y2 = y2

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
            y1 = int(node.get('observe memory offset', node.get('define memory offset', -1)))
            x2 = int(node.get('observe_end', 0))
            y2 = y1 + int(node.get('elementsize', 0))

            if y1 >= 0:
                print("Observe: cluster:{}".format(cluster_observe))
                draw_rectangle(ax_cluster[cluster_observe], color_observe, x1, y1, x2, y2)

            # draw shadow region
            # - move from DDR:           DDRtoL2 -> observe_start
            # - move from other cluster: L2toL2  -> observe_start
            # note that y1 and y2 is the same as previous ones
            x1 = int(node.get('L2toL2', node.get('DDRtoL2', -1)))
            x2 = int(node.get('observe_start', 0))
            if x1 >= 0:
                print("Shadow: cluster:{}".format(cluster_observe))
                draw_rectangle(ax_cluster[cluster_observe], 'gray', x1, y1, x2, y2)
                arrows = push_draw_arrow_request(arrows,
                    ax_cluster[cluster_define], ax_cluster[cluster_observe],
                    def_x2, def_y2, x1, y1
                )

        plt.show(block=False)

        input("Press one key to continue")

    # draw arrow cross axes
    for arrow in arrows:
        draw_arrow(fig, arrow[0], arrow[1], arrow[2], arrow[3], arrow[4], arrow[5])

    plt.show(block=False)


# filename = 'CCL_file_2cblk.txt'
# filename = 'ccl_file_12May22.txt'
filename = 'CCL_file_test_smem_svg.txt'

# parse ccl file: produce nodes dictionnary
def test_draw_smem_layout():
    nodes = ccl_file_parser(filename)
    draw_svg(nodes)


test_draw_smem_layout()
