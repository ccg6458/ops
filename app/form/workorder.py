from wtforms import StringField, IntegerField, Form, TextField
from wtforms.validators import Length, NumberRange, DataRequired


class WorkOrderForm(Form):
    name = StringField(validators=[Length(min=1, max=128), DataRequired])
    sql = StringField(DataRequired)
    audit = IntegerField(validators=[NumberRange(min=0, max=1)])
    finish = IntegerField(validators=[NumberRange(min=0, max=1)])
    comment = StringField(DataRequired)
