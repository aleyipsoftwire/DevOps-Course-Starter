from flask import Flask, redirect, render_template, request

from todo_app.data.session_items import add_item
from todo_app.data.trello_items import get_board
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_board()
    return render_template('index.html', items=items)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    add_item(title)
    return redirect('/')
