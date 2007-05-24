import heapq

class HeapQueue:
    """A more object-oriented way of doing a heapq"""
    def __init__(self, l=None):
        self._heap = l or []
        heapq.heapify(self._heap)
    def __len__(self):
        return len(self._heap)
    def __iter__(self):
        """You can only get the contents as an iterable so that they
        will be read only."""
        return iter(self._heap)
    def __contains__(self, item):
        return item in self._heap
    def peek(self):
        return self._heap[0]
    def pop(self):
        return heapq.heappop(self._heap)
    def add(self, item):
        return heapq.heappush(self._heap, item)
