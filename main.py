from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Book(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(250),unique=True,nullable=False)
    author=db.Column(db.String(250),nullable=False)
    rating=db.Column(db.Float,nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

db.create_all()




@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html',books=all_books,n=len(all_books))


@app.route("/add",methods=["POST","GET"])
def add():
    if request.method=="POST":
        title=request.form["name"]
        author=request.form["author"]
        rating=request.form["rating"]
        new_book=Book(title=title,author=author,rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route("/edit/id=<id>",methods=["POST","GET"])
def edit(id):
    book=Book.query.get(id)
    if request.method=="POST":
        new_rating=request.form["new_rating"]
        book.rating=new_rating
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html',book=book)

@app.route("/delete/<id>")
def delete(id):
    book=Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

