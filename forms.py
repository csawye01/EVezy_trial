from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TimeField, IntegerField, validators
from wtforms.validators import DataRequired, Length, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField
from wtforms import ValidationError
from models import Bookings, Cars


class LoginForm(Form):
    EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class BookingsForm(Form):
    car_make = QuerySelectField('Car make', validators=[DataRequired()],
                                query_factory=lambda: Cars.query.distinct(Cars.make), get_label='make')
    car_model = QuerySelectField('Car model', validators=[DataRequired()],
                                 query_factory=lambda: Cars.query.distinct(Cars.model), get_label='model')
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    start_date = DateField('DatePicker', format='%Y-%m-%d')
    start_time = TimeField('Start time', validators=[DataRequired()])
    duration = IntegerField('Duration of Rental', validators=[DataRequired()])

    def validate_booking(self, field):
        if Bookings.query.filter_by(car_make=field.data, car_model=field.data, ).all():



                raise ValidationError('Car make and model alreday in use at the selected time frame.')
