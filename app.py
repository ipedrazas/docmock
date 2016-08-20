"""DockMock - API to mock REST APIs."""
import json
import numbers
import os
import random
import string
import base64
from requests_futures.sessions import FuturesSession


from flask import Flask, jsonify, abort


app = Flask(__name__)
SIZE = 12

SMAX = os.environ.get("MAX", "20")

if SMAX:
    MAX = int(SMAX)


def get_rnd_string():
    """Generate randon string."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(SIZE))


def get_rnd_number(top=2048):
    """Generate random number."""
    return random.randint(1, top)


def get_rnd_bool():
    """Generate random bool."""
    return bool(random.getrandbits(1))


def define_collection(jobj):
    """Return a collection of objects."""
    num_objs = random.randint(1, MAX)
    col = []
    for x in range(1, num_objs):
        col.append(define_object(jobj))
    return col


def define_object(jobj):
    """Create an object from a json object."""
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
    """Generate an object from a schema definition."""
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
    """Generate a collection using schema."""
    num_objs = random.randint(1, MAX)
    col = []
    for x in range(1, num_objs):
        col.append(generate_object(obj_schema))
    return col


def load_object():
    """Load json objevt from local json file."""
    base = os.environ.get("JSON")
    bbase = os.environ.get("BJSON")

    if base:
        return json.loads(base)
    if bbase:
        bjson = base64.b64decode(bbase.encode('ascii'))
        return json.loads(bjson.decode('ascii'))
    else:
        with open('/data/object.json') as data_file:
            return json.load(data_file)


def load_schema():
    """Load scheam from local file."""
    schema = os.environ.get("SCHEMA")
    if schema:
        return json.loads(schema)
    else:
        with open('/data/schema.json') as data_file:
            return json.load(data_file)


@app.route('/', methods=['GET'])
def hello():
    """Default endpoint."""
    return "docmock v0.1"

def http_callback(sess, resp):
    app.logger.debug(resp.text)

def check_dependencies():
    healthy = True
    urls = dependencies.split(",")
    session = FuturesSession()
    try:
        for url in urls:
            future = session.get(url, background_callback=http_callback)
            response = future.result()
            if response.status_code != 200:
                healthy = False
    except Exception as e:
        return False
    return healthy


@app.route('/_status/healthz', methods=['GET'])
def healthz():
    """Health check endpoint."""
    if dependencies:
        app.logger.debug("checking dependencies")
        ret = check_dependencies()
        if not ret:
            # return 412 Precondition Failed (RFC 7232)
            # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
            abort(412)
    return "healthy"


endpoint = os.environ.get("ENDPOINT")
if not endpoint.startswith('/'):
    endpoint = "/" + endpoint

jobj = load_object()

dependencies = os.environ.get("DEPENDENCIES")
envdebug = os.environ.get("DEBUG")

debug = False
if envdebug and envdebug.lower() == "true":
    debug = True

if not endpoint:
    schema = load_schema()
    endpoint = schema['endpoint']


@app.route(endpoint, methods=['GET'])
def endpoint():
    """Endpoint exposed."""
    if jobj:
        return jsonify(define_collection(jobj))
    if schema:
        return jsonify(generate_collection(schema['schema']))
    return "Define json object or schema, please"

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=debug,
        threaded=True)
