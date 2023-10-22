import wtforms
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditorField, CKEditor
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL
from datetime import date
from werkzeug.urls import url_encode

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
ckeditor = CKEditor(app)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# app.config['CKEDITOR_PKG_TYPE'] = 'full'
# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class NewForm(FlaskForm):
    blog_post_title = StringField('Blog Post Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    your_name = StringField('Your Name', validators=[DataRequired()])
    blog_image_url = StringField('Blog Image Url', validators=[DataRequired()])
    # post_body = TextAreaField('The Blog')
    content = CKEditorField('Content')
    submit = SubmitField()


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.

    posts1 = []
    result = db.session.execute(db.select(BlogPost)).scalars()  # same query results
    data = BlogPost.query.all()  # same query results
    posts1 = result.all()
    # for item in result:
    #     posts.append(item)
    return render_template("index.html", all_posts=posts1)


# TODO: Add a route so that you can click on individual posts.
@app.route('/read_post/<post_id>', methods=['GET'])
def read_individual_post(post_id):
    # db by id
    render_template('index.html', post_id=post_id)


@app.route('/show_post_byid/<post_id>', methods=['GET'])
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    # "Grab the post from your database"
    # requested_post = db.session.execute(db.select(BlogPost).filter_by(id=post_id)).scalar_one()
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/add_new_post/', methods=['GET', 'POST'])
def add_post():
    form = NewForm()
    if form.validate_on_submit():
        flash('Form validated!')
        form.your_name = 'shlomo22'
        print(request.form.get('blog_post_title'))
        print(request.form.get('subtitle'))
        add_blog = BlogPost(title=request.form.get('blog_post_title'),
                            subtitle=request.form.get('subtitle'),
                            author=request.form.get('your_name'),
                            img_url=request.form.get('blog_image_url'),
                            body=request.form.get('content'),
                            date=date.today().strftime("%b, %d, %Y"))

        db.session.add(add_blog)
        db.session.commit()
        return redirect(url_for('get_all_posts'))

    return render_template("make_post.html", form=form, neworedit_post='New-Post', welcome='You are going to make a '
                                                                                           'great blog post!')


# TODO: edit_post() to change an existing blog post
@app.route("/edit-post/<post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    form = NewForm()
    yahoo='yahooo'

    return render_template('make_post.html', neworedit_post="Edit Post", form=form,yahoo=yahoo)


# TODO: delete_post() to remove a blog post from the database

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)

# " {{ render_field(form.body) }}-->"
