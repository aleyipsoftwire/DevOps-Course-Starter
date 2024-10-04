from flask import Flask, redirect, render_template, request

from todo_app.data.models import ViewModel
from todo_app.data.mongo_items import get_mongo_items, add_mongo_item, update_mongo_item_status, ItemStatus


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        items = get_mongo_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    def add():
        title = request.form.get('title')
        add_mongo_item(title)
        return redirect('/')

    @app.route('/update_status', methods=['POST'])
    def update_status():
        item_id = request.form.get('item_id')
        status = request.form.get('status')

        update_mongo_item_status(item_id, ItemStatus(status))

        return redirect('/')

    return app
