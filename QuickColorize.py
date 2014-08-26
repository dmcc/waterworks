#!/usr/bin/env python

"""QuickColorize: provides a quick way to randomly colorize text.
By calling colorize() on text, it will randomly assign a color for
that text (which will be reused on subsequent calls to colorize().
Also includes a command-line mode."""

import ansi, itertools, random
def make_cycler():
    all_colors = [name for name in dir(ansi) if name[0].isupper()]
    fg_colors = sorted([name for name in all_colors if not name.endswith('BG')])
    bg_colors = sorted([name for name in all_colors if name.endswith('BG')])

    for name in 'BLACK BOLD REVERSE RESET'.split():
        fg_colors.remove(name)

    # put black first
    bg_colors.remove('BLACKBG')
    bg_colors.insert(0, 'BLACKBG')

    color_pairs = []
    nonblackbg_color_pairs = []
    for bg_color in bg_colors:
        for fg_color in fg_colors:
            if bg_color.startswith(fg_color):
                continue
            if bg_color == 'BLACKBG' and fg_color == 'WHITE':
                continue

            if bg_color == 'BLACKBG':
                color_pairs.append((fg_color, bg_color))
            else:
                nonblackbg_color_pairs.append((fg_color, bg_color))

    rng = random.Random(0)
    rng.shuffle(nonblackbg_color_pairs)
    color_pairs += nonblackbg_color_pairs
    _color_cycler = itertools.cycle(color_pairs)
    return _color_cycler

_color_cycler = make_cycler()
_colors_defined = {}
def colorize(text):
    """Returns a colorized version of text.  The same text values will
    be consistently colorized."""
    text = str(text)
    colors = _colors_defined.get(text)
    if not colors:
        names = _color_cycler.next()
        colors = [getattr(ansi, name) for name in names]
        _colors_defined[text] = colors
    return ''.join(colors) + text + ansi.RESET

def assign_color(text, colors):
    _colors_defined[text] = colors

if __name__ == "__main__":
    import math
    for digit in str(math.pi):
        print colorize(digit)
    print
    for digit in str(math.e):
        print colorize(digit)
