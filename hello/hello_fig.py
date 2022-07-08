import matplotlib.pyplot as plt

fig = plt.figure()

ax_cluster1 = fig.add_subplot(411, ylabel='cluster 1')
ax_cluster1_stat = fig.add_subplot(412, sharex=ax_cluster1)

ax_cluster1_stat.set_aspect(0.05)
ax_cluster1_stat.sharex = ax_cluster1

ax_cluster2 = fig.add_subplot(413)
ax_cluster2_stat = fig.add_subplot(414, sharex=ax_cluster2)

plt.show(block=False)
