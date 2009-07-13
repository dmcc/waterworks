import os, sys
from distutils.core import setup

if len(sys.argv) < 2:
    sys.argv.append("build")

setup(name = "waterworks",
      version = "0.2",
      maintainer = "David McClosky",
      maintainer_email = "dmcc+py (at) cs.brown.edu",
      description = "David McClosky's utility library",
      packages = ['cookbook', 'waterworks'],
      py_modules = ['AIMA', 'ExitCodes', 'FigUtil', 'Histogram', 'IntRange', 
                    'IntShelve', 'LazyList', 'Selectron', 'Tailer', 'TeXTable', 
                    'ThreadedJobs', 'TkGeomSavers', 'diffprint', 
                    'iterextras', 'ClusterMetrics', 'FunctionPickler', 
                    'HeapQueue', 'PrecRec', 'Probably', 'robust_apply', 
                    'TerminalTitle', 'vimdiff'],
      url='http://cs.brown.edu/~dmcc/software/',
)
