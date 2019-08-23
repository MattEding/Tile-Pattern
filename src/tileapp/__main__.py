import argparse
import functools
from pathlib import Path

import matplotlib.pyplot as plt

from tileapp.image import plot_pattern, pattern_to_array


parser = argparse.ArgumentParser(description='Tile pattern parser from txt to png')
parser.add_argument('infile',
                    help='filepath with pattern to parse')
parser.add_argument('dim', type=int, nargs='+', 
                    help='dimensions to form pattern')
parser.add_argument('-a', '--alpha', default=1.0, type=float,
                    help='transparency of the colors used in png output; set to 0 for b/w png')
colormap_refrence = 'https://matplotlib.org/gallery/color/colormap_reference.html'
parser.add_argument('-cm', '--colormap', default='rainbow',
                    help=f'colormap used to differentiate tile parts; see {colormap_refrence}')
parser.add_argument('-o', '--outdir', metavar='DIR', nargs='?', const='.', default=None,
                    help='destination file for png output; if omitted, png is popup; if not arg, save png to cwd')
parser.add_argument('-p', '--prefix',
                    help='prefix used for png output; use alongside outdir')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='print to stdout the array used for png creation')

args = parser.parse_args()

if args.outdir is not None:
    outdir = Path(args.outdir)
    if not outdir.is_dir():
        raise NotADirectoryError('outdir must be a directory')
else:
    outdir = None

infile = Path(args.infile)
if not infile.is_file():
    raise FileNotFoundError('infile must be a file')
with open(infile) as fp:
    pat = fp.read()

if args.verbose:
    print('Pattern:')
    print(pat)

plt_pat = functools.partial(plot_pattern, pat, alpha=args.alpha, colormap=args.colormap)
for dim in args.dim:
    if args.verbose:
        arr = pattern_to_array(pat, dim)
        print('Dim:', dim)
        print(arr)
    
    if outdir is not None:
        outfile = outdir / f'{infile.stem}_dim{dim}.png'
        plt_pat(dim, savepath=outfile)
    else:
        plt_pat(dim)

if outdir is None:
    plt.show()
