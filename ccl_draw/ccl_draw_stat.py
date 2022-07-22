
import matplotlib.pyplot as plt
from ccl_parser.ccl_parse2 import ccl_file_parser


def create_dma_event(date, event, value, isMaster):
    """
    Create dma events :
    Input: digest from CCL file:
       - date: start of dma tx
       - event: kind of dma tx (SMEM to SMEM, SMEM to DDR, DDR to SMEM)
       - value: data size
       - isMaster: DMA event shoudl be increment
    Return
       - two events for rising and falling edge for
           - DMA event (for master)
           - DMA bandwith usage: TODO
    """
    dma_event = list()

    # DMA model
    bus_througput = 16  # 16 B/cycle
    sabm_clock_duration = 1300  #

    # Compute bus load
    delta_time = value / bus_througput / sabm_clock_duration
    delta = 1  # means bus load is ON/OFF mode

    if (event == "L2toL2" or event == "L2toDDR" or event == "DDRtoL2"):
        rising_event = {'date': date, 'event': 'SMEM bus', 'value': delta}
        falling_event = {'date': date + delta_time, 'event': 'SMEM bus', 'value': -1 * delta}
        dma_event.extend([rising_event, falling_event])

    if (event == "L2toDDR" or event == "DDRtoL2"):
        rising_event = {'date': date, 'event': 'DDR bus', 'value': delta}
        falling_event = {'date': date + delta_time, 'event': 'DDR bus', 'value': -1 * delta}
        dma_event.extend([rising_event, falling_event])


    # Compute DMA master event
    if(isMaster):
        # adding rising and falling edge for 'DMA (master) event'
        delta = 1
        rising_event = {'date': date, 'event': 'DMA event', 'value': delta}
        falling_event = {'date': date+1, 'event': 'DMA event', 'value': -1 * delta}
        dma_event.extend([rising_event, falling_event])


    return dma_event


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

        if int(node.get('define', -1)) >= 0:

            # Create PE and SMEM usage event
            if int(node.get('define memory offset', -1)) >= 0:

                # Handle super PE as 4 PE
                if node.get('defining resource')[0:3] == 'sPE':
                    delta = 4
                else:
                    delta = 1

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

            # Create DMA events
            HACK = True
            if(HACK):
                print("DMA processing of: {}".format(node))
                # L2 -> DDR
                if int(node.get('L2toDDR', -1)) >= 0:
                    new_events = create_dma_event(
                        date=int(node.get('L2toDDR')),
                        event='L2toDDR',
                        # TODO: handle elementsize of broadcasted stream
                        # TODO: same for all similar lines below
                        value=int(node.get('elementsize')),
                        isMaster=True)
                    print("DMA:cluster{}:{}".format(cluster, new_events))
                    events[cluster].extend(new_events)
                # DDR -> L2
                if int(node.get('DDRtoL2', -1)) >= 0:
                    clusters_obs = node.get('cluster_observes', [])
                    for cluster_obs in list(set(clusters_obs)):
                        new_events = create_dma_event(
                            date=int(node.get('DDRtoL2')),
                            event='DDRtoL2',
                            value=int(node.get('elementsize')),
                            isMaster=True)
                        print("DMA:cluster{}:{}".format(cluster_obs, new_events))
                        events[cluster_obs].extend(new_events)
                if int(node.get('L2toL2', -1)) >= 0:
                    # L2 -> L2 (send)
                    new_events = create_dma_event(
                        date=int(node.get('L2toL2')),
                        event='L2toL2',
                        value=int(node.get('elementsize')),
                        isMaster=False)
                    print("DMA:cluster{}:{}".format(cluster, new_events))
                    events[cluster].extend(new_events)
                    # L2 -> L2 (receive)
                    clusters_obs = node.get('cluster_observes', [])
                    for cluster_obs in list(set(clusters_obs)):
                        new_events = create_dma_event(
                            date=int(node.get('L2toL2')),
                            event='L2toL2',
                            value=int(node.get('elementsize')),
                            isMaster=True)
                        print("DMA:cluster{}:{}".format(cluster_obs, new_events))
                        events[cluster_obs].extend(new_events)


    return events


