from flask_wtf import Form
from wtforms import TextField, SubmitField,IntegerField,SelectField

from wtforms import validators, ValidationError
from wtforms.validators import DataRequired
hour_choices=[('1', '9:00-9:30'), ('2', '9:30-10:00'), ('3', '10:00-10:30'), ('4', '10:30-11:00'), ('5', '14:00-14:30'), ('6', '14:30-15:00'), ('7', '15:00-15:30'), ('8', '15:30-16:00')]
class singleContactForm(Form):
    name = TextField("姓名",[validators.Required("Please enter your name.")])
    cellphone = TextField("手机号",[validators.Required("Please enter your cellphone.")])
    people_num=IntegerField("人数",[validators.Required("Please enter your people_num.")])
    year=IntegerField("年",[validators.Required("Please enter your date.")])
    month = SelectField(
        label="月",
        validators=[DataRequired('请选择时间段')],
        render_kw={
            'class': 'form-control'
        },
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12')],
        default = 12,
        coerce=int
    )
    date=IntegerField("日",[validators.Required("Please enter your date.")])
    time = SelectField(
        label="具体时间",
        validators=[DataRequired('请选择时间段')],
        render_kw={
            'class': 'form-control'
        },
        choices=hour_choices,
        default = 8,
        coerce=int
    )

class singleCancel(Form):
    cell = TextField("手机号",[validators.Required("Please enter your cellnum.")])
