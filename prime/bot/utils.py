def strip(message):
    def from_iterable(iterable):
        for val in iterable:
            yield val.strip()
    if isinstance(message, (str, bytes)):
        return message.strip()
    elif hasattr(message, '__iter__'):
        return from_iterable(message)

def splitlines(message, max_lines=30):
    chunk = ''
    line_counter = 0
    for line in message.splitlines(True):
        if not line_counter % max_lines or not line.strip():
            yield chunk.strip()
            chunk = ''
            line_counter = 0
        chunk += line
        line_counter += 1
    else:
        yield chunk.strip()

def code_block(message):
    blockify = lambda m: '```{0}```'.format(m)

    def from_iterable(iterable):
        for val in iterable:
            if val:
                yield blockify(val)

    if isinstance(message, (str, bytes)):
        if message:
            return blockify(message)
    elif hasattr(message, '__iter__'):
        return from_iterable(message)


