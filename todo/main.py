from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

#Flask()を使ってFlaskの機能を使えるappインスタンスを作っています
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite'

#データーベースを作成
db = SQLAlchemy(app)
class Task(db.Model):
    
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text())
    status = db.Column(db.Integer)
    
#テキストと違う[ 追加：with app.app_context(): ]
with app.app_context():
    db.create_all()

#ルーティングとindexにアクセスされた場合の処理を記述
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks = tasks)

#app.run()でアプリケーションを起動する！
app.run(debug=True, host=os.getenv('APP_ADDRESS', 'localhost'), port=8001)

#終了