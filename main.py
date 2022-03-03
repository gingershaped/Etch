import etch

i = etch.Interpreter()
print(i.__context__.classes)
i.run(open("tests/simpletest.etch").read())