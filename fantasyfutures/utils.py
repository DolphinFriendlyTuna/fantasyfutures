from collections import defaultdict


class SortedDefaultDict(defaultdict):

    def __init__(self, *args, **kwargs):
        self.key_order = []
        self.reverse = kwargs.pop('reverse', False)
        super(SortedDefaultDict, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if key not in self.key_order:
            self.key_order.append(key)
            self.key_order.sort(reverse=self.reverse)

        super(SortedDefaultDict, self).__setitem__(key, value)

    def __delitem__(self, key):
        super(SortedDefaultDict, self).__delitem__(key)
        self.key_order.remove(key)

    def keys(self):
        return self.key_order

    def items(self):
        for key in self.key_order:
            yield key, self[key]
