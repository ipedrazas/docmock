# docmock

Docker to mock services based on a json schema.

Docmock generates a REST enpoint that returns json objects based on the schema provided. The main use case is for integration testing in isolation of 3rd party services..


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
