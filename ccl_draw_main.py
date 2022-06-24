import drawSvg as draw
import re

from ccl_parser.ccl_graph2 import build_stream_graph
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
    d = draw.Drawing(2000, 2000, origin=(0,0), displayInline=False)
    for index in nodes:
        ratio_x = 10
        ratio_y = 1000
        node = nodes[index]

        # identify define cluster
        cluster_define = get_cluster(node.get('defining resource'))

        # draw memory zone
        offset_phase_define = 1000 * cluster_define

        print(node)
        name = "{}({})".format(node.get('action'),node.get('id'))

        if(node.get('phase') == '0'):
            color_define = 'blue'
            color_observe = 'red'
            ratio_phase_define = 1
            ratio_phase_observe = 1
        elif(node.get('phase') == '1'):
            color_define = 'cyan'
            color_observe = 'pink'
            ratio_phase_define = 1
            ratio_phase_observe = 1
        else:  # assuming 0,1
            color_define = 'blue'
            color_observe = 'pink'
            ratio_phase_define = 1
            ratio_phase_observe = 1

        print("{}:".format(name))

        # draw define buffer
        x1 = int(node.get('define', 0))
        y1 = int(node.get('define memory offset', 0))
        width1 = int(node.get('end_define', 0)) - x1
        height1 = int(node.get('elementsize', 0))
        r1 = draw.Rectangle(
            x1/ratio_x + offset_phase_define, y1/ratio_y, width1/ratio_x, height1/ratio_y/ratio_phase_define,
            border='gray', fill=color_define)
        print("({},{}) ({},{})".format(
            x1/ratio_x + offset_phase_define, y1/ratio_y, width1/ratio_x, height1/ratio_y/ratio_phase_define,
        ))

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
        for cluster_observer in list(set(cluster_observes)):
            offset_phase_observe = 1000 * cluster_observer

            # observed bloc
            x2 = int(node.get('observe_start', 0))
            y2 = int(node.get('observe memory offset', node.get('define memory offset', 0)))
            width2 = int(node.get('observe_end', 0)) - x2
            height2 = int(node.get('elementsize', 0))

            r2 = draw.Rectangle(
                x2/ratio_x + offset_phase_observe, y2/ratio_y,
                width2/ratio_x, height2/ratio_y/ratio_phase_observe,
                border='black', fill=color_observe)
            print("({},{}) ({},{})".format(
                x2/ratio_x + offset_phase_observe, y2/ratio_y,
                width2/ratio_x, height2/ratio_y/ratio_phase_observe,
            ))

            # outline
            # r = draw.Rectangle(
            #     x1/ratio_x + offset_phase_define, y1/ratio_y, (x2 - x1 + width2 + offset_phase_observe)/ratio_x, height2 / ratio_y,
            #     fill='gray')
            # print("({},{}) ({},{})".format(
            #     x1/ratio_x, y1/ratio_y, (x2 - x1 + width2)/ratio_x, height2 / ratio_y,
            # ))
            #d.append(r)

            # arrow
            r = draw.Line(
                x1/ratio_x, y1/ratio_y, x2/ratio_x, y2/ratio_y, width=10
            )
            print("Line: ({},{}) ({},{})".format(
                x1/ratio_x, y1/ratio_y, x2/ratio_x, y2/ratio_y,
            ))

            d.append(r)

        d.append(r1)
        d.append(r2)

        # add label
        d.append(draw.Text(name, 20, x1/ratio_x + offset_phase_define, y1/ratio_y, fill='black'))

        d.saveSvg('example.svg')
        input("Press one key to continue")


filename = 'CCL_file_2cblk.txt'
# filename = 'ccl_file_12May22.txt'
# filename = 'CCL_file_test_smem_svg.txt'

# parse ccl file: produce nodes dictionnary
nodes = ccl_file_parser(filename)
draw_svg(nodes)
