from wtforms import StringField, IntegerField, Form
from wtforms.validators import Length, NumberRange, DataRequired


class UserForm(Form):
    name = StringField(validators=[Length(min=1, max=50), DataRequired])
    email = StringField(validators=[Length(min=1, max=50), DataRequired])
    status = IntegerField(validators=[NumberRange(min=0, max=1)])



