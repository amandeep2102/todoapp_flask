from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
db = SQLAlchemy(app)
app.app_context().push()

class Data(db.Model):
    __tablename__ = "data"
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Data(title=title, description=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Data.query.all()
    return render_template('index.html', alltodo=alltodo)

@app.route('/show')
def show():
    alltodo = Data.query.all()
    print(alltodo)
    return "hello world"

@app.route('/done/<int:sno>')
def delete(sno):
    todo = Data.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods=['POST', 'GET'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Data.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = desc
        db.session.commit()
        return redirect('/')
    todo = Data.query.filter_by(sno=sno).first()
    return render_template("update.html", todo = todo)

if __name__ == '__main__':
    app.run()