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

#登録処理用の関数。
@app.route('/new', methods=["POST"])
#上の部分について、@app.routeの1つ目の引数に/newを設定している。
#だから、下のコードははlocalhost:8001/newでリクエストされたときに作動する。
def new():
    task = Task()
    task.text = request.form["new_text"]
    task.status = 0
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

#完了処理用の関数
@app.route('/completion')
def completion():
    id = request.form["id"]
    task = Task.query.filter_by(id=id).first()
    task.status = 1
    db.session.commit()
    return redirect(url_for('index'))
#上の部分について
#htmlのフォームからidを受け、Task.query.filter_by()を使ってデータを取得。
#数字で完了(1)・未完了(0)を判断

#app.run()でアプリケーションを起動する！
app.run(debug=True, host=os.getenv('APP_ADDRESS', 'localhost'), port=8001)

#終了