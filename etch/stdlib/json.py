import etch.api
import json

def setup(i):
    class Json(metaclass = etch.api.PythonModule, parent = i):
        def parse(data):
            return json.loads(data)
        def dump(data):
            return json.dumps(data)