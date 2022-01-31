def filter_comments(source):
    buffer = []
    comment_depth = 0
    for ch in source:
        if ch == "[":
            comment_depth += 1
        elif ch == "]":
            assert comment_depth > 0
            comment_depth -= 1
        else:
            if comment_depth == 0:
                buffer.append(ch)
    return "".join(buffer)


def tokenize(source: str):
    "it just works, dude"
    word_buffer = []
    tokens = []

    def add_word():
        nonlocal word_buffer
        if word_buffer:
            tokens.append("".join(word_buffer))
            word_buffer = []

    for ch in source:
        if ch in "'()":
            add_word()
            tokens.append(ch)
        elif ch in " \n":
            add_word()
        else:
            word_buffer.append(ch)
    add_word()
    return tokens


def is_word(tokens):
    return tokens[-1] not in "'()"


def is_quote(tokens):
    return tokens[-1] == "'"


def is_list(tokens):
    return tokens[-1] == "("


def is_list_end(tokens):
    return tokens[-1] == ")"


def read(tokens):
    """
    LL(1) recursive descent parser.
    Uses reverse token order for efficiency (pop() vs pop(0))
    """
    if not tokens:
        return
    if is_word(tokens):
        return ("word", tokens.pop())
    elif is_quote(tokens):
        tokens.pop()
        v = read(tokens)
        assert v is not None
        return ("quote", v)
    elif is_list(tokens):
        tokens.pop()
        values = []
        while not is_list_end(tokens):
            v = read(tokens)
            assert v is not None  # close your parens, dude
            values.append(v)
        tokens.pop()
        return ("list", values)
    assert not is_list_end(tokens)  # don’t close before opening, dude
    # wait, what happened, dude ?
    raise SyntaxError("check your facts, dude")


def read_all(tokens):
    tokens = tokens[::-1]
    values = []
    while (v := read(tokens)) is not None:
        values.append(v)
    return values


def parse(source: str):
    return read_all(tokenize(filter_comments(source)))


source = "(head [cons(a, b) - a] 0 extract) define"
print(parse(source))
