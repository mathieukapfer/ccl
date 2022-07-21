
import matplotlib.pyplot as plt
from ccl_parser.ccl_parse2 import ccl_file_parser


def stat_create_events(nodes):
    """
    input:
        nodes: dictionary of ccl file stream

    return:
        list of event by cluster:
         - 'PE' event track PE usage change
         - 'smem' event track smem usage change
    """

    # list of events by cluster
    events = [[], []]

    for index in nodes:
        node = nodes[index]

        cluster = node.get('cluster')

        if (int(node.get('define', -1)) > 0 and
            int(node.get('define memory offset', -1)) > 0):

            # Handle super PE as 4 PE
            if node.get('defining resource')[0:3] == 'sPE':
                delta = 4
            else:
                delta = 1
            print(delta)

            # Create PE usage event
            events[cluster].append({
                'date': int(node.get('define')),
                'event': 'PE',
                'value': delta})

            events[cluster].append({
                'date': int(node.get('end_define')),
                'event': 'PE',
                'value': -delta})

            # Create 'smem used size' event
            # - increase when stream is processing
            delta = int(node.get('elementsize')) + int(node.get('internal memory'))
            events[cluster].append({
                'date': int(node.get('define')),
                'event': 'smem',
                'value': delta})

            # - decrease when stream is moved outside cluster or no more observed
            events[cluster].append({
                'date': int(node.get('L2toDDR',
                                     node.get('L2toL2',
                                              node.get('observe_end'
                                              )))),
                'event': 'smem',
                'value': -delta})

    return events


def stat_integrated_events(sorted_events, rate=1):
    """
    input:
        sorted_event:  list of event sorted by date

    return:
        list of point (x,y) corresponding to the integration of events on date
    """
    # init
    integrated_value = 0
    date = 0
    previous_integrated_value = 0
    previous_date = 0
    x = list()
    y = list()

    # integrate events
    for event in sorted_events:
        date = event['date']

        print("time:{}, integrated value:{}".format(
            event['date'], integrated_value))

        if (previous_date != date):
            # added new point previously computed
            print("plot {},{}, {},{}".format(
                previous_date, integrated_value,
                previous_date, previous_integrated_value,
            ))
            # add rise or falling 'edge' points (same date)
            x.append(previous_date)
            y.append(previous_integrated_value/rate)
            x.append(previous_date)
            y.append(integrated_value/rate)
            previous_date = date
            previous_integrated_value = integrated_value

        # sum each event of the same date
        integrated_value += event['value']
        print("delta {},{}".format(date, integrated_value))

    # add last point
    x.append(date)
    y.append(previous_integrated_value/rate)
    x.append(date)
    y.append(integrated_value/rate)

    return x, y


def draw_stat_events(events, ax):
    """
    Integrate events and display its
    """

    axis = list()

    # Create 'nb PEs' curve
    for events_by_cluster in events:

        # extract event by cluster and sorted by date
        cluster = events.index(events_by_cluster)
        sorted_cluster_events = sorted(events_by_cluster, key=lambda item: item['date'])

        print(sorted_cluster_events)

        # define axis
        ax2 = ax[cluster].twinx()
        ax1 = ax[cluster]

        # draw PE usage
        sorted_events = [event for event in sorted_cluster_events if event['event'] == 'PE']
        x, y = stat_integrated_events(sorted_events, 16/100)
        # ax2 = ax[cluster]
        ax2.plot(
            x, y,
            linewidth=1, marker='.', c='blue', markersize=0)
        ax2.yaxis.label.set_color('blue')
        ax2.set_ylabel("% nb PEs")
        ax2.set_ylim([0, 100])
        ax2.fill_between(x, y, 0, color='blue', alpha=.1)
        # ax2.spines['right'].set_color('blue')
        [t.set_color('blue') for t in ax2.yaxis.get_ticklabels()]
        # ax2.tick_params(axis='y', length=4.0)

        # draw smem usage
        sorted_events = [event for event in sorted_cluster_events if event['event'] == 'smem']
        x, y = stat_integrated_events(sorted_events, 2*1024*1024/100)

        # plot cluster curve
        ax1.plot(
            x, y,
            linewidth=1, marker='.', c='green', markersize=0)
        ax1.yaxis.label.set_color('green')
        ax1.set_ylabel("% SMEM")
        ax1.set_ylim([0, 100])
        ax1.fill_between(x, y, 0, color='green', alpha=.3)
        # ax1.spines['left'].set_color('green')
        [t.set_color('green') for t in ax1.yaxis.get_ticklabels()]

        axis.append([ax1, ax2])

    return axis


# filename = "data/CCL_file_phase3.txt"
filename = "data/ToKalray12JUL22/CCL_file.txt"    # Rx + Tx
# filename = "data/ToKalray05JUL22/CCL_file.txt"  # working memory
# filename = "data/ToKalray07JUL22/CCL_file.txt"  # Tx
# filename = "data/ToKalray07JUL22/CCL_file_extract_broadcast.txt"
# filename = 'data/CCL_file_2cblk.txt'
# filename = 'data/ccl_file_12May22.txt'
# filename = 'data/CCL_file_test_smem_svg.txt'


def draw_stat(nodes, ax):
    events = stat_create_events(nodes)
    print(events)
    return draw_stat_events(events, ax)


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
    print(nodes)

    # draw stat
    draw_stat(nodes, ax)

    # show
    plt.show(block=False)


# test_stat()
