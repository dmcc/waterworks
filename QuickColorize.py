"""QuickColorize: provides a quick way to randomly colorize text.
By calling colorize() on text, it will randomly assign a color for that
text (which will be reused on subsequent calls to colorize()."""

# TODO use bg colors
import ansi, itertools
all_colors = [name for name in dir(ansi) if name[0].isupper()]
fg_colors = [name for name in all_colors if not name.endswith('BG')]
bg_colors = [name for name in all_colors if name.endswith('BG')]

for name in 'BLACK BOLD REVERSE RESET'.split():
    fg_colors.remove(name)

fg_color_cycler = itertools.cycle(fg_colors)
colors_defined = {}
def colorize(text):
    color = colors_defined.get(text)
    if not color:
        name = fg_color_cycler.next()
        color = getattr(ansi, name)
        colors_defined[text] = color
    return color + text + ansi.RESET
