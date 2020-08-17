from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://amrelsekilly@localhost:5432/todoapp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo ID: {self.id}, title: {self.title}>'


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
    if error:
        abort(500)
    if not error:
        return jsonify(data)


@app.route('/todos/<id>/update', methods=['PUT'])
def update_todo(id):
    error = False
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(id)
        todo.completed = completed
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exec_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    if not error:
        return redirect(url_for('index'))


@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    error = False
    try:
        todo = Todo.query.get(id)
        print(todo)
        Todo.query.filter_by(id=todo.id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        abort(500)
    if not error:
        return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    data = Todo.query.order_by('id').all()
    return render_template('index.html', data=data)
