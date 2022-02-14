#package
from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_user, logout_user, current_user, login_required


#project
from marvel_inventory.forms import UserLoginForm
from marvel_inventory.models import User, db, check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup',methods=['GET','POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            #Adds user to the database
            user = User(email, password = password)
            
            db.session.add(user)
            db.session.commit()


            flash(f'You have created an account for {email}.','user-created')
            return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: Please check your form.')

    return render_template('signup.html', form=form)

@auth.route('/signin',methods=['GET','POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            #Adds user to the database
            logged_user = User.query.filter(User.email==email).first()

            if logged_user and check_password_hash(logged_user.password,password): 
                login_user(logged_user)
                flash('You have logged in','auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Your info is not correct.','auth-failed')
                return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: Please check your form.')

    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))

