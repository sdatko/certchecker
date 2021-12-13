#!/usr/bin/env python3

from random import random
import threading

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import pyotp


server_results = {}


def view():
    if request.form:
        if request.form.get('user') and request.form.get('pass'):
            if (request.form.get('user') == 'admin'
                    and request.form.get('pass') == 'qwerty'):
                session['secondfactor'] = True
            else:
                session['authenticated'] = False
                session['secondfactor'] = False
        elif request.form.get('token') and session.get('secondfactor', False):
            totp = pyotp.TOTP('base32secret3232')
            if totp.verify(request.form.get('token'), valid_window=3):
                session['authenticated'] = True
            else:
                session['authenticated'] = False
                session['secondfactor'] = False
        else:
            session['authenticated'] = False
            session['secondfactor'] = False
        return redirect(url_for('index'))

    authenticated = session.get('authenticated', False)
    secondfactor = session.get('secondfactor', False)
    return render_template('index.html',
                           authenticated=authenticated,
                           secondfactor=secondfactor,
                           results=server_results)


def main():
    app = Flask(__name__)
    app.add_url_rule('/', 'index', view_func=view, methods=['GET', 'POST'])
    app.secret_key = 'development key ' + str(random())
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
