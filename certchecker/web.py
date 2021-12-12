#!/usr/bin/env python3

import threading

from flask import Flask
from flask import render_template


server_results = {}


def view():
    return render_template('index.html', results=server_results)


def main():
    app = Flask(__name__)
    app.add_url_rule('/', 'index', view_func=view)
    app.run(port=5000, debug=False, use_reloader=False)


def start_server():
    flask_thread = threading.Thread(target=main)
    flask_thread.setDaemon(True)
    flask_thread.start()


def update_server_data(data):
    global server_results
    server_results = data


if __name__ == "__main__":
    main()
