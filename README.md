# docmock

Docker to mock services based on a json schema.

Docmock generates a REST enpoint that returns json objects based on the schema provided. The main use case is for integration testing in isolation of 3rd party services..


There rea two ways of creating a REST endpoint. One is defining a schema, the other is just passing and `endpoint` env var and a `JSON` object:

        docker run -d -p 5000:5000 -e ENDPOINT="/things" -e JSON="$(cat object.json)" ipedrazas/docmock

This will run a cointainer that will expose an anedpoint in port 5000

        curl localhost:5000/things

Will return a collection os random objects like the one specified in `object.json`. If for example we would like to have an endpoint like `http://localhost:8080/super/long/endpoint/people` we just have to define the following JSON object like `person.json`:

        {
            "name": "a name",
            "age": 21,
            "email": "my email"
        }

then, we run our container like

        docker run -d -p 8080:5000 -e ENDPOINT="/super/long/endpoint/people" -e JSON=$(cat person.json) ipedrazas/docmock

If we now curl localhost at 8080 we will get the following response:



    -> % curl -vvv localhost:8080//super/long/endpoint/people

    *   Trying ::1...
    * Connected to localhost (::1) port 8080 (#0)
    > GET /super/long/endpoint/people HTTP/1.1
    > Host: localhost:8080
    > User-Agent: curl/7.43.0
    > Accept: */*
    >
    * HTTP 1.0, assume close after body
    < HTTP/1.0 200 OK
    < Content-Type: application/json
    < Content-Length: 762
    < Server: Werkzeug/0.11.10 Python/3.5.2
    < Date: Sat, 23 Jul 2016 15:14:39 GMT
    <
    [
      {
        "age": 403,
        "email": "23OQBK9KREHI",
        "name": "6TVPZI3OZYZV"
      },
      {
        "age": 776,
        "email": "IGVKWXXZYXBG",
        "name": "0PH1VHJYXNQK"
      },
      {
        "age": 2046,
        "email": "EWLY50D0OBKW",
        "name": "2RXQG9GDKU09"
      },
      {
        "age": 1402,
        "email": "GP1A21I53N6B",
        "name": "KPVUG2J5JAWR"
      }
    ]

Schema supports json objects:

```
JSON is built on two structures:

A collection of name/value pairs. In various languages, this is realized as an object, record, struct, dictionary, hash table, keyed list, or associative array.
An ordered list of values. In most languages, this is realized as an array, vector, list, or sequence.

```
Schema can define objects with the following attribute types:

* string
* number
* object
* collection
* bool (true / false)
* null

Both types `collection` and `object` need to specify a schema with the definition of the contained objects.


To build the container, clone the repo and run

    docker build -t your_user/docmock

To run the container in interactive mode:

    docker run -it --rm -p 5000:5000 -v $(pwd):/data ipedrazas/docmock

Or as a daemon:

    docker run -d -p 5000:5000 -v $(pwd):/data ipedrazas/docmock

Schema definition is pretty simple, you define the attribute name and include the `type` of attribute it is. In the case of a collection or an object, you add the schema:

```
        {
            "user": {
                "type":  "string"
            },
            "password":{
                "type" : "string"
            },
            "age":{
                "type" : "number"
            },
            "computer":{
                "type" : "object",
                "schema": {
                    "brand": {
                        "type" : "string"
                    }
                }
            },
            "emails":{
                "type": "list",
                "schema": {
                    "email" :{
                        "type": "string"
                    }
                }
            },
            "registered": {
                "type": "bool"
            },
            "nil": {
                "type": "null"
            }
        }
```
