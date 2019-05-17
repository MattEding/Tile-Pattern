import string

import matplotlib.pyplot as plt
import numpy as np

from .parser import pattern_to_array


def plot_square(xy, val, color, **kwargs):
    square = plt.Rectangle(xy, facecolor=color, width=1, height=1, 
                           edgecolor='black', linewidth=3, **kwargs)
    plt.gca().add_patch(square)


def plot_nonzero(arr, values=None, *, alpha=1, colormap=plt.cm.summer, **kwargs):
    """Plot nonzero elements of an array.

    Parameters
    ----------
    arr : array-like
    Nonzero elements will be plotted as square tiles.

    values : array-like (optional)
    Used to determine coloring scheme of tiles. Useful for dim=0 pattern consistency.

    alpha : int
    Transparency value for facecolor of tiles. Does not affect tile borders.

    colormap : matplotlib.colors.Colormap, str
    Colormap to distinguish distinct values in the array.

    kwargs : (optional)
    Keyword arguments passed to matplotlib.pyplot.Rectangle.
    """
    
    arr = np.rot90(np.asarray(arr), -1)
    
    if values is None:
        values = np.unique(arr[np.nonzero(arr)])
    else:
        values = np.unique(np.asarray(values))
        if not np.in1d(arr[np.nonzero(arr)], values).all():
            raise ValueError('values must be superset of elements in arr')

    if isinstance(colormap, str):
        colormap = getattr(plt.cm, colormap)
    colors = colormap(np.linspace(0, 1, values.size))  #TODO: adjust for dim=0

    plt.figure(figsize=arr.shape)
    cm = dict(zip(values, colors))
    xs, ys = np.nonzero(arr)
    for xy in zip(xs, ys):
        val = arr[xy]
        *rgb, _ = cm[val]
        color = rgb + [alpha]
        plot_square(xy, val, color, **kwargs)
    
    plt.axis('equal')
    plt.axis('off')


def plot_pattern(pattern, dim, *, val_to_dim=None, savepath=None, **kwargs):
    """Plot a tile pattern for a given dimension.
    
    Parameters
    ----------
    pattern : str
    Acceptable composite shapes -- unit(.), linear(|, -, /, \\), quadratic(O)
    
    dim : int
    Dimension of the composite shapes.
    
    val_to_dim : dict[int] -> func (optional)
    Custom dimensions mapping composite shape value to dimension.

    savepath : path-like object (optional)
    Filename to save plot to.

    kwargs : (optional)
    Keyword arguments passed to plot_nonzero.
    """

    arr = pattern_to_array(pattern, dim, val_to_dim=val_to_dim)
    num_of_parts = sum(char not in string.whitespace for char in pattern)
    values = np.arange(num_of_parts) + 1
    plot_nonzero(arr, values, **kwargs)

    if savepath is not None:
        plt.savefig(savepath)
