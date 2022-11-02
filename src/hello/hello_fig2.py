import matplotlib.pyplot as plt


def annotate_axes(ax, text, fontsize=18):
    ax.text(0.5, 0.5, text, transform=ax.transAxes,
            ha="center", va="center", fontsize=fontsize, color="darkgrey")


gs_kw = dict(width_ratios=[2, 1], height_ratios=[1, 2])
fig, axd = plt.subplot_mosaic([['upper left', 'upper right'],
                               ['lower left', 'lower right']],
                              gridspec_kw=gs_kw, figsize=(5.5, 3.5),
                              constrained_layout=True)

for k in axd:
    annotate_axes(axd[k], f'axd["{k}"]', fontsize=14)


fig.suptitle('plt.subplot_mosaic()')

plt.show(block=False)
