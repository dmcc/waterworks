import heapq

class HeapQueue:
    """A more object-oriented way of doing a heapq"""
    def __init__(self, initial_list=None):
        """Create a heap queue, optionally from an initial list."""
        self._heap = initial_list or []
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
        """Look at the top element."""
        return self._heap[0]
    def pop(self):
        """Removes and returns the top element."""
        return heapq.heappop(self._heap)
    def add(self, item):
        """Add an item into the heap."""
        return heapq.heappush(self._heap, item)
