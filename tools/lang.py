import json
from tools import misc
import langid

if __name__ == "__main__":
    raise Exception()


class Word:
    name = ""
    ends = {}
    def __init__(self, name :str, ends :dict):
        self.name = name
        self.ends = ends

words = []

with open("tools/word_list.json") as f:
    data = json.load(f)
    for key in data.keys():
        w = Word(key, data[key])
        words.append(w)

def get_pl_word(name :str, number :int):
    last_digit = str(number)[-1]
    if number in [11, 12, 13, 14]:
        last_digit = '0'
    if number == 1:
        last_digit = "x"
    for word in words:
        if word.name == name:
            for ending in word.ends.keys():
                if last_digit in ending:
                    return name + word.ends[ending]
    misc.log(f"LANG_PL: None '{name}'")
    return name

def detect_lang(text):
    return langid.classify(text)
