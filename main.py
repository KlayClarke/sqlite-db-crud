import os
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-book-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()


# # To Update Particular Record By Query
# book_to_update = Book.query.filter_by(title='Harry Potter').first()
# book_to_update.title = 'Harry Potter and the Chamber of Secrets'
# db.session.commit()


class AddForm(FlaskForm):
    book_name = StringField(label='Book Name', validators=[DataRequired()])
    book_author = StringField(label='Book Author', validators=[DataRequired()])
    book_rating = StringField(label='Book Rating e.g, 8/10', validators=[DataRequired()])
    add_book = SubmitField(label='Add Book')


class EditForm(FlaskForm):
    new_rating = StringField(label='', validators=[DataRequired()])
    change_rating = SubmitField(label='Change Rating')


@app.route('/')
def home():
    # To Read All Records
    all_books = db.session.query(Book).all()
    num_of_books = len(all_books)
    return render_template('index.html', all_books=all_books, num_of_books=num_of_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddForm()
    if request.method == 'GET':
        form.validate_on_submit()
        return render_template('add.html', form=form)
    elif request.method == 'POST' and form.validate_on_submit():
        # Create New Record
        new_book = Book(title=form.book_name.data, author=form.book_author.data, rating=form.book_rating.data)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/edit/<book_id>', methods=['GET', 'POST'])
def edit_rating(book_id):
    form = EditForm()
    # retrieve book's data from db using id
    book = Book.query.get(book_id)
    if request.method == 'GET':
        form.validate_on_submit()
        return render_template('edit.html', form=form, book_title=book.title, book_current_rating=book.rating)
    elif request.method == 'POST' and form.validate_on_submit():
        # To Update Particular Record By ID (Primary Key)
        book.rating = form.new_rating.data
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/delete/<book_id>')
def delete_book(book_id):
    # retrieve book data
    book = Book.query.get(book_id)
    # To Delete Particular Record By ID (Primary Key)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
