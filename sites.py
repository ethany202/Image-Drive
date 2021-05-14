from flask import Blueprint, redirect, url_for, render_template

sites = Blueprint('sites', __name__)
authenticated = False

@sites.route('/home')
def home():
    return render_template("home.html")
