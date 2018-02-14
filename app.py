# app.py - Cooler News, an HN-alike website written with Flask & intercooler
# from bottle import route, run, view, static_file, post, get, request, static_file
from datetime import datetime
from pprint import pprint
import urllib

from flask import Flask, render_template, request
from peewee import SqliteDatabase, Model, AutoField, CharField, IntegerField, \
     DateTimeField, ForeignKeyField

db = SqliteDatabase('db.sqlite3')


class BaseModel(Model):
    class Meta:
        database = db


class Post(BaseModel):
    id = AutoField()
    created_at = DateTimeField()
    title = CharField()
    url = CharField()
    username = CharField()


db.create_tables([Post])


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


def valid_url(url):
    token = urllib.parse.urlparse(url)
    return all([getattr(token, check) for check in ('scheme', 'netloc',)])


@app.route('/submit/validate-url', methods=['POST'])
def validate_url():
    "Validate submission URL"
    # result = urlparse(request.form['url'])
    if not valid_url(request.form['url']):
        return render_template('index_url.html', url_error='Not a valid URL',
                               url=request.form['url'])
    return render_template('index_url.html', url=request.form['url'])


@app.route('/submit/validate-title', methods=['POST'])
def validate_title():
    "Validate submission title"
    title = request.form['title']
    if len(title) < 3 or len(title) > 255:
        return render_template('index_title.html', title=request.form['title'],
                               title_error='Title must be '
                               'between 3 and 255 characters')
    return render_template('index_title.html', title=request.form['title'])


@app.route('/submit', methods=['POST'])
def submit():
    url = request.form['url']
    title = request.form['title']

    if not valid_url(request.form['url']):
        return render_template('submit.html',
                               url=request.form['url'],
                               title=request.form['title'],
                               url_error='Not a valid URL')
    elif len(title) < 3 or len(title) > 255:
        return render_template('submit.html', url=request.form['url'],
                               title=request.form['title'],
                               title_error='Title must be'
                               ' between 3 and 255 characters')

    post = Post.create(created_at=datetime.now(), title=title, url=url, username='guest')

    return render_template('post.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
