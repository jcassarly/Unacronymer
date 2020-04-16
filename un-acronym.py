class Buffer():

    SIZE = 255

    def __init__(self):
        self.__buffer = []

    def add(self, new_item):
        if len(self.__buffer) >= self.SIZE:
            self.__buffer.pop(0)

        self.__buffer.append(new_item)

    def get(self, index):
        return self.__buffer[index]

    def newest(self):
        return self.__buffer[len(self.__buffer) - 1]


class Unacronym():

    FILE_NAME = "/tmp/unacronym"

    REPLACE_DICT = {
        "&": "&amp",
        "<": "&lt",
        ">": "&gt",
        "\"": "&quot"
        "\'": "&#39"
    }

    def __init__(self):
        self.__buffer = Buffer()

    def preprocess(self):
        with open(FILE_NAME, "r") as input_file:
            for line in input_file:
                for old, replacement in self.REPLACE_DICT:
                    print(line.replace(old, replacement))

if __name__ == "__main__":
    ua = Unacronym()
    ua.preprocess()





