"""Potentially useful functions for probability, statistics, and machine
learning."""
from __future__ import division

import math
from random import uniform, random
def jittered_probs(count, max_jitter=1e-10):
    """Return count jittered probabilities.  This is useful for randomly
    initializing a multinomial over count items when you want the
    probabilities to be almost uniform but a little noise to break ties.
    max_jitter is the maximum (unnormalized) jitter each probability
    can have."""
    weights = [1 + uniform(-max_jitter, max_jitter) for x in range(count)]
    weights_sum = sum(weights)
    return [weight / weights_sum for weight in weights]

def sample_simplex(n):
    """Sample probabilities from an n-simplex uniformly at random.  This,
    like jittered_probs is useful for initializing a multinomial over n
    items, except that the probabilities will be totally random instead
    of more or less uniform."""
    parts = [-math.log(1 - random()) for x in range(n)]
    s = sum(parts)
    return [part / s for part in parts]
