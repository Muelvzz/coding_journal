from flask import Flask, render_template

def createapp():
    app = Flask(__name__)

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    return app