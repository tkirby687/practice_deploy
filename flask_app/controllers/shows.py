from flask_app.models.show import Show
from flask_app import app
from flask import render_template, redirect, request, session

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')    
    return render_template("dashboard.html", shows = Show.get_all_shows_with_user())

@app.route('/show/create', methods=['POST'])
def create_show():
    if 'user_id' not in session:
        return redirect('/logout')
    valid = Show.show_validator(request.form)
    if valid:
        
        data = {
            'title' : request.form['title'],
            'description' : request.form['description'],
            'release_date' : request.form['release_date'],
            'user_id' : session['user_id'] 
        }
        show = Show.create_show(data)
        return redirect(f'/show/{show}')
    return redirect('/show/add_show')

@app.route('/show/add_show')
def add_show_form():
    return render_template('new_show.html')

@app.route('/show/edit_show/<int:show_id>')
def edit_show(show_id):
    data = {
        'id' : show_id
    }    
    return render_template("edit_show.html", show = Show.get_one(data))
    
@app.route('/show/update/<int:show_id>', methods=['POST'])
def update_show(show_id):
    Show.update_show(request.form)
    return redirect('/dashboard')

@app.route('/show/delete_show/<int:show_id>')
def delete_show(show_id):
    data = {
        'id' : show_id
    }
    Show.delete_show(data)
    return redirect('/dashboard')

@app.route('/show/<int:show_id>')
def display_show(show_id):
    data = {
        'id' : show_id
    }
    return render_template('one_show.html', show = Show.get_one(data))