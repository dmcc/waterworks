###########################
# dictionary manipulation #
###########################

class CounterDict(dict):
    """Simple subclass of a dictionary to help count items:
    
    >>> c = CounterDict()
    >>> c.count('a', 'sequence', 'of', 'things', 'to', 'count')
    >>> c
    {'a': 1, 'count': 1, 'sequence': 1, 'of': 1, 'to': 1, 'things': 1}
    >>> c.count('more', 'things')
    >>> c
    {'a': 1, 'count': 1, 'sequence': 1, 'of': 1, 'to': 1, 'things': 2, 'more': 1}
    >>> c.count('justonething')
    >>> c
    {'a': 1, 'count': 1, 'sequence': 1, 'of': 1, 'to': 1, 'justonething': 1, 'things': 2, 'more': 1}
    """
    def count(self, *keys):
        "Count each item in the sequence 'keys' (which could be a single item)"
        for key in keys:
            self.setdefault(key, 0)
            self[key] += 1

def dictadd(d1, d2):
    """Add the numeric values of values in two dictionaries together in
    a functional fashion (d1 and d2 are not modified)."""
    # we're going to clone d1, so we'll reverse our arguments if d2 is the
    # smaller one
    if len(d2) < len(d1):
        d1, d2 = d2, d1
    d1 = dict(d1) # clone d1
    return dictiadd(d1, d2)

def dictiadd(d1, d2):
    """Add the numeric values of values in two dictionaries together,
    modifying the first argument in place. (Called iadd to be like
    Python's __iadd__ which is the method that does incremental
    addition)."""
    for k, v in d2.items():
        d1.setdefault(k, 0)
        d1[k] += v
    return d1

def countdict_to_pairs(counts, limit=None):
    """Convert a dictionary from { anything : counts } to a list of at
    most 'limit' pairs (or all if limit is None), sorted from highest
    count to lowest count."""
    pairs = [(count, x) for (x, count) in counts.items() if count]
    pairs.sort()
    pairs.reverse() # sort from high to low
    if limit is not None:
        pairs = pairs[:limit]

    return pairs

def dict_subset(d, dkeys, default=0):
    """Subset of dictionary d: only the keys in dkeys.  If you plan on omitting
    keys, make sure you like the default."""
    newd = {} # dirty variables!
    for k in dkeys:
        newd[k] = d.get(k, default)
    return newd
