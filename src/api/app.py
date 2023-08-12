from flask import Flask 
from src.api.article import views as article_views
from src.api.user import views as user_views

def create_app():

    app = Flask(__name__)
    
    register_blueprints(app)
    return app 

def register_blueprints(app) :
    app.register_blueprint(article_views.article)
    app.register_blueprint(user_views.user)