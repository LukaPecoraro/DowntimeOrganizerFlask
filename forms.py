from flask_wtf import FlaskForm

from wtforms import DecimalField, StringField, IntegerField, SubmitField, RadioField, PasswordField
from wtforms.validators import InputRequired, NumberRange, EqualTo

# class CaesarShift(FlaskForm):
#     plainText = StringField("Plaintext", validators=[InputRequired()])
#     shift = IntegerField("Shift", validators=[InputRequired(), NumberRange(1,25)])
#     cipher = StringField("chipher")
#     submit = SubmitField("Submit")

# class TemperatureConversion(FlaskForm):
#     unitFrom = RadioField("From", 
#         choices=["Celsius", "Fahrenheit", "Kelvin"], 
#         default= "Celsius",
#     validators=[InputRequired()]
#     )

#     temperature = DecimalField("Temperature", validators=[InputRequired()])

#     unitTo = RadioField("To", 
#         choices=["Celsius", "Fahrenheit", "Kelvin"], 
#         default= "Kelvin",
#         validators=[InputRequired()],
#     )

#     converted = DecimalField("Converted")
#     submit = SubmitField("Convert")
class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()]) 
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Login") 

class RegisterForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()]) 
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Repeat password:", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Register") 

class MovieSearch(FlaskForm):
    movieTitle = StringField("Movie title:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class MusicSearch(FlaskForm):
    searchString = StringField("Movie title:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class BookSearch(FlaskForm):
    searchString = StringField("Movie title:", validators=[InputRequired()])
    submit = SubmitField("Submit")