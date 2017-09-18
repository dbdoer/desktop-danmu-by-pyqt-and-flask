from __future__ import unicode_literals
from flask import (Flask, render_template, g, session, redirect, url_for,
                   request, flash, current_app, jsonify)
from form import DanmuForm
from flask_bootstrap import Bootstrap
import queue

SECRET_KEY = 'This is my key'

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = SECRET_KEY

with app.app_context():
    current_app.danmu_queue = queue.Queue()
    current_app.danmu_list = []


@app.route('/', methods=['GET', 'POST'])
def index():
    form = DanmuForm()
    if request.method == 'GET':
        
        print('queue:',current_app.danmu_queue.qsize(),'\nlist:',current_app.danmu_list)
        return render_template('index.html', form=form)
    else:
        if form.validate_on_submit():
            content = form.content.data
            with app.app_context():
                print(content)
                current_app.danmu_queue.put(content)
                current_app.danmu_list.append(content)
            flash('吐槽完毕，' + content)
        else:
            flash(form.errors)
        return redirect(url_for('index'))


@app.route('/danmu_get', methods=['GET'])
def danmu_get():
    if request.method == 'GET':
        with app.app_context():
            if not current_app.danmu_queue.empty():
                return current_app.danmu_queue.get(block=False)
    return "no"

@app.route('/_add_numbers', methods = [ "POST", "GET" ] )
def add_numbers():
    if request.method == "POST":  
        first_name = request.form.get( "first_name", "null" )  
        last_name = request.form.get( "last_name", "null" )  
        return jsonify( name = first_name + " " + last_name )
    else:  
        return render_template( "index2.html" )  

if __name__ == '__main__':
    app.run()
