import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()

t = np.arange(0.01, 5.0, 0.01)
s1 = np.sin(2 * np.pi * t)
s2 = np.exp(-t)
s3 = np.sin(4 * np.pi * t)

ax_cluster1 = plt.subplot(411, ylabel='cluster 1')
plt.plot(t, s1)
plt.tick_params('x', labelbottom=False)
ax_cluster1_stat = plt.subplot(412, sharex=ax_cluster1)

#ax_cluster1_stat.set_aspect(0.05)
ax_cluster2 = plt.subplot(413)
ax_cluster2_stat = plt.subplot(414, sharex=ax_cluster2)

plt.show(block=False)
