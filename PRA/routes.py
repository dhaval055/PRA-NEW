from flask import render_template, url_for, flash, redirect, request, abort
from PRA import app

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/registration')
def registration():
    return render_template('reg.html')

@app.route('/login')
def login():
    return render_template('login.html')    

