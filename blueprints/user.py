from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_user , current_user
from passlib.hash import sha256_crypt

from extentions import db
from models.user import User

app = Blueprint('user', __name__)

@app.route('/user/login', methods=['GET', 'POST'])
def user():
  if request.method == "GET":
    if current_user.is_authenticated:
       return redirect( url_for('user.dashboard') )
    return render_template('user/login.html')
  else:
    register= request.form.get('register',None)
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    first_name = request.form.get('first_name', None)
    last_name = request.form.get('last_name', None)
    email = request.form.get('email', None)
    phone = request.form.get('phone', None)
    address = request.form.get('address', None)

    if register != None:
      user = User.query.filter(User.username == username).first()
      if user == None:
        flash('invaid username')
        return redirect(url_for('user.login'))
      user = User(username=username, password = sha256_crypt.encrypt(password) , first_name=first_name, last_name=last_name, email=email, phone=phone, address=address)
      db.session.add(user)
      db.session.commit()
      login_user(user)      
    else:
      user = User.query.filter(User.username == username).first()
      if user == None:
        flash("Username or password is incorrect")
        return redirect(url_for('user.login'))
      if sha256_crypt.verify(password, user.password):
        login_user(user)  
        return redirect(url_for('user.dashboard'))
      else:
        flash( "Username or password is incorrect")
        return redirect(url_for('user.login'))

    return redirect(url_for('user.dashboard'))


@app.route('/user/dashboard', methods=['GET'])
def dashboard():
  return 'dashboard'