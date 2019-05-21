from flask import flash, redirect, render_template, request, url_for
from tileapp import app
from tileapp.forms import PatternForm
from tileapp.image import plot_pattern, pattern_to_html


@app.route('/')
@app.route('/home')
def home():
    # introduction and example highlights
    return render_template('home.html', title='Home')


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


@app.route('/about')
def about():
    # help and documentation
    return render_template('about.html', title='About')