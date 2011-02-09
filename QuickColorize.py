"""QuickColorize: provides a quick way to randomly colorize text.
By calling colorize() on text, it will randomly assign a color for that
text (which will be reused on subsequent calls to colorize()."""

# TODO use bg colors
import ansi, itertools
all_colors = [name for name in dir(ansi) if name[0].isupper()]
fg_colors = sorted([name for name in all_colors if not name.endswith('BG')])
bg_colors = sorted([name for name in all_colors if name.endswith('BG')])

for name in 'BLACK BOLD REVERSE RESET'.split():
    fg_colors.remove(name)

# put black first
bg_colors.remove('BLACKBG')
bg_colors.insert(0, 'BLACKBG')

color_pairs = []
for bg_color in bg_colors:
    for fg_color in fg_colors:
        if bg_color.startswith(fg_color):
            continue
        if bg_color == 'BLACKBG' and fg_color == 'WHITE':
            continue

        color_pairs.append((fg_color, bg_color))

color_cycler = itertools.cycle(color_pairs)
colors_defined = {}
def colorize(text):
    color = colors_defined.get(text)
    if not color:
        names = color_cycler.next()
        colors = [getattr(ansi, name) for name in names]
        colors_defined[text] = color
    return ''.join(colors) + text + ansi.RESET
