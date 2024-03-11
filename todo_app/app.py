from flask import Flask, redirect, render_template, request

from todo_app.data.models import ViewModel
from todo_app.data.trello_items import add_trello_item, get_trello_board, update_trello_item_status


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        items = get_trello_board()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    def add():
        title = request.form.get('title')
        add_trello_item(title)
        return redirect('/')

    @app.route('/update_status', methods=['POST'])
    def update_status():
        item_id = request.form.get('item_id')
        status = request.form.get('status')

        update_trello_item_status(item_id, status)

        return redirect('/')

    return app
