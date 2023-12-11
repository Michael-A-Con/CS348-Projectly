from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import datetime 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    due_date = db.Column(db.DateTime)

# -----------------------------------------
#               UI Pages
# -----------------------------------------

# Base homepage for the website
@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)

@app.route('/Analytics')
def analytics():
    tasks = Todo.query.all()
    return render_template('analytics.html', tasks=tasks)



# -----------------------------------------
#               Actions
# -----------------------------------------
@app.route("/add", methods=["POST"])
def add():
    # add new todo
    todo_title = request.form.get("title")
    todo_due_date = request.form.get("due_date")
    
    if todo_title is None or not todo_title.strip():
        # Handle the case where todo_title is empty
        return redirect(url_for("index"))

    if todo_due_date is None or not todo_due_date.strip():
        # Handle the case where todo_title is empty
        return redirect(url_for("index"))
    
    temp = todo_due_date.split("-")
    x = datetime.datetime(int(temp[0]), int(temp[1]), int(temp[2]))

    new_todo = Todo(title=todo_title, complete=False, due_date=x)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # add new todo
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # add new todo
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/sort/<column>')
def sort_tasks(column):
    valid_columns = ['id', 'title', 'due_date', 'complete']
    
    if column not in valid_columns:
        return 'Invalid column for sorting'
    
    tasks = Todo.query.order_by(getattr(Todo, column)).all()
    return render_template('analytics.html', tasks=tasks)

@app.route('/search', methods=['POST'])
def search_tasks():
    title = request.form.get('title')
    due_date = request.form.get('due_date')
    completed = request.form.get('completed')

    filters = {}

    if title:
        filters['title'] = title

    if due_date:
        filters['due_date'] = datetime.strptime(due_date, '%Y-%m-%d')
        
    if completed:
        filters['complete'] = completed.lower() == 'true'

    tasks = Todo.query.filter_by(**filters).all()
    
    return render_template('analytics.html', tasks=tasks)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)