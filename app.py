from flask import Flask, request, render_template, redirect
import os
from uuid import uuid4
from datetime import date, timedelta

app = Flask(__name__, static_url_path='/static')


class Task:
    def __init__(self, name, description, duration):
        self.id = uuid4()
        self.name = name
        self.description = description
        self.creation_date = date.today()
        self.expiration_date = self.creation_date + timedelta(duration)
        self.completed = False

    def __str__(self):
        return f"[{self.id}] {self.name} ({self.description}) | from {self.creation_date} to {self.expiration_date}"


# list storing tasks which could be replaced by a database (data is not persisted when server is restarted)
TASKS = [
    Task(
        "Write report",
        "Report about businesss trip to UK. Don't forget to include all presentations!",
        14
    ),
    Task(
        "Record-keeping",
        "Find all legal acts about record-keeping with personal data and analyze them.",
        20
    )
]


def find_existing_task(id):
    for idx, task in enumerate(TASKS):
        if str(task.id) == id:
            return task, idx

    return None, -1


@app.route('/')
def index():
    return render_template('index.html', tasks=TASKS)


@app.route('/create-task', methods=['POST'])
def create():
    name = request.form['name']
    description = request.form['description']
    duration = int(request.form['duration'])
    new_task = Task(name, description, duration)
    TASKS.append(new_task)

    return redirect('/')


@app.route('/update-task', methods=['POST'])
def update():
    id = request.form['id'].strip()
    existing_task, idx = find_existing_task(id)
    if existing_task is None:
        return redirect("/")

    if request.form["name"]:
        existing_task.name = request.form['name']
    if request.form['description']:
        existing_task.description = request.form['description']
    if request.form['duration']:
        existing_task.expiration_date = existing_task.creation_date + timedelta(int(request.form['duration']))
    if "completed" in request.form and request.form["completed"]:
        existing_task.completed = True

    return redirect('/')


@app.route('/delete-task', methods=['POST'])
def delete():
    id = request.form['id'].strip()
    existing_task, idx = find_existing_task(id)
    if existing_task is None:
        return redirect("/")

    del TASKS[idx]

    return redirect('/')


if __name__ == '__main__':
    app.run(threaded=True, port=int(os.environ.get('PORT', 5000)))
