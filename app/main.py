import datetime
import os

from tools import misc, config, encryption, database
from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages, Response, make_response

ips = ['127.0.0.1']
save = []
tmp_save = []

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

def gen_load_infa():
    site = db.get_table('site', order_by='id')
    result = ""
    for s in site:
        if s[1] == 'C':
            result += 'createCode(`'+s[2]+"`);"
        else:
            result += 'createText(`'+s[2]+"`);"
    return result


app = Flask(__name__)
app.secret_key = os.environ['TOKEN'][0:10]

db = database.Database()

school_classes, plans = get_school_classes()

@app.route('/')
def index():
    msgs = get_flashed_messages()
    if len(msgs) == 1:
        return render_template("index.html", msg=msgs[0])
    return render_template("index.html")

@app.route('/infa')
def infa():
    msgs = get_flashed_messages()
    if len(msgs) == 1:
        return render_template("infa.html",infa=gen_load_infa(), msg=msgs[0])
    return render_template("infa.html",infa=gen_load_infa())

@app.route('/login')
def login():
    cookie = request.cookies.get('auth', None)
    ip = request.remote_addr
    if cookie == ip and cookie in ips:
        return redirect('/admin')
    msgs = get_flashed_messages()
    if len(msgs) == 1:
        return render_template("adminlogin.html", msg=msgs[0])
    return render_template('adminlogin.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect('/login'))
    resp.set_cookie('auth', '', expires=0)
    return resp

@app.route("/admin", methods= ['POST', 'GET'])
def admin():
    cookie = request.cookies.get('auth', None)
    ip = request.remote_addr
    if cookie not in ips or cookie != ip:
        if request.method == 'GET':
            return redirect('login')
        else:
            try:
                pwd = request.form['pwd']
                if encryption.is_web_pwd_ok(pwd):
                    flash("Zle haslo")
                    return redirect('login')
            except:
                 return Response(status=403)


    tasks = get_tasks()
    msgs = get_flashed_messages()
    if request.remote_addr not in ips:
        ips.append(request.remote_addr)
    if len(msgs) == 1:
        resp = make_response(render_template("admin.html",infa=gen_load_infa(), plan=str(plans), tasks=tasks, msg=msgs[0]))
    else:
        resp = make_response(render_template("admin.html",infa=gen_load_infa(), plan=str(plans), tasks=tasks))
    resp.set_cookie('auth', request.remote_addr)
    return resp

@app.route('/startsave')
def start_save():
    cookie = request.cookies.get('auth', None)
    ip = request.remote_addr
    if cookie not in ips or cookie != ip:
        return Response(status=403)
    tmp_save.clear()
    return Response(status=200)

@app.route('/save', methods=['POST'])
def save_elem():
    cookie = request.cookies.get('auth', None)
    ip = request.remote_addr
    if cookie not in ips or cookie != ip:
        return Response(status=403)
    data = request.data.decode("UTF-8")
    if data.startswith("text="):
        tmp_save.append(("T", data[5:]))
    elif data.startswith("code="):
        tmp_save.append(("C",data[5:]))
    return Response(status=200)

@app.route('/endsave')
def end_save():
    cookie = request.cookies.get('auth', None)
    ip = request.remote_addr
    if cookie not in ips or cookie != ip:
        return Response(status=403)
    site = db.get_table('site')
    num = len(site)
    x = 0
    for t in tmp_save:
        code = t[1].replace("'", "''")
        if x < num:
            db.replace_in_table('site', ['type', 'valuex'], [f"'{t[0]}'", f"'{code}'"], where=f'id={x}')
            x+=1
        else:
            db.add_to_table('site', 'id, type, valuex', f"{num}, '{t[0]}', '{code}'")
            num+=1
    if x < len(site):
        db.delete_from_table('site', f'id >= {x}')
    return Response(status=200)

@app.route('/sendadd', methods= ['POST', 'GET'] )
def send_add():
    if request.method == 'GET':
        return redirect(url_for('index'), code=301)
    else:
        cookie = request.cookies.get('auth', None)
        ip = request.remote_addr
        if cookie not in ips or cookie != ip:
            return Response(status=403)

        school_class = request.form['sc']
        weekday = int(request.form['weekday'])
        lesson_num, lesson_index = [int(x) for x in request.form['lessons'].split('.')]
        year, month, day = [int(x) for x in request.form['date'].split("-")]
        flash(f"Zapisano {request.form['text']} {plans[school_class][weekday][lesson_num][lesson_index]} {request.form['date']}")
        datetime_epoch = datetime.datetime(year=year,month=month, day=day,hour=config.LESSON_TIMES[lesson_num][0],minute=config.LESSON_TIMES[lesson_num][1]).timestamp()
        crypto = encryption.encrypt(request.form['text']).decode("UTF-8")

        db.add_to_table("tasks", "channel_id, epoch, lesson, msg", f"'{school_classes[school_class]['channel_id']}', '{int(datetime_epoch)}', '{school_class}', '{crypto}'")

        return redirect(url_for('admin'), code=307)