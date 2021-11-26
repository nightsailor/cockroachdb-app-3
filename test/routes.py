""" from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction """
from math import floor
import os
import random
import uuid
import urllib.parse
from datetime import datetime
from decouple import config
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
from cockroachdb.sqlalchemy import run_transaction

# from models import Account

def create_accounts(session, num):
    account_id = uuid.uuid4()
    account_balance = floor(random.random()*1_000_000)
    new_account = Account(id=account_id, balance=account_balance)
    session.add_all([new_account])

def connect(db_uri):
    engine = create_engine(db_uri)
    engine.connect()
    print('Hey! You successfully connected to your CockroachDB cluster.')

def main():
    conn_string = config('SQLALCHEMY_DATABASE_URI', default='guess_me')

    try:
        db_uri = os.path.expandvars(conn_string) #declare $HOME
        db_uri = urllib.parse.unquote(db_uri) #unquote %3D to =
        psycopg_uri = db_uri.replace('postgresql://', 'cockroachdb://').replace('26257?', '26257/todos?') #bank

        # connect(psycopg_uri)
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))

    # run_transaction(sessionmaker(bind=engine), lambda s: create_accounts(s, 10))
    return psycopg_uri


psycopg_uri = main()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = psycopg_uri
db = SQLAlchemy(app)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)
# app.config.from_pyfile('hello.cfg')
# db.create_all()


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column('todo_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String)
    done = db.Column(db.Boolean)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.done = False
        self.pub_date = datetime.utcnow()


@app.route('/')
def show_all():
    def callback(session):
        return render_template(
            'show_all.html',
            todos=session.query(Todo).order_by(Todo.pub_date.desc()).all())
    return run_transaction(sessionmaker, callback)


if __name__ == '__main__':
    app.run()