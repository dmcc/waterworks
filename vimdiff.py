"""Simple interface for visualizing differences between two strings using
vimdiff (configurable to use other differs too)"""

import tempfile
def vimdiff(*strings, **options):
    """Given a list of strings, visualizes the differences between them
    using vimdiff (or similar program). 
    The visualizer program is specified by the command_template keyword
    and the default is:

        vimdiff -gf %s

    where %s will be replaced with a list of filenames."""
    import sys
    assert len(strings) >= 2, "Must have at least two strings."
    file_objs = []
    for i, s in enumerate(strings):
        vim_tempfile = tempfile.NamedTemporaryFile(mode='w',
                                                   prefix='%d-' % i)
        vim_tempfile.write(s)
        vim_tempfile.flush()
        file_objs.append(vim_tempfile)

    filenames = [vim_tempfile.name for vim_tempfile in file_objs]
    command_template = options.get('command_template', 'vimdiff -gf %s')
    command = command_template % ' '.join(filenames)
    import os
    print("Running:", command)
    os.system(command)

def pprint_and_vimdiff(*objs, **options):
    """Takes objects instead of strings, run them through pprint first."""
    import pprint
    strings = [pprint.pformat(obj) for obj in objs]
    return vimdiff(*strings, **options)
