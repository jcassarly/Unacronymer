import urllib.parse
import re

class Buffer():

    SIZE = 256

    def __init__(self):
        self.__buffer = []

    def add(self, new_item):
        if len(self.__buffer) >= self.SIZE:
            self.__buffer.pop(0)

        self.__buffer.append(new_item)

    def get(self, index):
        return self.__buffer[index]

    def is_in_bounds(self,index):
        return (index >= 0 and index < self.SIZE)

    def get_from_end(self, index_from_end):
        return self.__buffer[len(self.__buffer) - 1 - index_from_end]

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

    def sort(self):
        self.acronyms = sorted(self.acronyms)
        self.acronyms.reverse()

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

    def match_acronym(self, acronym):
        """Returns none if no match, otherwise returns the matched def
        """
        acronym_index = len(acronym) - 1
        last_matched_index = acronym_index
        buffer_index = 1
        MAX_FAILED_MATCHES = 3
        failed_matches = 0
        definition = ""
        next_word = self.__buffer.get_from_end(buffer_index)
        while last_matched_index >= 0 and self.__buffer.is_in_bounds(buffer_index):
            if acronym_index < 0 and failed_matches <= MAX_FAILED_MATCHES:
                failed_matches = failed_matches + 1
                buffer_index = buffer_index + 1
                acronym_index = last_matched_index - 1

                next_word = self.__buffer.get_from_end(buffer_index)

            if next_word.lower().startswith(acronym[acronym_index].lower()):
                definition = "{} {}".format(next_word, definition)

                failed_matches = 0
                last_matched_index = acronym_index
                acronym_index = acronym_index - 1
                buffer_index = buffer_index + 1

                next_word = self.__buffer.get_from_end(buffer_index)

            # p o s Interface (POSIX)
            # Lord of of of of of The Rings (LTR)
            else:
                acronym_index = acronym_index - 1




    def build_dictionary(self):
        with open(self.PREPROCESS_FILENAME, "r") as input_file:
            for line in input_file:
                words = line.split()

                for word in words:
                    self.__buffer.add(word)

                    match = re.fullmatch("\(([A-Z][A-Za-z]*[A-Z])[)]*[:;?.,\"']*", word)
                    if match is not None:
                        acronym = match.group(1)
                        definition = self.match_acronym(acronym)

                        if definition is not None:
                            self.acronyms.add(acronym, definition)

        self.acronyms.sort() # TODO: sort by acronym length to do longest matching

    def replace_acronyms(self):
        with open(self.REPLACE_FILENAME, "w") as output_file:
            with open(self.PREPROCESS_FILENAME, "r") as input_file:
                for line in input_file:

                    updated_line = line

                    # TODO: change color on acronyms that are not in the dictionary
                    for old, replacement in self.acronyms:
                        updated_line = re.sub("(^|[^>A-Z]){}([^<A-Z]|$)".format(old), r"\1>{}<\2".format(replacement), updated_line)

                    updated_line = updated_line.replace("\n", "<br />")

                    output_file.write(updated_line)



if __name__ == "__main__":
    ua = Unacronym()
    ua.preprocess()
    ua.replace_acronyms()






