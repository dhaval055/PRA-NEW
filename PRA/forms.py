from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from PRA import mongo

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
    organization_type = SelectField('Organization Type',choices=[('Airline', 'Airline'), ('E-commerce', 'E-commerce'), 
                                        ('Education', 'Education'),('Political Party', 'Political Party')])                                 
    twitter_link = StringField('Twitter Link',
                           validators=[DataRequired(), Length(min=2, max=50)])
    facebook_link = StringField('facebook_link',
                           validators=[Length(min=2, max=50)])
    keywords = StringField('Keywords',
                           validators=[DataRequired(), Length(min=2, max=25)])                                                                               
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        taken_email = mongo.db.user.find_one({"Email": email.data},{"_id":0 ,"Email":1})
        if taken_email == None:
            return
        if taken_email['Email'] == email.data:
                raise ValidationError('That email is taken. Please choose a different one.')

class UpdateForm(FlaskForm):
    fullname = StringField('Full name',
                           validators=[Length(min=2, max=25)])
    organization = StringField('Organization Name',
                           validators=[Length(min=2, max=25)])                       
    email = StringField('Email',
                        validators=[Email()])

    twitter_link = StringField('Twitter Link',
                           validators=[Length(min=2, max=50)])
    facebook_link = StringField('facebook_link',
                           validators=[Length(min=2, max=50)])
    keywords = StringField('Keywords',
                           validators=[Length(min=2, max=25)])                                                                               
    submit = SubmitField('Save Changes')
    
    def validate_email(self, email):
        taken_email = mongo.db.user.find_one({"Email": email.data},{"_id":0 ,"Email":1})
        if taken_email == None:
            return
        if taken_email['Email'] == email.data:
                raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
