import urllib.parse

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

class AcronymDict(list):

    def __init__(self):
        self.acronyms = []
        self.dict = {}

    def __iter__(self):
        for acronym in self.acronyms:
            yield acronym, self.dict[acronym]

    def add(self, key, value):
        self.acronyms.append(key)
        self.dict[key] = value

class Unacronym():

    INPUT_FILE_NAME = "/tmp/unacronym-in"
    PREPROCESS_FILENAME = "/tmp/unacronym-pre"
    REPLACE_FILENAME = "/tmp/unacronym-replace"

    REPLACE_DICT = {
#        "&": "&amp",
        "<": "&lt",
        ">": "&gt",
        "\"": "&quot",
        "\'": "&#39",
    }

    def __init__(self):
        self.__buffer = Buffer()
        self.acronyms = AcronymDict()
        self.acronyms.add("TCB", "TCP Control Block") # TODO: come back to this for how we want to sort the acronyms
        self.acronyms.add("TCP", "Transport Control Protocol")

    def preprocess(self):
        with open(self.PREPROCESS_FILENAME, "w") as output_file:
            with open(self.INPUT_FILE_NAME, "r") as input_file:
                for line in input_file:

                    updated_line = urllib.parse.unquote_plus(line)
                    updated_line = updated_line.replace("&", "&amp")


                    for old in self.REPLACE_DICT:
                        updated_line = updated_line.replace(old, self.REPLACE_DICT[old])

                    output_file.write(updated_line)



    def replace_acronyms(self):
        with open(self.REPLACE_FILENAME, "w") as output_file:
            with open(self.PREPROCESS_FILENAME, "r") as input_file:
                for line in input_file:

                    updated_line = line

                    for old, replacement in self.acronyms:
                        updated_line = updated_line.replace(old, "<font color=\"red\">{}</font>".format(replacement))

                    updated_line = updated_line.replace("\n", "<br />")

                    output_file.write(updated_line)



if __name__ == "__main__":
    ua = Unacronym()
    ua.preprocess()
    ua.replace_acronyms()






