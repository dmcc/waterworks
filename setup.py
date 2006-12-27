import os, sys
from distutils.core import setup

if len(sys.argv) < 2:
    sys.argv.append("build")

setup(name = "waterworks",
      version = "0.1e",
      maintainer = "David McClosky",
      maintainer_email = "dmcc+py (at) cs.brown.edu",
      description = "David McClosky's utility library",
      packages = ['cookbook', 'waterworks'],
      py_modules = ['AIMA', 'ExitCodes', 'FigUtil', 'Histogram', 'IntRange', 
                    'IntShelve', 'LazyList', 'Selectron', 'Tailer', 'TeXTable', 
                    'ThreadedJobs', 'TkGeomSavers', 'Utility', 'diffprint', 
                    'iterextras'],
      url='http://cs.brown.edu/~dmcc/software/',
)
