from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import requests


app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wrote.sqlite'


class Wrote(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.CHAR(50), nullable=False)

    def __str__(self):
        return f'{self.name}'


class Parsing(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.CHAR(50), nullable=False)
    link = db.Column(db.CHAR(100), nullable=False)

    def __str__(self):
        return f'title: {self.title},  url: {self.link}'


def api_req(name):
    try:
        url = 'http://www.thecocktaildb.com/api/json/v1/1/search.php?s=' + str(name)
        req = requests.get(url).json()
        return req['drinks'][0]['strInstructions']
    except:
        return "name is incorrect"


@app.route('/home')
def home():
    data = Wrote.query.all()

    return render_template('Home.html', data=data)


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        if request.form['todo_text'] != '':
            d = request.form['todo_text']
            writing = Wrote(name=d)
            db.session.add(writing)
            db.session.commit()
            flash('data is added', 'succ')
        elif request.form['todo_text'] == Wrote.query.filter_by(name=request.form['todo_text']):
            flash('this text is already exists', 'error')
        else:
            flash("it's empty", 'error')

    return render_template('Add.html')


@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'Giorgi' and request.form['password'] == '123':
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        else:
            flash('incorrect', 'error')
    return render_template('Login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/parsing')
def parsing():
    parsed = Parsing.query.all()
    return render_template('parsing.html', data=parsed)


@app.route('/apiconnect', methods=['POST', 'GET'])
def apiconnect():
    if request.method == 'POST':

        name = request.form['search_api']
        data = api_req(name)
        return render_template('apiconnect.html', data=data)
    return render_template('apiconnect.html')


if __name__ == '__main__':
    app.run(debug=True)
