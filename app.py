from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    data = [{
        'title': 'Todo 1'
    }, {
        'title': 'Todo 2'
    }, {
        'title': 'Todo 3'
    }]
    return render_template('index.html', data=data)
