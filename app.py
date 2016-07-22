from flask import Flask, jsonify
import os
import json
import string
import random
from random import randint


app = Flask(__name__)
SIZE=6

def get_rnd_string():
    chars=string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(SIZE))


def get_rnd_number():
    return randint(0, 2048)


def generate_object():
    rnd_obj = {}
    for key in schema:
        elem = schema[key]
        app.logger.debug(elem['type'])
        if elem['type'] == 'string':
            rnd_obj[key] = get_rnd_string()
        if elem['type'] == 'number':
            rnd_obj[key] = get_rnd_number()
    app.logger.debug(rnd_obj)
    return rnd_obj
        # print "key: %s , value: %s" % (key, mydictionary[key])


def generate_collection():
    num_objs = randint(0, 20)
    col = []
    for x in range(1,num_objs):
        col.append(generate_object())
    return col

def load_schema():
    with open('/src/schema.json') as data_file:
        return json.load(data_file)


@app.route('/', methods=['GET'])
def hello():
    return jsonify(generate_collection())

schema = load_schema()

if __name__ == '__main__':
    load_schema()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True)
