import etch.api
import random

def setup(interpreter):
    class Rand(metaclass = etch.api.PythonModule, parent = interpreter):
        def randint(min, max):
            return random.randint(min, max)
        def random():
            return random.random()
        def yn():
            return bool(random.randint(0, 1))