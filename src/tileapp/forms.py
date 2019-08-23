from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Regexp
from wtforms.widgets import TextArea


class PatternForm(FlaskForm):
    pattern = StringField('Pattern', widget=TextArea(), 
                          validators=[DataRequired(), Regexp('^[Oo01l\\/|.\s-]+$')])
    fignum = IntegerField('Figure Number', validators=[NumberRange(0, 10)])
    cms = 'gnuplot summer autumn winter spring rainbow gray'.split()
    colormap = SelectField('Color Palette', choices=[(cm.lower(), cm.title()) for cm in cms])
    alpha = FloatField('Transparency', default=1, validators=[NumberRange(0, 1)])
    submit = SubmitField('Generate Figure')
