from flask import render_template, url_for, flash, redirect, request, abort, jsonify, json
from flask_bcrypt import bcrypt
from PRA.forms import RegistrationForm, UpdateForm, LoginForm
from PRA import app, mongo, bcrypt

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/registration',methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        keywords = form.keywords.data.split()
        user_profile = {
            "FullName": form.fullname.data, "Organiaztion" : form.organization.data,
            "Email": form.email.data,"Password": hashed_password, "OrganizationType": form.organization_type.data,
            "TwitterLink": form.twitter_link.data, "FacebookLink": form.facebook_link.data, 
            "Keywords":keywords }
        mongo.db.user.insert_one(user_profile)   
        flash('Registration Successful, Login to continue.','success')
        return redirect('login')
    return render_template('auth-register.html',form=form)

@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('home')
    return render_template('auth-login.html',form=form)

@app.route('/home')
def home():
    return render_template('home.html')     

@app.route('/update')
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        flash('Profile Updated.','success')
        return redirect('home')
    return render_template('update-profile.html',form=form)

@app.route('/feedback')
def feedback():
    return render_template('contact.html')

@app.route('/tweets')
def tweets():
    return render_template('tweets.html')
