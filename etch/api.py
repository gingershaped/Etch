from etch.utils import Context, PartialWrapper
from functools import partial

MIXINS = {}

class PythonModule(type):
    def __new__(meta, cls, bases, classdict, **kwargs):
        parent = kwargs["parent"]
        context = Context(parent.__context__)
        for i in classdict:
            context.vars[i] = classdict[i]
        classdict["__context__"] = context
        newcls = super().__new__(meta, cls, bases, classdict)
        parent.__context__.vars[cls] = newcls
        return newcls

    def getFunction(cls, name):
        def _(i, *args): # kludges go brr
            return PartialWrapper(cls.__context__.getFunction(name), *args)
        return _

class Mixin(type):
    def __new__(meta, cls, bases, classdict, **kwargs):
        n = bases[0].__qualname__
        if not n in MIXINS:
            MIXINS[n] = {}
        for i in classdict:
            if not i in ["__module__", "__qualname__"]:
                MIXINS[n][i] = classdict[i]
        return super().__new__(meta, cls, bases, classdict, **kwargs)