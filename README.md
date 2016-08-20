# docmock

[![](https://images.microbadger.com/badges/image/ipedrazas/docmock.svg)](https://microbadger.com/images/ipedrazas/docmock "Get your own image badge on microbadger.com")

Docker to mock services based on a json file or a json schema.

Docmock generates a REST enpoint that returns json objects based on the schema provided. The main use case is for integration testing in isolation of 3rd party services..


There are two ways of creating a REST endpoint. One is defining a schema, the other is just passing and `endpoint` env var and a `JSON` object, you can also specify the maximum objects returned using the `MAX` env var. :

        docker run -d -p 5000:5000 -e ENDPOINT="/things" -e MAX=5 -e JSON="$(cat object.json)" ipedrazas/docmock

This will run a cointainer that will expose an endpoint in port 5000

        -> % curl localhost:8080/people
        [
          {
            "age": 475,
            "email": "8S90QNHLLWGZ",
            "name": "IV3FS8UO0DUK"
          },
          {
            "age": 13,
            "email": "NMBRJD33U4MY",
            "name": "01IKNMR3NB7K"
          },
          {
            "age": 931,
            "email": "W2F66PQ5U6YS",
            "name": "7EFR7AE8R97U"
          },
          {
            "age": 464,
            "email": "4GBAJLVQDSTK",
            "name": "TP79O5HN79XR"
          }
        ]

Will return a collection os random objects like the one specified in `object.json`. If for example we would like to have an endpoint like `http://localhost:8080/super/long/endpoint/people` you just have to define the following JSON object `person.json`:

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

## Kubernetes support

In order to use `docmock` inside a kubernetes cluster, you can inject the json file base64 encoded using the env var 'BJSON'. For example, the next container will create an endpoint in `http://localhost:5000/srv1`

    docker run -it -p 5000:5000 \
      -e BJSON="ewogICJuYW1lIjogIkl2YW4iLAogICJBZ2UiOiA0Mgp9Cg==" \
      -e ENDPOINT=srv1 \
    ipedrazas/docmock


This service will return a collection of objects similar to:

    echo "ewogICJuYW1lIjogIkl2YW4iLAogICJBZ2UiOiA0Mgp9Cg==" | base64 -D
    {
    "name": "Ivan",
    "Age": 42
    }

## Dependencies

Sometimes we want the health check to verify if the dependencies are healthy too. To inject dependencies into the container we have to use the env var `DEPENDENCIES`. Dependencies will be a sequence of urls comma separated.

Let's assume we want to create a service that exposes an endpoint as 'http://localhost:5000/srv3' that has two dependencies: `http://localhost:5001/srv1` and `http://localhost:5000/srv2`, we should call our docker container as follows:

    docker run -it -p 5000:5000 \
      -e BJSON="ewogICJuYW1lIjogIkl2YW4iLAogICJBZ2UiOiA0Mgp9Cg==" \
      -e ENDPOINT=srv2 \
      -e DEPENDENCIES="http://localhost:5000/srv1,http://localhost:5000/srv2"
    ipedrazas/docmock
