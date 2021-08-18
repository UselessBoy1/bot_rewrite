from tools import database, misc

LESSON_TIMES = [[8, 0], [8, 50], [9, 45], [10, 45], [11, 40], [12, 35], [13, 35], [14, 30], [15, 20]]
LESSON_TIMES_ENDS = [[8, 45], [9, 35], [10, 30], [11, 30], [12, 25], [13, 20], [14, 20], [15, 15], [16, 5]]

def check_database():
    global v
    db = database.Database()
    output = db.get_table("config")
    resolved = misc.resolve_config_table(output)
    v = def_v.copy()
    for key in v.keys():
        if key in resolved.keys():
            v[key] = resolved[key]


v = {
    'HELP_COLOR': 0x2ecc71,
    'LINK_COLOR': 0x9b59b6,
    'HOMEWORK_COLOR': 0xf1c40f,
    'REDDIT_COLOR': 0xe74c3c,
    'CONFIG_COLOR': 0x3498db,
    'DATE_CHANNEL': 740525989788123218,
    'SECONDS_BEFORE_LINK': 100,
    'HOLIDAY': 0
}

def_v = v.copy()

check_database()