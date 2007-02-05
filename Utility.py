"""(DEPRECATED) This file contains many potentially helpful functions.
Originally, all functions lived in Utility, but for organizational and
faster-importing purposes, it has mostly been split into many smaller
files. (waterworks.*)"""

from __future__ import nested_scopes
import os, sys

# TODO remove this when people update their references
from IntShelve import IntShelve

from waterworks.Dictionaries import *
from waterworks.Files import *
from waterworks.Sequences import *
from waterworks.Strings import *
from waterworks.Tools import *

###################
# unfiled for now #
###################

def bettersystem(command, stdout=None, stderr=None):
    """Not quite finished, sadly."""
    import select
    from popen2 import Popen3
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    p = Popen3(command, capturestderr=True)
    p_out, p_err = p.fromchild, p.childerr
    fd_out = p_out.fileno()
    fd_err = p_err.fileno()

    while 1:
        if p.poll() != -1:
            break

        rlist, _, _ = select.select([p_out, p_err], [], [])
        if not rlist:
            break

        if p_out in rlist:
            output = os.read(fd_out, 1024)
            if output == '':
                p.wait()
            else:
                stdout.write(output)
                stdout.flush()
        if p_err in rlist:
            output = os.read(fd_err, 1024)
            if output == '':
                p.wait()
            else:
                stderr.write(output)
                stderr.flush()

    return p.wait()

################
# testing code #
################

def test_find_indices_of_unique_items():
    x = [101, 102, 103, 101, 104, 106, 107, 102, 108, 109]
    print list(enumerate(x))
    print find_indices_of_unique_items(x)

if __name__ == "__main__":
    test_find_indices_of_unique_items()
