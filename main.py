from parse import parse

with open("bootstrap.fy") as f:
    source = f.read()

print(parse(source))
