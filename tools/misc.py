import datetime
import pytz
import discord
import json
import os
from os.path import  isfile, join

if __name__ == "__main__":
    raise Exception()

class Task:
    channel_id = 0
    epoch = 0
    lesson = ""
    msg = ""
    def __init__(self, channel_id, epoch, lesson, msg):
        self.channel_id = int(channel_id)
        self.epoch = int(epoch)
        self.lesson = lesson
        self.msg = msg

class Subreddit:
    name = ""
    def __init__(self, name):
        self.name = name

def resolve_tasks_table(output):
    """
    :param output: output from database tasks request
    :return: list of Task objects
    """
    values = []
    for row in output:
        values.append(Task(row[0], row[1], row[2], row[3]))
    return values


def resolve_config_table(output):
    """
    :param output: output from database config request
    :return: dict od config options
    """
    values = {}
    for row in output:
        name = row[0]
        value = row[1]
        if row[2] != 0:
            value = int(value, 0)
        values[name] = value
    return values

def resolve_reddit_table(output):
    """
    :param output: output from database reddit request
    :return: list of SubReddit objects
    """
    values = []
    for row in output:
        values.append(Subreddit(row[0]))
    return values

def get_every_school_class_json():
    for school_class in [d for d in os.listdir("school_classes") if isfile(join("school_classes", d))]:
        with open(join("school_classes", school_class)) as f:
            yield school_class.lower().replace(".json", ""), json.load(f)

def get_now():
    """
    :return: datetime.now() in Europe/Warsaw timezone
    """
    return datetime.datetime.now(pytz.timezone("Europe/Warsaw"))

def check_dict(keys :list, d :dict):
    """
    :param keys: keys to check
    :param d: dict
    :return: keys that arent in dictionary d
    """
    not_in = []
    for k in keys:
        if k not in d.keys():
            not_in.append(k)
    return not_in


def in_voice_channel(member :discord.Member):
    if member.voice is not None:
        if member.voice.channel is not None:
            return True
    return False


def log(msg):
    print(f"BOT:", msg)