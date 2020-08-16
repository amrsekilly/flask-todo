from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys

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


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    data = {}
    try:
        title = request.get_json()['title']
        todo = Todo(title=title)
        db.session.add(todo)
        db.session.commit()
        data = {'title': todo.title}
    except:
        error = True
        db.session.rollback()
        print(sys.exec_info())
    finally:
        db.session.close()
    if not error:
        return jsonify(data)


@app.route('/')
def index():
    data = Todo.query.all()
    return render_template('index.html', data=data)
