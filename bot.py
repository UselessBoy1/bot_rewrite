import discord
import os
import traceback
import sys
import threading
import asyncio
import datetime

from discord.ext import commands
from os.path import isfile, join
from tools import database, misc, config
from flask import Flask, render_template, url_for, request, redirect, make_response, flash, get_flashed_messages

CMD_PREFIXES = ["t?", "T?"]
pending_index = -1

def get_cogs():
    for f in os.listdir("cogs"):
        if isfile(join("cogs", f)) and not f.startswith("_"):
            yield f.replace(".py", "")

def load_cogs(bot):
    for cog in get_cogs():
        try:
            bot.load_extension("cogs" + "." + cog)
        except Exception as e:
            misc.log(f"Can't load extension: {cog}")
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)


def create_default_tables():
    db = database.Database()
    db.create_table("tasks", "channel_id TEXT, epoch TEXT, lesson TEXT, msg TEXT")
    db.create_table("config", "namex TEXT, valuex TEXT, isint INTEGER")
    db.create_table("reddit", "followed TEXT")


def run_bot(loop):
    asyncio.set_event_loop(loop)

    create_default_tables()

    bot = commands.Bot(command_prefix=CMD_PREFIXES, intents=discord.Intents.all(), help_command=None)

    @bot.event
    async def on_ready():
        misc.log("READY")

    @bot.event
    async def on_pending_reminder_set(reminder):
        global pending_index
        pending_index = reminder.index


    load_cogs(bot)
    token = os.environ["TOKEN"]
    bot.run(token, bot=True, reconnect=True)

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

def run_app():
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

    app.run(port=80)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    thread_bot = threading.Thread(target=run_bot, args=(loop,))
    thread_app = threading.Thread(target=run_app)
    thread_bot.start()
    thread_app.start()
    thread_bot.join()
    thread_app.join()

