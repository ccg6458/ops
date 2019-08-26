from wtforms import StringField, IntegerField, Form, TextField
from wtforms.validators import Length, NumberRange, DataRequired


class WorkOrderForm(Form):
    type = IntegerField(validators=[NumberRange(min=0, max=3)])
    name = StringField(validators=[Length(min=1, max=128), DataRequired])
    sql = StringField(DataRequired)
    database = StringField(DataRequired)
    audit = IntegerField(validators=[NumberRange(min=0, max=1)])
    finish = IntegerField(validators=[NumberRange(min=0, max=1)])
    comment = StringField(DataRequired)
