from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///money_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models for Income, Investments, Savings, and Expenses
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    units = db.Column(db.Float, nullable=False)
    class_type = db.Column(db.String(50), nullable=False)
    currency = db.Column(db.String(10), nullable=False)

class Saving(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    currency = db.Column(db.String(10), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    currency = db.Column(db.String(10), nullable=False)

# Create all database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    total_income = db.session.query(db.func.sum(Income.amount)).scalar() or 0
    total_savings = db.session.query(db.func.sum(Saving.amount)).scalar() or 0
    total_expenses = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
    total_investments = db.session.query(db.func.sum(Investment.amount)).scalar() or 0
    return render_template('home.html', total_income=total_income, total_savings=total_savings,
                           total_expenses=total_expenses, total_investments=total_investments)

@app.route('/income', methods=['GET', 'POST'])
def income():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        amount = float(request.form['amount'])
        currency = request.form['currency']
        new_income = Income(date=date, amount=amount, currency=currency)
        db.session.add(new_income)
        db.session.commit()
        return redirect(url_for('income'))
    incomes = Income.query.all()
    return render_template('income.html', incomes=incomes)

@app.route('/investments', methods=['GET', 'POST'])
def investments():
    if request.method == 'POST':
        company = request.form['company']
        amount = float(request.form['amount'])
        units = float(request.form['units'])
        class_type = request.form['class']
        currency = request.form['currency']
        new_investment = Investment(company=company, amount=amount, units=units, class_type=class_type, currency=currency)
        db.session.add(new_investment)
        db.session.commit()
        return redirect(url_for('investments'))
    investments = Investment.query.all()
    return render_template('investments.html', investments=investments)

@app.route('/savings', methods=['GET', 'POST'])
def savings():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        amount = float(request.form['amount'])
        type = request.form['type']
        currency = request.form['currency']
        new_saving = Saving(date=date, amount=amount, type=type, currency=currency)
        db.session.add(new_saving)
        db.session.commit()
        return redirect(url_for('savings'))
    savings = Saving.query.all()
    return render_template('savings.html', savings=savings)

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        amount = float(request.form['amount'])
        category = request.form['category']
        currency = request.form['currency']
        new_expense = Expense(date=date, amount=amount, category=category, currency=currency)
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('expenses'))
    expenses = Expense.query.all()
    return render_template('expenses.html', expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)
