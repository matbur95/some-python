from flip_flops import JK

f = '{:0>3b}'

hline = r'\hline'
end_tabular = r'\end{tabular}'


def begin_tabular(n):
    """ Function returns opening tag for table with width n.

    :param n: number of column in table
    :return: string which starts table
    """
    return r'\begin{tabular}{|' + 'c|' * n + '}'


def subscript(big, small):
    """ Function returns proper syntax for subscript.

    :param big: value which should be up and big
    :param small: value which should be down and small
    :return: string
    """
    return '${}_{{{}}}$'.format(big, small)


def multicolumn(n, value):
    """ Function merges n columns and fills it with value

    :param n: number of merged columns
    :param value: text in merged columns
    :return: string
    """
    return r'\multicolumn{{{}}}{{|c|}}{{{}}}'.format(n, value)


def gen_row(row):
    """ Function transforms list of items to one row from Latex

    :param row: list of items
    :return: string, merged row
    """
    row = map(str, row)
    return ' & '.join(row) + r' \\'


def gen_tabular(rows, sep=' '):
    """ Function combines all parts of table.

    :param rows: list of rows
    :param sep: separator between rows
    :return: string, merged table
    """
    n = max(len(row) for row in rows)
    s = [begin_tabular(n)]

    for row in rows:
        s.append(gen_row(row))

    s.append(end_tabular)
    # sep = '\n'
    return '{0}{1}{0}'.format(sep, hline).join(s)


def gen_moves(moves):
    n = len(moves[0])
    rows = (
        [multicolumn(n, '')],
        ['t', 't+1'],
        *moves
    )

    if n == 3:
        rows[1].insert(0, 'Z')

    return gen_tabular(rows)


def gen_bin_moves(moves):
    n = len(moves[0])
    rows = (
        [multicolumn(3, 't'), multicolumn(3, 't+1')],
        [subscript('Q', i) for i in '210'] * 2,
        *[(*z, *f.format(t), *f.format(u)) for *z, t, u in moves]
    )

    if n == 3:
        rows[0].insert(0, '')
        rows[1].insert(0, 'Z')

    return gen_tabular(rows)


def gen_flip_flops(moves):
    rows = [
        [multicolumn(6, 'Przerzutniki')],
        [subscript(i, j) for j in '210' for i in 'JK']
    ]

    for *_, t, u in moves:
        t2, t1, t0 = f.format(t)
        u2, u1, u0 = f.format(u)
        rows.append((*JK(t2, u2), *JK(t1, u1), *JK(t0, u0),))

    return gen_tabular(rows)


if __name__ == '__main__':
    # moves = [(i, (i + 1) % 8) for i in range(8)]
    series = [int(i) for i in '0123654']
    moves = [(v, series[(i + 1) % len(series)]) for i, v in enumerate(series)]

    moves3 = [
        (0, 0, 1),
        (0, 1, 2),
        (0, 2, 3),
        (0, 3, 6),
        (0, 4, 0),
        (0, 5, 4),
        (0, 6, 5),

        (1, 0, 4),
        (1, 1, 0),
        (1, 2, 1),
        (1, 3, 2),
        (1, 4, 5),
        (1, 5, 6),
        (1, 6, 3),
    ]

    print(gen_moves(moves))
    print(gen_bin_moves(moves))
    print(gen_flip_flops(moves))
