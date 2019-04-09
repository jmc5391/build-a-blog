from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(400))
    date = db.Column(db.DateTime)

    def __init__(self, title, body, date=None):

        self.title = title
        self.body = body
        if date is None:
            date = datetime.utcnow()
        self.date = date

@app.route('/')
def index():

    return redirect('/blog')

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':

        title_error = ''
        body_error = ''
        post_title = request.form['title']
        post_body = request.form['body']

        if post_title == '':

            title_error = 'Please enter a title!'

        if post_body == '':

            body_error = 'Please enter your post!'

        if not title_error and not body_error:

            new_post = Blog(post_title, post_body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog?id=' + str(new_post.id))

        else:

            return render_template('newpost.html', title = 'New Post', post_title = post_title, post_body = post_body,
             title_error = title_error, body_error = body_error)

    return render_template('newpost.html', title = 'New Post', post_title = 'Title')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'GET':
        if request.args.get('id'):
            post_id = int(request.args.get('id'))
            current_post = Blog.query.get(post_id)
            return render_template('current.html', post=current_post)

    posts = Blog.query.order_by(desc(Blog.date)).all()
    return render_template('blog.html', title='My Blog', posts=posts)

if __name__ == '__main__':
    app.run()