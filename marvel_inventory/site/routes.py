# a route is what makes the 'folder in a folder' system work and allow us to create unique sub-domain names or URL's that can be accessed from the front end

from flask import Blueprint, render_template
from flask_login.utils import login_required

# Like our var 'app', this var creates a reference to this folder and its pages that allow them to be accessed from our directory(__init__)
site = Blueprint('site',__name__,template_folder='site_templates')

# Creates a function that loads our home page and a route to do so
@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
