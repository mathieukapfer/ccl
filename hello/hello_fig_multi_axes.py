import matplotlib.pyplot as plt
fig, ax1 = plt.subplots()

plt.style.use('classic')

ax1.plot([1, 2, 3, 4, 5], [3, 5, 7, 1, 9], color='red')
ax1.set_ylabel("blabla")

ax2 = ax1.twinx()
ax2.plot([11, 12, 31, 41, 15], [13, 51, 17, 11, 76], color='blue')
ax2.set_ylabel("houlala")

fig.tight_layout()
plt.show()
