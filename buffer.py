class Buffer():
    """Cyclic Queue to buffer data"""

    SIZE = 256

    def __init__(self):
        self.__buffer = []

    def add(self, new_item):
        """Adds the item to the buffer and pops the last element in the buffer out if at max size

        :param new_item: the item to add to the from of the buffer

        """
        if len(self.__buffer) >= self.SIZE:
            self.__buffer.pop(0)

        self.__buffer.append(new_item)

    def get(self, index):
        """Gets the item ar the specified index

        :param int index: the index to get the item in the buffer at

        """
        return self.__buffer[index]

    def is_index_from_end_in_bounds(self, index_from_end):
        """Checks if the index from the from of the buffer is in bounds

        :param int index_from_end: the index from the front of the buffer to check

        """
        converted_index = len(self.__buffer) - 1 - index_from_end
        return (converted_index >= 0 and converted_index < self.SIZE)

    def get_from_end(self, index_from_end):
        """Gets the item from the front of the buffer back index_from_end indices

        :param int index_from_end: the idnex from the front of the buffer to get an item from

        """
        return self.__buffer[len(self.__buffer) - 1 - index_from_end]

    def newest(self):
        """Gets the item from the front of the buffer"""
        return self.__buffer[len(self.__buffer) - 1]
