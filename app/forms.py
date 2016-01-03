from flask.ext.wtf import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired


class TestForm(Form):
    int_a = IntegerField('int_a', validators=[DataRequired()])
    int_b = IntegerField('int_b', validators=[DataRequired()])
