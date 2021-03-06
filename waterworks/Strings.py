"""Collection of functions and classes for working on strings."""

import re
pretty_time_parsing_regex = re.compile(r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?')

def try_parse_int(val, default=None):
    """Attempt to parse a string as an integer.  If parsing fails,
    the default will be returned."""
    try:
        return int(val)
    except ValueError:
        return default

def try_parse_float(val, default=None):
    """Attempt to parse a string as an integer.  If parsing fails,
    we try again as a float.  If parsing fails again, the default will
    be returned."""
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return default

def try_parse_date(val, default=None):
    """Attempt to parse a string as an date.  If parsing fails in
    recoverable way, as much information about the date as possible will
    be returned.  If the input is not parsable at all, the default will
    be returned."""
    import mx.DateTime
    try:
        return mx.DateTime.Parser.DateTimeFromString(val)
    except:
        return default

# by George Sakkis (gsakkis at rutgers.edu)
# http://mail.python.org/pipermail/python-list/2005-March/312004.html
def parseSexpression(expression):
    subexpressions,stack = [],[]
    for token in re.split(r'([()])|\s+', expression):
        if token == '(':
            new = []
            if stack:
                stack[-1].append(new)
            else:
                subexpressions.append(new)
            stack.append(new)
        elif token == ')':
            try: stack.pop()
            except IndexError:
                raise ValueError("Unbalanced right parenthesis: %s" % \
                    expression)
        elif token:
            try: stack[-1].append(token)
            except IndexError:
                raise ValueError("Unenclosed subexpression (near %s)" % token)
    if stack:
        raise ValueError("Unbalanced left parenthesis: %s" % expression)
    if len(subexpressions) > 1:
        raise ValueError("Single s-expression expected (%d given)" % \
            len(subexpressions))
    return subexpressions[0]

def multisplit(string_to_split, delimiters):
    """Example:

    >>> print(multisplit('hello there, how are you?', delimiters=','))
    ['hello there', ' how are you?']
    >>> print(multisplit('hello there, how are you?', delimiters=', '))
    ['hello', 'there', 'how', 'are', 'you?']
    """
    import re
    splitter_re = re.compile('|'.join(["(?:%s)" % delimiter 
        for delimiter in delimiters]))
    splitted = splitter_re.split(string_to_split)
    return [splittee for splittee in splitted 
        if splittee and splittee not in delimiters]

def zfill_by_num(x, num_to_fill_to):
    """zfill with an example, i.e. give it a number of the length (string
    length) you want it to fill to.

    >>> zfill_by_num(1, 102)
    '001'
    """
    l = len(str(num_to_fill_to))
    return str(x).zfill(l)

def pretty_time_range(diff, show_seconds=True):
    """Given a number of seconds, returns a string attempting to represent
    it as shortly as possible.  Only handles seconds in integers.
    
    >>> pretty_time_range(1)
    '1s'
    >>> pretty_time_range(10)
    '10s'
    >>> pretty_time_range(100)
    '1m40s'
    >>> pretty_time_range(1000)
    '16m40s'
    >>> pretty_time_range(10000)
    '2h46m40s'
    >>> pretty_time_range(100000)
    '1d3h46m40s'
    """
    diff = int(diff)
    days, diff = divmod(diff, 86400)
    hours, diff = divmod(diff, 3600)
    minutes, seconds = divmod(diff, 60)
    str = ''
    if days: 
        str += '%sd' % days
    if hours: 
        str += '%sh' % hours
    if minutes: 
        str += '%sm' % minutes
    if show_seconds and seconds: 
        str += '%ss' % seconds
    if not str:
        if show_seconds: str = '%ss' % seconds
        else: str = '0m'
    return str

def parse_pretty_time_range(text):
    """Given a pretty time range from pretty_time_range() (e.g. "7s", "35m", "2d12h5s"),
    returns the number of seconds.
    
    >>> parse_pretty_time_range('1s')
    1
    >>> parse_pretty_time_range('10s')
    10
    >>> parse_pretty_time_range('1m40s')
    100
    >>> parse_pretty_time_range('16m40s')
    1000
    >>> parse_pretty_time_range('2h46m40s')
    10000
    >>> parse_pretty_time_range('1d3h46m40s')
    100000
    """
    match = pretty_time_parsing_regex.match(text)
    total_seconds = 0
    if match:
        days, hours, minutes, seconds = match.groups()
        if days:
            total_seconds += int(days) * 86400
        if hours:
            total_seconds += int(hours) * 3600
        if minutes:
            total_seconds += int(minutes) * 60
        if seconds:
            total_seconds += int(seconds)
        return total_seconds
    else:
        raise ValueError("Couldn't parse %r" % text)

def sumstring(s):
    """Sum up a string containing only numbers. Whitespace is ignored but this function is not otherwise very robust."""
    return sum(map(float, s.split()))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
