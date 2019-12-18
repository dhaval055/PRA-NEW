from flask import render_template, url_for, flash, redirect, request, abort
from PRA import app

@app.route('/index')
def index():
    return render_template('index.html')
