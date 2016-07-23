import json
import numbers
import os
import random
import string


from flask import Flask, jsonify


app = Flask(__name__)
SIZE = 12


def get_rnd_string():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(SIZE))


def get_rnd_number():
    return random.randint(0, 2048)


def get_rnd_bool():
    return bool(random.getrandbits(1))


def define_collection(jobj):
    num_objs = random.randint(0, 20)
    col = []
    for x in range(1, num_objs):
        col.append(define_object(jobj))
    return col


def define_object(jobj):
    rnd_obj = {}
    for key, value in jobj.items():
        if type(value) is str:
            rnd_obj[key] = get_rnd_string()
        if isinstance(value, numbers.Number):
            rnd_obj[key] = get_rnd_number()
        if isinstance(value, (dict)):
            rnd_obj[key] = define_object(value)
        if isinstance(value, (list)):
            # we just need to analyse the first object
            rnd_obj[key] = define_collection(value[0])

    return rnd_obj


def generate_object(obj_schema):
    rnd_obj = {}
    for key in obj_schema:
        elem = obj_schema[key]
        if elem['type'] == 'string':
            rnd_obj[key] = get_rnd_string()
        if elem['type'] == 'number':
            rnd_obj[key] = get_rnd_number()
        if elem['type'] == 'bool':
            rnd_obj[key] = get_rnd_bool()
        if elem['type'] == 'null':
            rnd_obj[key] = None
        if elem['type'] == 'object':
            rnd_obj[key] = generate_object(elem['schema'])
        if elem['type'] == 'list':
            rnd_obj[key] = generate_collection(elem['schema'])
    return rnd_obj


def generate_collection(obj_schema):
    num_objs = random.randint(0, 20)
    col = []
    for x in range(1, num_objs):
        col.append(generate_object(obj_schema))
    return col


def load_object():
    base = os.environ.get("JSON")
    app.logger.debug(base)
    if base:
        return json.loads(base)
    else:
        with open('/data/object.json') as data_file:
            return json.load(data_file)


def load_schema():
    schema = os.environ.get("SCHEMA")
    if schema:
        return json.loads(schema)
    else:
        with open('/data/schema.json') as data_file:
            return json.load(data_file)


@app.route('/', methods=['GET'])
def hello():
    return "docmock v0.1"


endpoint = os.environ.get("ENDPOINT")
jobj = load_object()

if not endpoint:
    schema = load_schema()


@app.route(endpoint, methods=['GET'])
def endpoint():
    return jsonify(define_collection(jobj))
    # return jsonify(generate_collection(schema['schema']))

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True)
