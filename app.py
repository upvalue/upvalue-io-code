# app.py - Cooler News, an HN-alike website written with Flask & intercooler
# from bottle import route, run, view, static_file, post, get, request, static_file
from flask import Flask, render_template, request
from peewee import SqliteDatabase, Model, AutoField, CharField, IntegerField, \
     DateTimeField, ForeignKeyField
from pprint import pprint
import urllib
# from datetime import datetime

db = SqliteDatabase('db.sqlite3')


class BaseModel(Model):
    class Meta:
        database = db


class Post(BaseModel):
    id = AutoField()
    created_at = DateTimeField()
    title = CharField()
    url = CharField()
    body = CharField()
    username = CharField()


class Comment(BaseModel):
    id = AutoField()
    created_at = DateTimeField()
    post = ForeignKeyField(Post, backref='comments')
    content = CharField()
    username = CharField()


class PostVote(BaseModel):
    id = AutoField()
    post = ForeignKeyField(Post, backref='post')
    value = IntegerField()


class CommentVote(BaseModel):
    id = AutoField()
    post = ForeignKeyField(Post, backref='post')
    value = IntegerField()


db.create_tables([Post, Comment])


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/submit/url', methods=['POST'])
def submit():
    # result = urlparse(request.form['url'])
    pprint(request.form)
    token = urllib.parse.urlparse(request.form['url'])
    if not all([getattr(token, check) for check in ('scheme', 'netloc',)]):
        return render_template('index_url.html', url_error = 'Not a valid URL')
    # return render_template('post.html')

if __name__ == '__main__':
    app.run(debug=True)