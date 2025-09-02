import os
from logging import Formatter

from flask import Flask, redirect, render_template, request
from loggly.handlers import HTTPSHandler

from todo_app.data.models import ViewModel
from todo_app.data.mongo_items import get_mongo_items, add_mongo_item, update_mongo_item_status, ItemStatus


def create_app():
    app = Flask(__name__)

    app.logger.setLevel(os.getenv("LOG_LEVEL", "ERROR"))

    if os.getenv('LOGGLY_TOKEN') is not None:
        print(f'https://logs-01.loggly.com/inputs/{os.getenv("LOGGLY_TOKEN")}/tag/todo-app')
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{os.getenv("LOGGLY_TOKEN")}/tag/todo-app')
        handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
        app.logger.addHandler(handler)

    @app.route('/')
    def index():
        items = get_mongo_items()

        app.logger.info(f'Found {len(items)} items')

        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    def add():
        title = request.form.get('title')

        app.logger.info(f'Adding new item: {title}')

        add_mongo_item(title)
        return redirect('/')

    @app.route('/update_status', methods=['POST'])
    def update_status():
        item_id = request.form.get('item_id')
        status = request.form.get('status')

        app.logger.info(f'Updating status of item {item_id} to {status}')

        update_mongo_item_status(item_id, ItemStatus(status))

        return redirect('/')

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.warning(f'Exception: {e}')
        return e

    return app
