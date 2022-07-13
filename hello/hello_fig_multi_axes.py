import matplotlib.pyplot as plt
fig, ax1 = plt.subplots()
ax1.plot([1, 2, 3, 4, 5], [3, 5, 7, 1, 9], color='red')
ax2 = ax1.twinx()
ax2.plot([11, 12, 31, 41, 15], [13, 51, 17, 11, 76], color='blue')
fig.tight_layout()
plt.show()
