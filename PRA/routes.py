from flask import render_template, url_for, flash, redirect, request, abort
from PRA import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration')
def registration():
    return render_template('auth-register.html')

@app.route('/login')
def login():
    return render_template('auth-login.html')

@app.route('/home')
def home():
    return render_template('home.html')     

@app.route('/update')
def update():
    return render_template('update-profile.html')      

    

