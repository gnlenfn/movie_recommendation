from flask import Flask
from flask_pymongo import PyMongo

import config

mongo = PyMongo()
def create_app():
    app = Flask(__name__)

    app.config.from_object(config)
    mongo.init_app(app)

    from .views import main_views, recommend_view, review_view
    app.register_blueprint(main_views.bp)
    app.register_blueprint(recommend_view.bp)
    app.register_blueprint(review_view.bp)

    return app





