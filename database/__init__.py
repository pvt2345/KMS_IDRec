import json
from . import base,database,mysql_utils

db = 2
if db==0:
    DataBase = database.TextMiningDB
elif db==1:
    DataBase = base.Database
else:
    DataBase = mysql_utils.DataAccess


data = []
def load_data(path):
    global data
    data = json.load(open(path,encoding='utf-8'))
    return data


def get_reference(id):
    # d=None
    print(id)
    print(data)
    for dt in data:
        if dt['id'] and id == int(dt['id']):
            d=dt.copy()
            print(d)
            return d
    return None