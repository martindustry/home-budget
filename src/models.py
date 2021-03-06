from functools import wraps
from datetime import date
from flask import redirect, session, url_for
from src import db, ma


CATEGORIES = {
    'outcome': ['grocery', 'health', 'house', 'personal', 'media', 'savings', 
                'debts', 'whims', 'transport', 'gifts', 'travels', 'other'],
    'income': ['savings', 'salary', 'bonus', 'interest', 'gifts', 'other']
}

MONTHS = {
    0: 'All',
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

YEARS = [2022 + i for i in range(10)]
YEARS.insert(0, 0)

TRANSACTION_TYPES = ['all', 'income', 'outcome']


def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user has active session
        if session.get('user_id') is None:
            return redirect(url_for('auth.login'))
        else:
            # Ensure cookies are correct
            user = User.query.filter_by(id=session['user_id']).first()
            if not user:
                session.clear()
                return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


# Set up database tables
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(150))
    transactions = db.relationship('Transactions')
    planned_outcomes = db.relationship('PlannedOutcomes')
    planned_incomes = db.relationship('PlannedIncomes')
    starting_balance = db.relationship('StartingBalance')

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(10))
    amount = db.Column(db.Integer)
    category = db.Column(db.String(20))
    date = db.Column(db.Date, default=date.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class PlannedOutcomes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20))
    amount = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class PlannedIncomes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20))
    amount = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class StartingBalance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Set up database schemas used for json
class TransactionsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transactions
        include_relationships = True
        load_instance = True
