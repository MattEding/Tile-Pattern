import matplotlib.pyplot as plt
import numpy as np

from .parser import pattern_to_array


def plot_square(xy, val, color, **kwargs):
    square = plt.Rectangle(xy, facecolor=color, 
                           width=1, height=1, edgecolor='black', linewidth=3, **kwargs)
    plt.gca().add_patch(square)


def plot_nonzero(arr, *, alpha=1, colormap=plt.cm.gist_ncar, **kwargs):
    values = np.unique(arr[arr > 0])
    colors = colormap(np.linspace(0, 1, values.size))  # does this preserve when dim=0? prolly not
    colormap = dict(zip(values, colors))
    xs, ys = np.nonzero(arr)
    for xy in zip(xs.flat, ys.flat):
        val = arr[xy]
        *rgb, _ = colormap[val]
        color = rgb + [alpha]
        plot_square(xy, val, color, **kwargs)


def plot_pattern(pattern, dim, *, val_to_dim, savepath=False, **kwargs):
    arr = pattern_to_array(pattern, dim, val_to_dim=val_to_dim)
    plt.figure(figsize=arr.shape)
    plot_nonzero(arr, **kwargs)
    plt.axis('equal')
    plt.axis('off')
