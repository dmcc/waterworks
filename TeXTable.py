"""Convert a Python table into a LaTeX/TeX table."""
def texify(table, compact=1, has_header=False):
    """compact is a value from 0 to 2 which controls how much whitespace
    we output.  It does not change the display of the table."""
    s = []
    xdim = len(table[0])

    if compact == 0:
        compact1 = compact2 = '\n'
    elif compact == 1:
        compact1 = '\n'
        compact2 = ''
    else:
        compact1 = ' '
        compact2 = ''

    s.append(r"\begin{tabular}{" + 'c'.join((["|"] * (xdim + 1))) + "}\n")
    s.append(r"\hline" + "\n")
    for count, row in enumerate(table):
        s.append(' & '.join([str(x) for x in row]) + compact1)
        if has_header and count == 0:
            s.append(r"\\ \hline\hline" + "\n" + compact2)
        else:
            s.append(r"\\ \hline" + "\n" + compact2)
    s.append(r"\end{tabular}")

    return ''.join(s)

if __name__ == "__main__":
    print texify([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
