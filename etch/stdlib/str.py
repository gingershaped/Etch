import etch.api
import string

def setup(i):
    class str(metaclass=etch.api.PythonModule, parent=i):
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        letters = string.ascii_letters