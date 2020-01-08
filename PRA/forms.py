from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    fullname = StringField('Full name',
                           validators=[DataRequired(), Length(min=2, max=25)])
    organization = StringField('Organization Name',
                           validators=[DataRequired(), Length(min=2, max=25)])                       
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    organization_type = SelectField('Organization Type',choices=[('1', 'Airline'), ('2', 'E-commerce'), 
                                        ('3', 'Education'),('4', 'Plotical Party')])                                 
    twitter_link = StringField('Twitter Link',
                           validators=[DataRequired(), Length(min=2, max=50)])
    facebook_link = StringField('facebook_link',
                           validators=[Length(min=2, max=50)])
    keywords = StringField('Keywords',
                           validators=[DataRequired(), Length(min=2, max=25)])                                                                               
    submit = SubmitField('Sign Up')


class UpdateForm(FlaskForm):
    fullname = StringField('Full name',
                           validators=[Length(min=2, max=25)])
    organization = StringField('Organization Name',
                           validators=[Length(min=2, max=25)])                       
    email = StringField('Email',
                        validators=[Email()])
    password = PasswordField('Password')

    twitter_link = StringField('Twitter Link',
                           validators=[Length(min=2, max=50)])
    facebook_link = StringField('facebook_link',
                           validators=[Length(min=2, max=50)])
    keywords = StringField('Keywords',
                           validators=[Length(min=2, max=25)])                                                                               
    submit = SubmitField('Save Changes')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

