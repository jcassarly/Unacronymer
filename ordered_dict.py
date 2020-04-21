class OrderedDict(list):
    """A dictionary that has an order associated with it and is iterable over that order"""

    def __init__(self):
        self.keys = []
        self.dict = {}

    def __iter__(self):
        """An iterator the walks over the dictionary in order

        :yields: a key, value pair that is next in the dictionary
        """
        for acronym in self.keys:
            yield acronym, self.dict[acronym]

    def __contains__(self, key):
        """Checks whether the key is in the dictionary

        :param key: the key to check if it is in the dictionary
        :returns: True if the key is in the dictionary, false otherwise

        """
        return key in self.keys

    def add(self, key, value):
        """Adds the key, value pair to the end of the dictionary if not already there

        :param key: the key to the dictionary
        :param value: the value of the key in the dictionary

        """
        if not key in self:
            self.keys.append(key)
            self.dict[key] = value

class AcronymDict(OrderedDict):
    """An ordered dictionary for acronyms and their definitions"""

    def sort(self):
        """Sorts the dictionary by reverse alphabetical order (longer acronyms with the same start come first)"""
        self.keys = sorted(self.keys)
        self.keys.reverse()
