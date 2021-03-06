"""PrecRec: standard calculation of precision, recall and f-score."""

def precision_recall(n_matched, n_gold, n_proposed):
    """Calculates the classification precision and recall, given
    the number of true positives, the number of existing positives,
    and the number of proposed positives."""

    if n_gold > 0:
        recall = n_matched / n_gold
    else:
        recall = 0.0

    if n_proposed > 0:
        precision = n_matched / n_proposed
    else:
        precision = 0.0

    return precision, recall

def precision_recall_posneg(tp=0, fp=0, fn=0):
    """Calculates the classification precision and recall, given
    true positives, false positives, and false negatives."""
    prec_denom = tp + fp
    if prec_denom == 0:
        precision = 0
    else:
        precision = tp / prec_denom

    recall_denom = tp + fn
    if recall_denom == 0:
        recall = 0
    else:
        recall = tp / recall_denom

    return precision, recall

def fscore(precision, recall, beta=1.0):
    """Calculates the f-score (default is balanced f-score; beta > 1
    favors precision), the harmonic mean of precision and recall."""

    num = (beta ** 2 + 1) * precision * recall
    denom = (beta ** 2) * precision + recall
    if denom == 0:
        return 0.0
    else:
        return num / denom

def precision_recall_f(n_matched, n_gold, n_proposed, beta=1.0):
    """Calculates precision, recall and f-score."""

    prec, rec = precision_recall(n_matched, n_gold, n_proposed)
    f = fscore(prec, rec, beta=beta)

    return prec, rec, f

def precision_recall_f_posneg(tp=0, fp=0, fn=0, beta=1.0):
    """Calculates precision, recall and f-score from true/false negatives."""

    prec, rec = precision_recall_posneg(tp, fp, fn)
    f = fscore(prec, rec, beta=beta)

    return prec, rec, f

def fscore_from_components(n_matched, n_gold, n_proposed, beta=1.0):
    """Calculates f-score from the number of matched, gold, and proposed
    items instead of precision and recall.  See fscore()."""
    return precision_recall_f(n_matched, n_gold, n_proposed, beta=beta)[2]

def fscore_from_components_posneg(tp=0, fp=0, fn=0, beta=1.0):
    """Calculates f-score from true/false positives and false negaties
    items instead of precision and recall.  See fscore()."""
    return precision_recall_f_posneg(tp, fp, fn, beta=beta)[2]

if __name__ == "__main__":
    print(precision_recall(1, 10, 1))
    print(precision_recall(10, 10, 20))
    print(precision_recall(10, 10, 10))

    print(fscore(1, 1))
    print(fscore(0, 0))
    print(fscore(.5, .5))
    print(fscore(.5, .7))
    print(fscore(.7, .5))
