import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import Rectangle


def demo_anotation():

    ax = plt.subplot()

    t = np.arange(0.0, 5.0, 0.01)
    s = np.cos(2*np.pi*t)

    line, = plt.plot(t, s, lw=2)

    plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
                 arrowprops=dict(facecolor='black', shrink=0.05),
    )

    plt.ylim(-2, 2)
    plt.show()


def demo_keyword_string():
    data = {'a': np.arange(50),
        'c': np.random.randint(0, 50, 50),
        'd': np.random.randn(50)}
    data['b'] = data['a'] + 10 * np.random.randn(50)
    data['d'] = np.abs(data['d']) * 100

    plt.scatter('a', 'b', c='c', s='d', data=data)
    plt.xlabel('entry a')
    plt.ylabel('entry b')
    plt.show()


def demo_keyword_string():
    data = {'a': np.arange(50),
        'c': np.random.randint(0, 50, 50),
        'd': np.random.randn(50)}
    data['b'] = data['a'] + 10 * np.random.randn(50)
    data['d'] = np.abs(data['d']) * 100

    plt.scatter('a', 'b', c='c', s='d', data=data)
    plt.xlabel('entry a')
    plt.ylabel('entry b')
    plt.show()


def demo_rectangle():

    # The image
    X = np.arange(16).reshape(4, 4)

    # highlight some feature in the
    # middle boxes.
    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.imshow(X, cmap = plt.cm.gray, interpolation ='nearest')
    ax.add_patch(Rectangle((0.5, 0.5),
                           2, 2,
                           fc ='none',
                           ec ='g',
                           lw = 10))

    plt.show()
