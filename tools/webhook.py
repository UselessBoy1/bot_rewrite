import os
from urllib.request import Request, urlopen
from json import dumps

HEADERS_JSON = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
}

WEBHOOK_URL = os.environ['WEBHOOK']

class Embed:
    def __init__(self, title="", description="", color=0x7289da):
        self.title = title
        self.description = description
        self.color = color
        self.fields = []

    def add_field(self, name, value, inline=False):
        self.fields.append({
            "name": name,
            "value": value,
            "inline": inline
        })

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "color": self.color,
            "fields": self.fields
        }

def send(username: str, content: str, embeds: list[Embed]):

    webhook = {
        "content": content,
        "embeds": [embed.to_dict() for embed in embeds],
        "username": username # msg display username / when clicked will show webhook name
    }

    try:
        urlopen(Request(WEBHOOK_URL, data=dumps(webhook).encode(), headers=HEADERS_JSON))
    except Exception as e:
        print(e)
