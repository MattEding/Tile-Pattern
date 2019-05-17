import matplotlib.pyplot as plt
import numpy as np

from .parser import pattern_to_array


def plot_square(xy, val, color, **kwargs):
    square = plt.Rectangle(xy, facecolor=color, width=1, height=1, 
                           edgecolor='black', linewidth=3, **kwargs)
    plt.gca().add_patch(square)


def plot_nonzero(arr, *, alpha=1, colormap=plt.cm.summer, **kwargs):
    """Plot nonzero elements of an array.

    Parameters
    ----------
    arr : array-like
    Nonzero elements will be plotted as square tiles.

    alpha : int
    Transparency value for facecolor of tiles. Does not affect tile borders.

    colormap : matplotlib.colors.Colormap, str
    Colormap to distinguish distinct values in the array.

    kwargs : optional
    Keyword arguments passed to matplotlib.pyplot.Rectangle.
    """
    
    arr = np.asarray(arr)
    values = np.unique(arr[arr > 0])
    if isinstance(colormap, str):
        colormap = getattr(plt.cm, colormap)
    colors = colormap(np.linspace(0, 1, values.size))  #TODO: adjust for dim=0

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
    arr = np.rot90(arr, -1)
    plt.figure(figsize=arr.shape)
    plot_nonzero(arr, **kwargs)

    if savepath is not None:
        plt.savefig(savepath)
