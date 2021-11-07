import datetime
import os

from random import choice
from tools import misc, config, encryption, database
from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages, Response, make_response

tokens = []
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

def gen_token():
    alph = 'qwertyuiopasdfghjklzxcvbnm'
    alph = alph + alph.upper()
    res = ""
    for i in range(50):
        res += choice(alph)
    return res

def get_id():
    return str(int(datetime.datetime.now().timestamp()))

def get_other_sites():
    sites = db.get_table("website", where="type='title'", order_by="id")
    res = []
    for site in sites:
        res.append({"txt": site[1], "id": site[5]})
    return res

def get_json_for_site__id(site_id):
    elements = db.get_table("website", where=f"site_id='{site_id}'", order_by="num") # TEXT: type, txt, data, INTEGER: num TXT: site_id, id
    res = {
        "site": [],
        "id": site_id,
        "other": get_other_sites()
    }
    if len(elements) == 0:
        res["site"].append({"type": "title", "txt": "New Page", "data": "", "id": get_id(), "num": 0})
        return res
    for elem in elements:
        res["site"].append({"type": elem[0], "txt": elem[1], "data": elem[2], "id": elem[5], "num": elem[3]})
    return res

def set_json_for_site_id(site_id, site_json):
    db.delete_from_table("website", where=f"site_id='{site_id}'")
    for node in site_json:
        db.add_to_table("website","type, txt, num, id, site_id, data" ,f"'{node['type']}', '{node['txt']}', {node['num']}, '{node['id']}', '{site_id}', '{node['data']}'")

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
        elif s[1] == 'T':
            result += 'createText(`'+s[2]+"`);"
        else:
            result += 'createHeader(`' + s[2] + "`);"
    return result


app = Flask(__name__)
app.secret_key = os.environ['TOKEN'][0:10]

db = database.Database()

school_classes, plans = get_school_classes()

@app.route('/')
def index():
    return view_site('main')

@app.route('/infa')
def infa():
    msgs = get_flashed_messages()
    if len(msgs) == 1:
        return render_template("infa.html",infa=gen_load_infa(), msg=msgs[0])
    return render_template("infa.html",infa=gen_load_infa())

@app.route("/v/<id>")
def view_site(id):
    site_json = get_json_for_site__id(id)
    return render_template("view.html", site_json=site_json, site_id=id)

@app.route("/e/<id>")
def edit_site(id):
    site_json = get_json_for_site__id(id)
    return render_template("edit.html", site_json=site_json, site_id=id, new_site_id=get_id())


@app.route('/save',  methods=['POST'])
def save_edited_json():
    token = request.cookies.get('auth', None)
    resp = Response(status=200)
    if token not in tokens:
        if not encryption.is_web_pwd_ok(request.json['pwd']):
            new_token = gen_token()
            resp.set_cookie('auth', new_token)
            tokens.append(new_token)
        else:
            return Response(status=403)
    set_json_for_site_id(request.json['id'], request.json['site'])
    return resp