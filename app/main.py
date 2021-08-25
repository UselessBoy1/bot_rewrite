import datetime
import os

from tools import misc, config, encryption, database
from flask import Flask, render_template, url_for, request, redirect, make_response, flash, get_flashed_messages

def get_school_classes():
    school_classes = {}
    plans = {}
    # for every file in school_classes directory
    for school_class, data in misc.get_every_school_class_json():
        # check if file is correct
        missing = misc.check_dict(['plan'], data)
        if len(missing) > 0:
            continue
        name = school_class
        school_classes[name] = data
        plans[name] = data['plan']
    return school_classes, plans

def get_tasks():
    tasks = {}
    tasks_obj = misc.resolve_tasks_table(db.get_table("tasks"))
    for task_obj in tasks_obj:
        if task_obj.lesson not in tasks.keys():
            tasks[task_obj.lesson] = []
        tasks[task_obj.lesson].append([task_obj.epoch, task_obj.msg])
    return tasks


app = Flask(__name__)
app.secret_key = os.environ['TOKEN'][0:10]

db = database.Database()

school_classes, plans = get_school_classes()

@app.route('/')
def index():
    tasks = get_tasks()
    msgs = get_flashed_messages()
    if len(msgs) == 1:
        return render_template("index.html", plan=str(plans), tasks=tasks, msg=msgs[0])
    return render_template("index.html", plan=str(plans),tasks=tasks)

@app.route('/add', methods= ['POST', 'GET'] )
def add():
    if request.method == 'GET':
        return redirect(url_for('index'), code=301)
    else:

        school_class = request.form['sc']
        weekday = int(request.form['weekday'])
        lesson_num, lesson_index = [int(x) for x in request.form['lessons'].split('.')]
        year, month, day = [int(x) for x in request.form['date'].split("-")]
        flash(f"Zapisano {request.form['text']} {plans[school_class][weekday][lesson_num][lesson_index]} {request.form['date']}")
        datetime_epoch = datetime.datetime(year, month, day, config.LESSON_TIMES[lesson_num][0], config.LESSON_TIMES[lesson_num][1]).timestamp()
        crypto = encryption.encrypt(request.form['text']).decode("UTF-8")

        db.add_to_table("tasks", "channel_id, epoch, lesson, msg", f"'{school_classes[school_class]['channel_id']}', '{int(datetime_epoch)}', '{school_class}', '{crypto}'")

        return redirect(url_for('index'), code=303)