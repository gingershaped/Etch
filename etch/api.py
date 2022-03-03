from etch.utils import Context, PartialWrapper
from functools import partial

class PythonModule(type):
    def __new__(meta, cls, bases, classdict, **kwargs):
        parent = kwargs["parent"]
        context = Context(parent.__context__)
        for i in classdict:
            if type(classdict[i]).__name__ == "function":
                context.functions[i] = classdict[i]
            else:
                context.vars[i] = classdict[i]
        classdict["__context__"] = context
        newcls = super().__new__(meta, cls, bases, classdict)
        parent.__context__.classes[cls] = newcls
        return newcls

    def getFunction(cls, name):
        def _(i, *args): # kludges go brr
            return PartialWrapper(cls.__context__.getFunction(name), *args)
        return _

