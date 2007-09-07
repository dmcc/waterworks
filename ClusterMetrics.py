"""ClusterMetrics: a metric ****** of cluster metrics!"""
from __future__ import division
from Probably import variation_of_information as vi, \
    mutual_information as mi, log2
from waterworks.Tools import ondemand
from AIMA import DefaultDict

class ConfusionMatrix:
    def __init__(self):
        # test : { gold : count }
        self.by_test = DefaultDict(DefaultDict(0))
    def add(self, gold, test, count=1):
        self.by_test[test][gold] += count
    def as_confusion_items(self):
        for test, gold_dict in self.by_test.items():
            for gold, count in gold_dict.items():
                yield (gold, test), count
    def one_to_one_greedy_mapping(self):
        """Computes the one-to-one greedy mapping.  The mapping returned
        is a dictionary of {test : gold}"""
        one_to_one_mapping = {} # test : gold
        confusion_by_count = sorted((-count, (gold, test))
            for (gold, test), count in self.as_confusion_items())

        for count, (gold, test) in confusion_by_count:
            if test in one_to_one_mapping.keys() or \
               gold in one_to_one_mapping.values():
                continue
            else:
                one_to_one_mapping[test] = gold
        return one_to_one_mapping
    def one_to_one_greedy(self):
        """Computes and evaluates the one-to-one greedy mapping.
        Returns a score between 0.0 and 1.0 (higher is better)."""
        return self.eval_mapping(self.one_to_one_greedy_mapping())
    def one_to_one_optimal_mapping(self):
        """Computes the one-to-one optimal mapping using the Hungarian 
        algorithm.  The mapping returned is a dictionary of {test : gold}"""
        import pyung
        all_gold = set()
        for (gold, test), count in self.as_confusion_items():
            all_gold.add(gold)
        all_gold = sorted(list(all_gold))
        neg_confusion_array = []
        all_test = []
        for test, gold_counts in self.by_test.items():
            counts = [-gold_counts.get(gold, 0) for gold in all_gold]
            neg_confusion_array.append(counts)
            all_test.append(test)

        for x in range(len(all_gold) - len(all_test)):
            neg_confusion_array.append([0] * len(all_gold))

        mapping = pyung.hungarian_method(neg_confusion_array)
        mapping_dict = {}
        for test_index, gold_index in mapping:
            try:
                test = all_test[test_index]
            except IndexError:
                continue
            mapping_dict[test] = all_gold[gold_index]
        return mapping_dict
    def one_to_one_optimal(self):
        """Computes and evaluates the one-to-one optimal mapping.
        Returns a score between 0.0 and 1.0 (higher is better)."""
        return self.eval_mapping(self.one_to_one_optimal_mapping())
    def many_to_one_mapping(self):
        """Computes the many-to-one mapping.  The mapping returned is
        a dictionary of {test : gold}"""
        many_to_one_mapping = {} # test tag : gold tag
        for test, gold_counts in self.by_test.items():
            by_count = ((v, k) for k, v in gold_counts.items())
            top_count, top = max(by_count)
            many_to_one_mapping[test] = top
        return many_to_one_mapping
    def many_to_one(self):
        """Computes and evaluates the many-to-one mapping.  Returns a
        score between 0.0 and 1.0 (higher is better)."""
        return self.eval_mapping(self.many_to_one_mapping())
    def eval_mapping(self, mapping, verbose=True):
        """Evaluates a mapping (dictionary of assignments between test and
        gold).  Returns a score between 0.0 and 1.0 (higher is better).
        
        If verbose is true, the mapping will be printed before being
        evaluated."""
        if verbose:
            print "Mapping", mapping
        right = 0
        wrong = 0
        for (gold, test), count in self.as_confusion_items():
            if mapping.get(test) == gold:
                right += count
            else:
                wrong += count
        return right, wrong, right / (right + wrong)
    def variation_of_information(self):
        """Calculates the variation of information between the test and gold.  
        Lower is better, minimum is 0.0"""
        return vi(dict(self.as_confusion_items()))
    def mutual_information(self):
        """Calculates the mutual information between the test and gold.  
        Higher is better, minimum is 0.0"""
        return mi(dict(self.as_confusion_items()))

if __name__ == "__main__":
    cm = ConfusionMatrix()
    cm.add('B', 1, 0)
    cm.add('A', 1, 9)
    cm.add('B', 2, 9)
    cm.add('A', 2, 10)
    print cm.one_to_one_greedy()
    print cm.eval_mapping(cm.many_to_one_mapping())
    print cm.variation_of_information()
    print cm.mutual_information()
    print cm.one_to_one_optimal_mapping()
    print cm.one_to_one_optimal()
