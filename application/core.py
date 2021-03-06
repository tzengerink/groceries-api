import os
import six

from flask import Flask, jsonify
from flask.ext.cors import CORS
from werkzeug.http import HTTP_STATUS_CODES

from application.views import item, login, status, suggest
from application.models import init_models


def app(environ, start_response):
    app = make_app()
    return app(environ, start_response)


def error_handler(error):
    resp = jsonify(code=error.code,
                   name=error.name,
                   description=error.description)
    resp.status_code = error.code
    return resp


def make_app(config={}):
    app = Flask(__name__)
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL'),
    })
    app.config.update(config)

    init_models(app)

    for code in [k for k, v in HTTP_STATUS_CODES.items() if k >= 400]:
        app.error_handler_spec[None][code] = error_handler

    CORS(app, resourses={
        r'/*': dict(allow_headers=['Content-Type'],
                    methods=['GET', 'POST', 'PUT', 'DELETE'],
                    origins='*')})

    routes = {
        '/item': item,
        '/item/<int:id>': item,
        '/login': login,
        '/status': status,
        '/suggest': suggest
    }

    for endpoint, func in six.iteritems(routes):
        app.add_url_rule(endpoint, view_func=func)

    return app
