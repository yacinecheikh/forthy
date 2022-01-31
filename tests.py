from parse import parse

print(parse("'() ."))
print(parse("(head [cons(a, b) - a] 0 extract) define"))
print(parse(""))
