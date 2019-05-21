from functools import partial

from flask import flash, redirect, render_template, request, url_for
from tileapp import app
from tileapp.forms import PatternForm
from tileapp.image import plot_pattern, pattern_to_html


pat_0 = """
 .
||O
 .
"""

@app.route('/')
@app.route('/home')
def home():
    figs_clr = [pattern_to_html(pat_0, x, 'gnuplot', 1.0) for x in range(5)]
    figs_bw = [pattern_to_html(pat_0, x, 'gray', 0.0) for x in range(5)]
    mask = [True, False, False, True, False]
    figs_bw_mask = zip(figs_bw, mask)
    return render_template('home.html', title='Home', figs_clr=figs_clr, figs_bw_mask=figs_bw_mask)


@app.route('/pattern', methods=['GET', 'POST'])
def pattern():
    form = PatternForm()
    if form.validate_on_submit():
        pattern = form.pattern.data
        fignum = form.fignum.data
        colormap = form.colormap.data
        alpha = form.alpha.data
        img_ascii = pattern_to_html(pattern, fignum, colormap, alpha)
        return render_template('pattern.html', title='Pattern', form=form, img=img_ascii)
    return render_template('pattern.html', title='Pattern', form=form, img=None)


def create_demo(pattern, fignum, colormap, alpha):
    form = PatternForm()
    form.pattern.data = pattern
    form.fignum.data = fignum
    form.colormap.data = colormap
    form.alpha.data = alpha
    img_ascii = pattern_to_html(pattern, fignum, colormap, alpha)
    return form, img_ascii


pat_1 = """
O|
 .
"""

pat_2 = """
. .
 O
. .
"""

pat_3 = """
--.--
"""

@app.route('/help')
def help():
    # help and documentation
    form_1, img_1 = create_demo(pat_1, 2, 'winter', 1.0)
    form_2, img_2 = create_demo(pat_2, 3, 'gray', 0.0)
    form_3, img_3 = create_demo(pat_3, 2, 'rainbow', 0.75)
    forms = [form_1, form_2, form_3]
    imgs = [img_1, img_2, img_3]
    return render_template('help.html', title='Help', demos=zip(forms, imgs))