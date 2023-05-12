
import flask
from flask import Flask, request, redirect, url_for
import requests


from flask_sqlalchemy import SQLAlchemy

DB_USERNAME = 'postgres'
DB_PASSWORD = 'khanhngoc2020'
DB_NETWORK = 'localhost'
DB_DATABASE = 'postgres'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_NETWORK}/{DB_DATABASE}'
db = SQLAlchemy(app)


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portfolio_name = db.Column(db.String, nullable=False)
    portfolio_link = db.Column(db.String, nullable=False)

    def __init__(self, portfolio_name, portfolio_link):
        self.portfolio_name = portfolio_name
        self.portfolio_link = portfolio_link


@app.route('/', methods=['GET'])
def index():
    error = request.args.get('error', '')
    return flask.render_template('index.html', portfolios=Portfolio.query.all(), error=error)


@app.route('/portfolio', methods=['POST'])
def add_new_portfolio():
    portfolio_name = request.form['portfolio_name']
    portfolio_link = request.form['portfolio_link']

    if portfolio_name == '' or portfolio_link == '':
        return redirect(url_for('index', error='Пожалуйста, введите название портфолио и ссылку на репозиторий (рабочая)'))

    url = portfolio_link # Ссылка, которая вы хотите проверить

    try:
        response = requests.get(url) # Отправить запрос HTTP GET на путь
        response.raise_for_status() # Проверьте, не является ли код состояния HTTP ошибочным.g
    except requests.exceptions.RequestException:
        return redirect(url_for('index', error='Ссылка не работает'))
    db.session.add(Portfolio(portfolio_name, portfolio_link))
    db.session.commit()

    return redirect(url_for('index')) 


@app.route('/portfolio', methods=['DELETE'])
def delete_all_comments():
    Portfolio.query.delete()
    db.session.commit()
    return "Success"


with app.app_context():
    db.create_all()

app.run()
