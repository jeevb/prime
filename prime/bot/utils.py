from itertools import chain, zip_longest

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
    blockify = lambda m: '```\n{0}\n```'.format(m)

    def from_iterable(iterable):
        for val in iterable:
            if val:
                yield blockify(val)

    if isinstance(message, (str, bytes)):
        if message:
            return blockify(message)
    elif hasattr(message, '__iter__'):
        return from_iterable(message)

class PrettyList(list):
    def columnify(self, cols, sep='\t', fillvalue=''):
        # Map list to strings
        str_list = list(map(str, self))

        # Split list into columns
        split_list = []
        col_widths = []
        rows, r = divmod(len(str_list), cols)
        rows += (r != 0)
        for i in range(rows):
            split_list.append(str_list[i::rows])
        for j in range(0, len(str_list), rows):
            col_widths.append(max(len(elem) for elem in str_list[j:j+rows]))

        # Print to pretty format
        template = sep.join(['%-*s'] * cols)
        for sublist in split_list:
            yield template % (tuple(
                chain.from_iterable(
                    zip_longest(col_widths,
                                sublist,
                                fillvalue=fillvalue)
                )
            ))
