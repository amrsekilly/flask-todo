from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://amrelsekilly@localhost:5432/todoapp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo ID: {self.id}, title: {self.title}>'


db.create_all()


@app.route('/')
def index():
    data = Todo.query.all()
    return render_template('index.html', data=data)
