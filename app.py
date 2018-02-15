# app.py - Cool Links, a simple link shortener demo written
# with flask and intercooler.js
from datetime import datetime
import urllib

from flask import Flask, render_template, request, redirect
from peewee import SqliteDatabase, Model, AutoField, CharField, IntegerField, \
     DateTimeField, IntegrityError

db = SqliteDatabase('db.sqlite3')


class BaseModel(Model):
    class Meta:
        database = db


class Post(BaseModel):
    id = AutoField()
    short_id = CharField()
    created_at = DateTimeField()
    title = CharField()
    url = CharField(unique=True)

    def relative_time(self):
        diff = datetime.now() - self.created_at

        if diff.days > 1:
            return f'{diff.days} days ago'
        elif diff.seconds > 3600:
            return f'{diff.seconds // 3600} hours ago'
        elif diff.seconds > 60:
            return f'{diff.seconds // 60} minutes ago'
        else:
            return 'just now'


class Settings(BaseModel):
    id = AutoField()
    letter = IntegerField()
    number = IntegerField()


db.create_tables([Post, Settings])

settings = Settings.get_or_none(id=1)

if not settings:
    settings = Settings.create(letter=ord('a'), number=0)
    settings.save()


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


def valid_url(url):
    "Check URL validity"
    token = urllib.parse.urlparse(url)
    return all([getattr(token, check) for check in ('scheme', 'netloc',)])


@app.route('/submit/validate-url', methods=['POST'])
def validate_url():
    "Validate submission URL"
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


@app.route('/recent', methods=['GET'])
def recent():
    posts = Post.select().order_by(Post.created_at.desc()).limit(10)

    return render_template('recent.html', posts=posts)


@app.route('/link/<shortid>')
def link(shortid):
    post = Post.get_or_none(short_id=shortid)
    if not post:
        return f'Link {shortid} not found', 404
    return redirect(post.url)


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

    post = Post.get_or_none(url=url)

    if post:
        return render_template('post.html', post=post, post_exists=True)
    else:
        short_field = f'{chr(settings.letter)}{settings.number}'

        try:
            with db.atomic():
                settings.letter = settings.letter + 1
                if settings.letter == ord('z') + 1:
                    settings.letter = ord('a')
                    settings.number += 1
                settings.save()
                post = Post.create(created_at=datetime.now(),
                                   short_id=short_field,
                                   title=title, url=url)
        except IntegrityError:
            return 'DB integrity error'

        return render_template('post.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
