import base64
import io
import itertools
import functools
import string

import matplotlib.pyplot as plt
import numpy as np
from scipy import sparse


def unit(fill_value, dim):  #: `dim` param included for signature compatibility
    return np.array(fill_value)


def linear_straight(fill_value, dim, vert):
    arr = np.array([[fill_value] * dim])
    if vert:
        arr = arr.T
    return arr


def linear_diagonal(fill_value, dim, pos):
    arr = np.eye(dim) * fill_value
    if pos:
        arr = np.flip(arr)
    return arr


def quadratic(fill_value, dim):
    return np.full((dim, dim), fill_value=fill_value)


CHAR_TO_ARR = {
    ' ': None,
    '.': unit,
    '|': functools.partial(linear_straight, vert=True),
    '-': functools.partial(linear_straight, vert=False),
    '/': functools.partial(linear_diagonal, pos=True),
    '\\': functools.partial(linear_diagonal, pos=False),
    'O': quadratic,
}


def pattern_to_array(pattern, dim):
    """Convert a pattern to an array.
    Example with dim=2: pattern      array([[1, 2, 2, 3, 3, 4, 0],
                         .--.              [0, 5, 5, 0, 0, 6, 7],
                          O ||             [0, 5, 5, 0, 0, 6, 7]]) 
    """
    
    pattern = (pattern.strip('\n')
                      .upper()
                      .replace('\r', '')
                      .replace('0', 'O')
                      .replace('L', '|')
                      .replace('1', '|'))
    if any(char not in CHAR_TO_ARR for char in pattern if char != '\n'):
        raise ValueError('pattern must only consist of: " .|-\\/O"')
    
    fill_value = itertools.count(start=1)
    lines = pattern.split('\n')
    width = len(max(lines, key=len))
    bmat = [[None] * width]  #: None row avoids bug for some valid patterns (e.g. "|||")
    for line in lines:
        line = line.ljust(width)
        row = []
        for char in line:
            arr = CHAR_TO_ARR[char]
            if arr is not None:
                value = next(fill_value)
                arr = arr(fill_value=value, dim=dim)
            row.append(arr)
        bmat.append(row)
    try:
        sbmat = sparse.bmat(bmat, dtype=int)
    except ValueError:
        raise ValueError('subarray dimensions do not align')
    return sbmat.toarray()


def plot_square(xy, val, color, **kwargs):
    square = plt.Rectangle(xy, facecolor=color, width=1, height=1, 
                           edgecolor='black', linewidth=3, **kwargs)
    plt.gca().add_patch(square)


def plot_nonzero(arr, values=None, *, alpha=1.0, colormap=plt.cm.summer, **kwargs):
    """Plot nonzero elements of an array.
    """
    
    arr = np.rot90(np.asarray(arr), -1)
    
    #: `values` used for dim=0 color consistency with dim=N
    if values is None:
        values = np.unique(arr[np.nonzero(arr)])
    else:
        values = np.unique(np.asarray(values))
        if not np.in1d(arr[np.nonzero(arr)], values).all():
            raise ValueError('values must be superset of elements in arr')

    if isinstance(colormap, str):
        colormap = getattr(plt.cm, colormap)
    colors = colormap(np.linspace(0.1, 0.9, values.size))

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


def plot_pattern(pattern, dim, savepath=None, **kwargs):
    """Plot a tile pattern for a given dimension.
    """

    arr = pattern_to_array(pattern, dim)
    num_of_parts = sum(char not in string.whitespace for char in pattern)
    values = np.arange(num_of_parts) + 1
    plot_nonzero(arr, values, **kwargs)

    if savepath is not None:
        plt.savefig(savepath, format='png')


def pattern_to_html(pattern, dim, colormap, alpha):
    """Prepare image from pattern and dimension for HTML without saving to disk.
    """

    img_io = io.BytesIO()
    plot_pattern(pattern, dim, savepath=img_io, colormap=colormap, alpha=alpha)
    img_b64 = base64.b64encode(img_io.getvalue())
    img_ascii = img_b64.decode('ascii')
    return img_ascii
