import sys

class ondemand(property):
    """A property that is loaded once from a function."""
    def __init__(self, fget, doc=None):
        property.__init__(self, fget=self.get, fdel=self.delete, doc=doc)
        self.loadfunc = fget
        import weakref
        self.values = weakref.WeakKeyDictionary()
    def get(self, obj):
        if obj not in self.values:
            self.load(obj)
        return self.values[obj]
    def load(self, obj):
        self.values[obj] = self.loadfunc(obj)
    def delete(self, obj):
        # XXX this may not be needed any more
        try:
            del self.values[obj]
        except:
            pass

def initialize(ob, args):
    """In __init__, call initialize(self, locals()) to load all passed 
    arguments."""
    if 'self' in args:
        del args['self']
    for k, v in args.items():
        setattr(ob, k, v)

def make_attributes_from_args(*argnames):
    """
    This function simulates the effect of running
      self.foo = foo
    for each of the given argument names ('foo' in the example just
    now). Now you can write:
        def __init__(self,foo,bar,baz):
            make_attributes_from_args('foo','bar','baz')
            ...
    instead of:
        def __init__(self,foo,bar,baz):
            self.foo = foo
            self.bar = bar
            self.baz = baz
            ... 
    """
    callerlocals = sys._getframe(1).f_locals
    callerself = callerlocals['self']
    for a in argnames:
        try:
            setattr(callerself,a,callerlocals[a])
        except KeyError:
            raise KeyError("Function has no argument '%s'" % a)

def make_dict_from_args(*argnames):
    """
    The sequel to the best selling make_attributes_from_args!  Turn your
    arguments into a dictionary.  Takes a list of the names of the arguements
    to convert, returns a dictionary with their names : values.

    def some_function(foo, bar, qux):
        d = make_dict_from_args('foo', 'bar', 'qux')

    d is now:
    { 'foo' : value_of_foo, 'bar' : value_of_bar, 'qux' : value_of_qux }
    """
    callerlocals=sys._getframe(1).f_locals
    d = {}
    for a in argnames:
        try:
            d[a] = callerlocals[a]
        except KeyError:
            raise KeyError("Function has no argument '%s'" % a)
    return d

def dumpobj(o, double_underscores=0):
    """Prints all the object's non-callable attributes.  If double_underscores
    is false, it will skip attributes that begin with double underscores."""
    print(repr(o))
    for a in [x for x in dir(o) if not callable(getattr(o, x))]:
        if not double_underscores and a.startswith("__"):
            continue
        try:
            print("  {:>20}: {} ".format(a, getattr(o, a)))
        except:
            pass
    print("")

_count = 0 # certainly not thread safe
def trace(func, stream=sys.stdout):
    """Good old fashioned Lisp-style tracing.  Example usage:
    
    >>> def f(a, b, c=3):
    >>>     print a, b, c
    >>>     return a + b
    >>>
    >>>
    >>> f = trace(f)
    >>> f(1, 2)
    |>> f called args: [1, 2]
    1 2 3
    <<| f returned 3
    3

    TODO: print out default keywords (maybe)"""
    name = func.__name__
    global _count
    def tracer(*args, **kw):
        global _count
        s = ('\t' * _count) + '|>> %s called with' % name
        _count += 1
        if args:
            s += ' args: %r' % list(args)
        if kw:
            s += ' kw: %r' % kw
        print(s, file=stream)
        ret = func(*args, **kw)
        _count -= 1
        print(('\t' * _count) + f'<<| {name} returned {ret}', file=stream)
        return ret
    return tracer

def get_current_traceback_tuple():
    """Returns a semiformatted traceback of the current exception as a tuple
    in this form:
       (exceptionclass, exceptioninstance, lines_of_string_traceback_lines)"""
    import traceback
    exceptionclass, exceptioninstance, tb = sys.exc_info()
    tb_lines = traceback.format_tb(tb)
    return (exceptionclass, exceptioninstance, tb_lines)

class Symbol:
    """Lisp symbols for Python (sort of).  These are like strings but
    used differently (think exception classes vs. string exceptions).
    Two symbols of the same name are equal but not equal to the string
    of their name, i.e. Symbol('x') == Symbol('x'), but Symbol('x') !=
    'x'."""
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return f"{self.__class__}({self.name!r})"
    def __eq__(self, other):
        try:
            return self.name == other.name
        except AttributeError:
            return False

def generic_repr(self):
    """Generic representation -- prints out the object's dictionary,
    ignoring keys that start with '_' and values that are non-false.
    Attribute names mentioned in the attribute _not_in_repr will also
    be ignored.  The attribute _show_false is a list containing things
    to show even if they are False.

    Example usage:
    class A:
        def __init__(self, *whatever):
            do_things()
        __repr__ = generic_repr
    """
    skip = getattr(self, '_not_in_repr', [])
    show_false = getattr(self, '_show_false', [])
    d = ', '.join('%s=%r' % item 
        for item in sorted(self.__dict__.items()) 
        if item[0] not in skip and not item[0].startswith('_') and \
           (item[1] or item[0] in show_false))
    name = str(self.__class__.__name__).replace('__main__.', '')
    return f"{name}({d})"

class SimpleKeyEquality:
    """Lets you define a _key() method which will be used for __eq__,
    __hash__, and __cmp__.  The _key() method should return a hashable
    key for the object e.g. a tuple of hashable objects."""
    def __eq__(self, other):
        try:
            other_key = other._key()
        except AttributeError:
            return False

        return self._key() == other_key
    def __hash__(self):
        return hash(self._key())
    def __cmp__(self, other):
        try:
            other_key = other._key()
        except AttributeError:
            return -1

        return cmp(self._key(), other_key)
    def _key(self):
        raise NotImplementedError("Must implement _key() method.")

def get_simple_logger(name):
    import logging

    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter("%(asctime)s %(name)-6s %(levelname)-5s %(message)s", datefmt='%Y-%m-%d %H:%M:%S')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    return logger

def import_maybe(module_name):
    "Import a module and return it if available, otherwise returns None."
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None

class DeprecatedGetter:
    """Used when a getter method has been converted to a property. All
    attributes will be dispatched to the property's value and a warning
    will be raised if this is called. This doesn't work if the property
    being deprecated has its own __call__ method, since that will be
    unreachable as a DeprecatedGetter."""
    def __init__(self, name, value):
        """name is the attribute name of the property. value is its
        value."""
        self.__name = name
        self.__value = value
    def __getattr__(self, attr):
        """All attributes except __call__ are dispatched to the property's
        value."""
        return getattr(self.__value, attr)
    def __call__(self, *args, **kwargs):
        """Shouldn't be called except by deprecated code. Issues a warning
        about the deprecation then returns the value so that deprecated
        code will continue to work."""
        from warnings import warn
        warn("%r is no longer a method. It's now a property." % self.__name,
             DeprecationWarning, stacklevel=2)
        return self.__value