def stat_integrate_events_with_edge(sorted_events, rate=1):
    """
    input:
        sorted_event:  list of event sorted by date

    return:
        list of point (x,y) corresponding to the integration of events in time:
         - add event at the same date
         - produce rising and falling edge
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

    # By cluster
    for events_by_cluster in events:

        # extract event by cluster and sorted by date
        cluster = events.index(events_by_cluster)
        sorted_cluster_events = sorted(events_by_cluster, key=lambda item: item['date'])

        print(sorted_cluster_events)

        # define axis
        ax2 = ax[cluster].twinx()
        ax1 = ax[cluster]

        # draw % PE usage
        sorted_events = [event for event in sorted_cluster_events if event['event'] == 'PE']
        x, y = stat_integrate_events_with_edge(sorted_events)

        ax2.plot(x, y, linewidth=1, marker='.', c='blue', markersize=0)
        ax2.yaxis.label.set_color('blue')
        ax2.set_ylabel("nb PEs")
        ax2.set_ylim([0, 16])
        ax2.fill_between(x, y, 0, color='blue', alpha=.1)
        [t.set_color('blue') for t in ax2.yaxis.get_ticklabels()]

        # draw % smem usage
        sorted_events = [event for event in sorted_cluster_events if event['event'] == 'smem']
        x, y = stat_integrate_events_with_edge(sorted_events, 2*1024*1024/100)

        ax1.plot(x, y, linewidth=1, marker='.', c='green', markersize=0)
        ax1.yaxis.label.set_color('green')
        ax1.set_ylabel("% SMEM")
        ax1.set_ylim([0, 100])
        ax1.fill_between(x, y, 0, color='green', alpha=.3)
        [t.set_color('green') for t in ax1.yaxis.get_ticklabels()]

        # DMA
        ax_dma = ax[cluster+2]

        # draw % SMEM Bus usage
        sorted_events = [event for event in sorted_cluster_events if
                         event['event'] == 'SMEM bus']
        print("SMEM bus - Cluster {}: {}".format(cluster, sorted_events))
        x, y = stat_integrate_events_with_edge(sorted_events)

        color = 'orange'
        ax_dma.plot(x, y, linewidth=1, marker='.', c=color, markersize=0)
        # ax_dma.yaxis.label.set_color(color)
        # ax_dma.set_ylabel("SMEM bus")
        # ax_dma.set_ylim([0, 100])
        ax_dma.fill_between(x, y, 0, color=color, alpha=.1)
        #[t.set_color(color) for t in ax_dma.yaxis.get_ticklabels()]

        # draw % DDR Bus usage
        # working well but remove for figure clarity
        if False:
            sorted_events = [event for event in sorted_cluster_events if
                             event['event'] == 'DDR bus']
            print("DDR bus - Cluster {}: {}".format(cluster, sorted_events))
            x, y = stat_integrate_events_with_edge(sorted_events)

            color = 'darkred'
            ax_dma.plot(x, y, linewidth=1, marker='.', c=color, markersize=0)
            # ax_dma.yaxis.label.set_color(color)
            # ax_dma.set_ylabel("SMEM bus")
            # ax_dma.set_ylim([0, 100])
            ax_dma.fill_between(x, y, 0, color=color, alpha=.1)
            #[t.set_color(color) for t in ax_dma.yaxis.get_ticklabels()]

        # draw % DMA event
        sorted_events = [event for event in sorted_cluster_events if
                         event['event'] == 'DMA event']
        print("DMA event - Cluster {}: {}".format(cluster, sorted_events))
        x, y = stat_integrate_events_with_edge(sorted_events)
        color = 'darkorange'
        ax_dma.plot(x, y, '--', linewidth=1, c=color, markersize=0)
        ax_dma.yaxis.label.set_color(color)
        ax_dma.set_ylabel("DMA event\n& buses")
        # ax_dma.set_ylim([0, 100])
        #ax_dma.fill_between(x, y, 0, color=color, alpha=.1)
        #[t.set_color(color) for t in ax_dma.yaxis.get_ticklabels()]

        # return axis for final rendering
        axis.append([ax1, ax2, ax_dma])

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
    """
    Produce statistic on data streams
    input:
       - nodes: data streams dictionary
       - ax: list of axes to display statistics, one per cluster
    """
    events = stat_create_events(nodes)
    # print(events)
    return draw_stat_events(events, ax)


def test_stat():
    """
    Unit test of 'draw_stat' function
    """
    fig = plt.figure()

    # stats by cluster
    ax1 = fig.add_subplot(411)
    ax2 = fig.add_subplot(412)
    # ax = [ax1, ax2]
    ax3 = fig.add_subplot(413)
    ax4 = fig.add_subplot(414)
    ax = [ax1, ax2, ax3, ax4]

    # parse ccl file
    nodes = ccl_file_parser(filename)
    print(nodes)

    # draw stat
    draw_stat(nodes, ax)

    # show
    plt.show(block=False)


test_stat()
