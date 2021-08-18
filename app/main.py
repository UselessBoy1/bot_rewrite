import datetime
import os
from tools import misc, config
from flask import Flask, render_template, url_for, request, redirect, make_response, flash, get_flashed_messages

def get_plans():
    plans = {}
    # for every file in school_classes directory
    for school_class, data in misc.get_every_school_class_json():
        # check if file is correct
        missing = misc.check_dict(['plan'], data)
        if len(missing) > 0:
            continue
        name = school_class
        plan = data['plan']
        plans[name] = plan
    return plans


app = Flask(__name__)
app.secret_key = os.environ['TOKEN'][0:10]
@app.route('/')
def index():
    msgs = get_flashed_messages()
    if len(msgs) == 1:
        return render_template("index.html", plan=str(get_plans()), msg=msgs[0])
    return render_template("index.html", plan=str(get_plans()))

@app.route('/add', methods= ['POST', 'GET'] )
def add():
    if request.method == 'GET':
        return redirect(url_for('index'), code=301)
    else:
        plan = get_plans()
        sc = request.form['sc']
        d = int(request.form['weekday'])
        i, li = [int(x) for x in request.form['lessons'].split('.')]
        year, month, day = [int(x) for x in request.form['date'].split("-")]
        flash(f"Zapisano {request.form['text']} {plan[sc][d][i][li]} {request.form['date']}")
        datetime_v = datetime.datetime(year, month, day, config.LESSON_TIMES[i][0], config.LESSON_TIMES[i][1])
        print(datetime_v.timestamp())

        return redirect(url_for('index'), code=303)