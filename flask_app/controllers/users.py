from flask import  render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():    
    return render_template('new_user.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.user_register(request.form):
        return redirect('/')
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "pwd" : bcrypt.generate_password_hash(request.form['pwd'])
    }
    
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.pwd, request.form['pwd']):
        # if we get False after checking the password
        flash("Invalid Password", "login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
