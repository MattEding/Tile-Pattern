import itertools
import functools

import numpy as np
from scipy import sparse


def unit(fill_value, dim):  # dim param included for signature compatibility
    return np.array(fill_value)


def linear(fill_value, dim, vert):
    arr = np.array([[fill_value] * dim])
    if vert:
        arr = arr.T
    return arr


def quadratic(fill_value, dim):
    return np.full((dim, dim), fill_value=fill_value)


CHAR_TO_ARR = {
    ' ': None, 
    '.': unit, 
    '|': functools.partial(linear, vert=True), 
    '-': functools.partial(linear, vert=False), 
    'O': quadratic,
}


def pattern_to_array(pattern, dim, *, val_to_dim=None):
    """
    Example with dim=2: pattern     values      array([[1, 2, 2, 3, 3, 4, 0],
                         .--.        1234              [0, 5, 5, 0, 0, 6, 7],
                          O ||        5 67             [0, 5, 5, 0, 0, 6, 7]]) 
    
    Parameters
    ----------
    pattern : str
    Acceptable composite shapes -- unit(.), linear(| or -), quadratic(O)
    
    dim : int
    Dimension of the composite shapes.
    
    val_to_dim : dict[int] -> func (optional)
    Custom dimensions mapping composite shape value to dimension.
    
    Returns
    -------
    arr : ndarray
    Array with 0s for empty space and integer values for each individual composite shape.
    
    Raises
    ------
    ValueError('dimensions must align')
    
    ValueError('pattern must only consist of: " .|-O"')
    """
    
    pattern = pattern.strip('\n').upper()
    if any(char not in CHAR_TO_ARR for char in pattern if char != '\n'):
        raise ValueError('pattern must only consist of: " .|-O"')
        
    if val_to_dim is None:
        val_to_dim = dict()
    
    fill_value = itertools.count(start=1)
    lines = pattern.split('\n')
    width = len(max(lines, key=len))
    bmat = [[None] * width]  # None row avoids bug for some valid patterns (e.g. "|||")
    for line in lines:
        line = line.ljust(width)
        row = []
        for char in line:
            arr = CHAR_TO_ARR[char]
            if arr is not None:
                value = next(fill_value)
                arr = arr(fill_value=value, dim=val_to_dim.get(value, lambda d: d)(dim))
            row.append(arr)
        bmat.append(row)
    try:
        sbmat = sparse.bmat(bmat, dtype=int)
    except ValueError:
        raise ValueError('subarray dimensions do not align')
    return sbmat.toarray()
