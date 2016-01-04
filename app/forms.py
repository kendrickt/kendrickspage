from flask.ext.wtf import Form
from wtforms import IntegerField
from wtforms.validators import Required, NumberRange


class TestForm(Form):
    int_a = IntegerField('int_a', validators=[Required()])
    int_b = IntegerField('int_b', validators=[Required()])


class YearIntervalSelectionForm(Form):
    start_year = IntegerField('start_year',  validators=[
        Required(),
        NumberRange(min=2009, max=2015)
    ])
    end_year = IntegerField('end_year', validators=[
        Required(),
        NumberRange(min=2009, max=2015)
    ])
