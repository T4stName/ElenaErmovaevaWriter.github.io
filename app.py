from logging import DEBUG, debug, fatal
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from werkzeug.utils import redirect
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_db.db'
app.config['SQLITE_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title =  db.Column(db.String(100), nullable = False)
    intro =  db.Column(db.String(300), nullable  = False)
    text  =  db.Column(db.Text, nullable  = False)
    date =  db.Column((db.DateTime), default=datetime.utcnow)
    link = db.Column(db.Text, nullable  = False)

    def __repr__(self):
       return '<Article %r>' % self.id

@app.before_first_request
def create_tables():
    db.create_all()
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/info')
def about_info():
    return render_template("info.html")



@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()) .all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
   article = Article.query.get(id)
   return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
   article = Article.query.get_or_404(id)

   try:
       db.session.delete(article)
       db.session.commit()
       return redirect('/posts')
   except:
        return "При удалении записи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST','GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article. text = request.form['text']
        article.link = request.form['link']
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании записи произошла ошибка"
    else:
     
     return render_template("post_update.html", article =article)



@app.route('/create-article', methods=['POST','GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        link = request.form['link']
        article = Article(title = title, intro = intro,text = text, link = link)

        try:
            print("COOL")
            #db.commit()
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении записи произошла ошибка"
    else:
     return render_template("create-article.html")




if __name__ == "__main__":
    app.run(debug=True)
