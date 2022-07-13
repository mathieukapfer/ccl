import matplotlib.pyplot as plt
from ccl_parser.ccl_parse2 import ccl_file_parser


def draw_stat(nodes, ax):


    # list of events by cluster
    events = [[], []]

    # 1 - Create events list
    for index in nodes:
        node = nodes[index]

        # create event
        cluster = get_cluster(node.get('defining resource'))

        if int(node.get('define', -1)) > 0:
            events[cluster].append({
                'date': int(node.get('define')),
                'event': 'PE',
                'value': 1})

            events[cluster].append({
                'date': int(node.get('end_define')),
                'event': 'PE',
                'value': -1})

    # 2 - Create nb PEs curve
    for events_by_cluster in events:

        cluster = events.index(events_by_cluster)
        sorted_events = sorted(events_by_cluster, key=lambda item: item['date'])

        print(sorted_events)

        #
        nb_active_pes = 0
        date = 0
        previous_nb_active_pes = 0
        previous_date = 0
        x = list()
        y = list()

        for event in sorted_events:
            date = event['date']

            print("cluster:{}, time:{}, #PE:{}".format(
                cluster, event['date'], nb_active_pes))

            if (previous_date != date):
                # added new point previously computed
                print("plot {},{}, {},{}".format(
                    previous_date, nb_active_pes,
                    previous_date, previous_nb_active_pes,
                ))
                x.append(previous_date)
                y.append(previous_nb_active_pes)
                x.append(previous_date)
                y.append(nb_active_pes)
                previous_date = date
                previous_nb_active_pes = nb_active_pes

            # sum each event of the same date
            nb_active_pes += event['value']
            print("delta {},{}".format(date, nb_active_pes))

        # add last point
        x.append(date)
        y.append(previous_nb_active_pes)
        x.append(date)
        y.append(nb_active_pes)

        # plot cluster curve
        ax[cluster].plot(
            x, y,
            linewidth=2, marker='o', c='black', markersize=2)

        plt.show(block=False)


# filename = "data/CCL_file_phase3.txt"
filename = "data/ToKalray05JUL22/CCL_file.txt"  # working memory
# filename = "data/ToKalray07JUL22/CCL_file.txt"  # Tx
# filename = "data/ToKalray07JUL22/CCL_file_extract_broadcast.txt"
# filename = 'data/CCL_file_2cblk.txt'
# filename = 'data/ccl_file_12May22.txt'
# filename = 'data/CCL_file_test_smem_svg.txt'

def test_stat():
    """
    """
    fig = plt.figure()

    # stats by cluster
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax = [ax1, ax2]

    # parse ccl file
    nodes = ccl_file_parser(filename)

    # draw stat
    return draw_stat(nodes, ax)


test_stat()
