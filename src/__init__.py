import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    # Configure application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    # Configure database
    DB_URI = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI.replace('postgres://', 
                                                           'postgresql://')

    from .models import (User, Transactions, PlannedOutcomes, PlannedIncomes, 
                         TransactionsSchema)

    # Initiate database
    with app.app_context():
        db.init_app(app)
        ma.init_app(app)
        db.create_all()
        db.session.commit()

    from .views.auth import auth
    from .views.home import home
    from .views.settings import settings
    from .views.transactions import transactions
    from .views.planning import planning

    app.register_blueprint(auth)
    app.register_blueprint(home)
    app.register_blueprint(settings)
    app.register_blueprint(transactions)
    app.register_blueprint(planning)

    return app
