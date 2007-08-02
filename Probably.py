"""Potentially useful functions for probability, statistics, and machine
learning."""
from __future__ import division

import math
from random import uniform, random

def log2(x):
    """Returns log base 2 of a number."""
    return math.log(x, 2)

def xlog2x(x):
    """Returns x*log2(x) handling the case where x is 0 correctly."""
    if x == 0:
        return 0
    else:
        return x * log2(x)

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

def entropy_of_multinomal(count_seq):
    # TODO document
    total = sum(count_seq)
    entropy = 0
    for i in count_seq:
        prob_i = i / total
        entropy -= xlog2x(prob_i)
    return entropy

def variation_of_information(confusion_dict):
    """VI(X, Y) = H(X) + H(Y) - 2I(X; Y)
                = H(X) + H(Y) - 2[H(X) + H(Y) - H(X, Y)]
                = 2H(X, Y) - H(X) - H(Y)"""
    # TODO document better
    from AIMA import DefaultDict
    count_x = DefaultDict(0)
    count_y = DefaultDict(0)
    for (x_key, y_key), count in confusion_dict.items():
        count_x[x_key] += count
        count_y[y_key] += count

    return (2 * entropy_of_multinomal(confusion_dict.values())) - \
           entropy_of_multinomal(count_x.values()) - \
           entropy_of_multinomal(count_y.values())

def mutual_information(confusion_dict):
    """I(X; Y) = H(X) + H(Y) - H(X, Y)"""
    # TODO document
    from AIMA import DefaultDict
    count_x = DefaultDict(0)
    count_y = DefaultDict(0)
    for (x_key, y_key), count in confusion_dict.items():
        count_x[x_key] += count
        count_y[y_key] += count
    return entropy_of_multinomal(count_x.values()) + \
           entropy_of_multinomal(count_y.values()) - \
           entropy_of_multinomal(confusion_dict.values())

def sample_multinomial(probs):
    """Gives a random sample from the unnormalized multinomial distribution
    probs, returned as the index of the sampled element."""
    norm = sum(probs)

    rn = random()
    tot = 0.0
    for ctr, pr in enumerate(probs):
        tot += pr / norm
        if rn < tot:
            return ctr
    raise("Failed to sample from "+str(probs)+
          ", sample was "+str(rn)+" norm was "+str(norm))

def sample_log_multinomial(probs):
    """Gives a random sample from the unnormalized multinomial distribution
    whose natural logarithm is probs, returned as the index of the sampled
    element."""

    maxElt = max(probs)
    expProbs = [math.exp(p - maxElt) for p in probs]
    return sample_multinomial(expProbs)

if __name__ == "__main__":
    dist = [1, 3, 5]
    print "Sampling from distribution:", dist

    hist = {1:0, 3:0, 5:0}
    samples = 5000
    for x in range(samples):
        hist[dist[sample_multinomial(dist)]] += 1

    normdist = sum(dist)
    for d in dist:
        print "True frequency:", d/normdist, \
              "sampled frequency", hist[d]/samples

    dist = [.8, .2, .5]
    logdist = [math.log(x) for x in dist]
    print "Sampling from logarithmic distribution:", logdist
    hist = dict([(x,0) for x in dist])
    samples = 5000
    for x in range(samples):
        hist[dist[sample_multinomial(dist)]] += 1

    normdist = sum(dist)
    for d in dist:
        print "True frequency:", d/normdist, \
              "sampled frequency", hist[d]/samples
        
