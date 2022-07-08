import matplotlib.pyplot as plt

# prepare conntent
t = np.arange(0.01, 5.0, 0.01)
s1 = np.sin(2 * np.pi * t)
s2 = np.exp(-t)
s3 = np.sin(4 * np.pi * t)
s4 = np.sin(2 * np.pi * t)

# helper
def annotate_axes(ax, text, fontsize=18):
    ax.text(0.5, 0.5, text, transform=ax.transAxes,
            ha="center", va="center", fontsize=fontsize, color="darkgrey")


# create axes
# - define ratio
gs_kw = dict(width_ratios=[1], height_ratios=[5, 1, 5, 1])
# - create axes
fig, axd = plt.subplot_mosaic([['cluster 1'], ['stat1'], ['cluster 2'], ['stat2']],
                              gridspec_kw=gs_kw, figsize=(5.5, 3.5),
                              constrained_layout=True)

# plot
axd['cluster 1'].plot(t, s2)
axd['stat1'].plot(t, s1)
axd['cluster 2'].plot(t, s3)
axd['stat2'].plot(t, s4)

# change properties
# - shared x axe
axd['cluster 1'].tick_params('x', labelbottom=False)
#axd['cluster 1'].set_xticklabels([])
#axd['cluster 1'].sharedx(axd['stat1'])
axd['stat1'].get_shared_x_axes().join(axd['stat1'],axd['cluster 1'])

axd['cluster 2'].tick_params('x', labelbottom=False)
axd['stat2'].get_shared_x_axes().join(axd['stat2'],axd['cluster 2'])


# add label
axd['cluster 1'].set_ylabel("cluster 1")
axd['stat1'].set_ylabel("stat1")


# add anotation
for k in axd:
    annotate_axes(axd[k], f'axd["{k}"]', fontsize=14)

fig.suptitle('plt.subplot_mosaic()')

plt.show(block=False)
