
import matplotlib.pyplot as plt
from ccl_parser.ccl_parse2 import ccl_file_parser

import logging

# create logger
logger = logging.getLogger("ccl.viewer.stat")


# const
SMEM_rate = 2*1024*1024/100  # percent of 2MB memory


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

    # check
    if value == 0:
        logger.warning("Warning: DMA {} with null size at time: {} [ismaster={}]".format(
            event, date, isMaster))

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
    if isMaster:
        # adding rising and falling edge for 'DMA (master) event'
        delta = 1
        rising_event = {'date': date, 'event': 'DMA event', 'value': delta}
        falling_event = {'date': date+1, 'event': 'DMA event', 'value': -1 * delta}
        dma_event.extend([rising_event, falling_event])

    return dma_event


def stat_create_events(nodes, max_cluster):
    """
    input:
        nodes: dictionary of ccl file stream

    return:
        list of event by cluster:
         - 'PE' event track PE usage change
         - 'smem' event track smem usage change
    """

    # list of events by cluster
    events = [[] for i in range(max_cluster + 1)]

    for index in nodes:
        node = nodes[index]

        cluster = node.get('cluster')

        if int(node.get('define', -1)) >= 0:

            # Create PE and SMEM usage event
            if int(node.get('define memory offset', -1)) >= 0:

                # for debug purpose
                streamId = int(node.get('id', -1))

                # Handle super PE as 4 PE
                if node.get('defining resource')[0:3] == 'sPE':
                    delta = 4
                else:
                    delta = 1

                # Create PE usage event
                events[cluster].append({
                    'id': streamId,
                    'date': int(node.get('define')),
                    'event': 'PE',
                    'value': delta})

                events[cluster].append({
                    'id': streamId,
                    'date': int(node.get('end_define')),
                    'event': 'PE',
                    'value': -delta})

                # Create 'smem used size' event
                # - increase when stream is processing
                if (int(node.get('internal memory offset', -1)) > 0):
                    delta = int(node.get('elementsize')) + int(node.get('internal memory', 0))
                    events[cluster].append({
                        'id': streamId,
                        'date': int(node.get('define')),
                        'event': 'smem',
                        'value': delta})

                    # - decrease when stream is moved outside cluster or no more observed
                    events[cluster].append({
                        'id': streamId,
                        'date': int(node.get('L2toDDR',
                                             node.get('L2toL2',
                                                      node.get('observe_end'
                                                      )))),
                        'event': 'smem',
                        'value': -delta})

            # Create DMA events
            HACK = True
            if(HACK):
                logger.debug("DMA processing of: {}".format(node))
                logger.info("DMA processing of id: {}".format(node.get('id')))
                # L2 -> DDR
                if int(node.get('L2toDDR', -1)) >= 0:
                    new_events = create_dma_event(
                        date=int(node.get('L2toDDR')),
                        event='L2toDDR',
                        # TODO: handle elementsize of broadcasted stream
                        # TODO: same for all similar lines below
                        value=int(node.get('elementsize')),
                        isMaster=True)
                    logger.info("DMA:cluster{}:{}".format(cluster, new_events))
                    events[cluster].extend(new_events)
                # DDR -> L2
                if int(node.get('DDRtoL2', -1)) >= 0:
                    clusters_obs = node.get('cluster_observes', [])
                    for cluster_obs in list(set(clusters_obs)):
                        new_events = create_dma_event(
                            date=int(node.get('DDRtoL2')),
                            event='DDRtoL2',
                            value=int(node.get('elementsize',0)),
                            isMaster=True)
                        logger.info("DMA:cluster{}:{}".format(cluster_obs, new_events))
                        events[cluster_obs].extend(new_events)
                if int(node.get('L2toL2', -1)) >= 0:
                    # L2 -> L2 (send)
                    new_events = create_dma_event(
                        date=int(node.get('L2toL2')),
                        event='L2toL2',
                        value=int(node.get('elementsize', 0)),
                        isMaster=False)
                    logger.info("DMA:cluster{}:{}".format(cluster, new_events))
                    events[cluster].extend(new_events)
                    # L2 -> L2 (receive)
                    clusters_obs = node.get('cluster_observes', [])
                    for cluster_obs in list(set(clusters_obs)):
                        new_events = create_dma_event(
                            date=int(node.get('L2toL2')),
                            event='L2toL2',
                            value=int(node.get('elementsize',0)),
                            isMaster=True)
                        logger.info("DMA:cluster{}:{}".format(cluster_obs, new_events))
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

        logger.debug("time:{}, integrated value:{}".format(
            event['date'], integrated_value))

        if (previous_date != date):
            # added new point previously computed
            logger.debug("plot {},{}, {},{}".format(
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
        # logger.debug(event)
        integrated_value += event['value']
        logger.debug("delta {},{}".format(date, integrated_value))

    # add last point
    x.append(date)
    y.append(previous_integrated_value/rate)
    x.append(date)
    y.append(integrated_value/rate)

    return x, y


def draw_stat_ax(ax, x, y, color, style='-', ylabel=0, ylim=0, alpha=0.1):
    """
    Helper to plot one stat ax
    input
      - ax:     the ax to plot where
      - x, y:   the data to plot
      - color:  color of plot
      - ylabel: title of y axe
      - ylim:   [min, max] value
      - alpha:  transpapance level of color below the curve
    """
    ax.plot(x, y, linewidth=1, marker=".", linestyle=style, c=color, markersize=0)
    if ylabel:
        ax.set_ylabel(ylabel)
        ax.yaxis.label.set_color(color)
    if ylim:
        ax.set_ylim(ylim)
    ax.fill_between(x, y, 0, color=color, alpha=alpha)
    [t.set_color(color) for t in ax.yaxis.get_ticklabels()]


def draw_stat_events(events, stat_axis, dma_axis):
    """
    Integrate events and display its
    """

    axis = list()

    # By cluster
    for events_by_cluster in events:

        # extract event by cluster and sorted by date
        cluster = events.index(events_by_cluster)
        sorted_cluster_events = sorted(events_by_cluster, key=lambda item: item['date'])

        logger.debug(sorted_cluster_events)

        # define axis
        logger.debug("cluster={}".format(cluster))
        ax_stat_pe = stat_axis[cluster].twinx()
        ax_stat_smem = stat_axis[cluster]

        # draw % PE usage
        sorted_events = [event for event in sorted_cluster_events if event['event'] == 'PE']
        x, y = stat_integrate_events_with_edge(sorted_events)
        draw_stat_ax(ax_stat_pe, x, y, 'blue', "-", "nbPEs", [0, 16], 0.1)

        # draw % smem usage
        sorted_events = [event for event in sorted_cluster_events if event['event'] == 'smem']
        x, y = stat_integrate_events_with_edge(sorted_events, SMEM_rate)
        draw_stat_ax(ax_stat_smem, x, y, 'green', "-", "% SMEM", [0, 100], .3)

        # DMA
        ax_dma = dma_axis[cluster]

        # draw % SMEM Bus usage
        sorted_events = [event for event in sorted_cluster_events if
                         event['event'] == 'SMEM bus']
        x, y = stat_integrate_events_with_edge(sorted_events)
        draw_stat_ax(ax_dma, x, y, 'orange', "-", alpha=0.1)

        # draw % DDR Bus usage
        # working well but remove to get a lighter graph
        if False:
            sorted_events = [event for event in sorted_cluster_events if
                             event['event'] == 'DDR bus']
            draw_stat_ax(ax_dma, x, y, 'darkred', "-", alpha=0.1)

        # draw % DMA event
        sorted_events = [event for event in sorted_cluster_events if
                         event['event'] == 'DMA event']
        x, y = stat_integrate_events_with_edge(sorted_events)
        draw_stat_ax(ax_dma, x, y, 'darkorange', style='--', ylabel='DMA event\n& buses')

        # return axis for final rendering
        axis.append([ax_stat_smem, ax_stat_pe, ax_dma])

    return axis


# filename = "data/CCL_file_phase3.txt"
# filename = "data/ToKalray12JUL22/CCL_file.txt"    # Rx + Tx
# filename = "data/ToKalray05JUL22/CCL_file.txt"  # working memory
# filename = "data/ToKalray07JUL22/CCL_file.txt"  # Tx
# filename = "data/ToKalray07JUL22/CCL_file_extract_broadcast.txt"
# filename = 'data/CCL_file_2cblk.txt'
# filename = 'data/ccl_file_12May22.txt'
# filename = 'data/CCL_file_test_smem_svg.txt'
# filename = "data/CCL_file_phase3_only_broadcast.txt"
filename = "data/ToKalray04AUG22/CCL_file_RxTx.txt"


def draw_stat(nodes, max_cluster, stat_axis, dma_axis):
    """
    Produce statistic on data streams
    input:
       - nodes: data streams dictionary
       - ax: list of axes to display statistics, one per cluster
    """
    events = stat_create_events(nodes, max_cluster)
    # logger.debug(events)
    return draw_stat_events(events, stat_axis, dma_axis)


def test_stat():
    """
    Unit test of 'draw_stat' function
    """
    fig = plt.figure()

    # parse ccl file
    nodes = ccl_file_parser(filename)
    # logger.debug(nodes)

    # check nb clusters
    max_cluster = 0
    for node_index in nodes:
        node = nodes[node_index]
        if node['cluster'] > max_cluster:
            max_cluster = node['cluster']

    logger.debug("max cluster: {}".format(max_cluster))

    # stats by cluster
    stat_axis = list()
    dma_axis = list()
    for cluster in range(0, max_cluster + 1):
        logger.debug("{}{}{}".format(
            2, max_cluster + 1, 1 + cluster)
        )
        stat_axis.append(fig.add_subplot(
            2, max_cluster + 1, 1 + cluster)
        )
        logger.debug("{}{}{}".format(
            2, max_cluster + 1, max_cluster + 2 + cluster)
        )
        dma_axis.append(fig.add_subplot(
            2, max_cluster + 1, max_cluster + 2 + cluster)
        )

    # draw stat
    logger.debug("stat_axis: {}".format(stat_axis))
    draw_stat(nodes, max_cluster, stat_axis, dma_axis)

    # show
    plt.show(block=False)


# test_stat()
