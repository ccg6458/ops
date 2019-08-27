from wtforms import StringField, IntegerField, Form
from wtforms.validators import Length, NumberRange, DataRequired


class TaskForm(Form):
    shell = StringField(validators=[DataRequired])
    schedule = StringField(validators=[Length(min=1, max=64), DataRequired])
    business_id = IntegerField(validators=[NumberRange(min=0, max=1)])
    comment = StringField(validators=[Length(min=1, max=128), DataRequired])




