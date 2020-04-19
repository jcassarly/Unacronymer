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

    def is_index_from_end_in_bounds(self, index_from_end):
        converted_index = len(self.__buffer) - 1 - index_from_end
        return (converted_index >= 0 and converted_index < self.SIZE)

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

    def __contains__(self, key):
        return key in self.acronyms

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
        "<": "&lt;",
        ">": "&gt;",
        "\"": "&quot;",
        "\'": "&#39;",
    }

    def __init__(self):
        self.__buffer = Buffer()
        self.acronyms = AcronymDict()
        #self.acronyms.add("TCB", "TCP Control Block") # TODO: come back to this for how we want to sort the acronyms
        #self.acronyms.add("TCP", "Transport Control Protocol")

    def preprocess(self):
        with open(self.PREPROCESS_FILENAME, "w") as output_file:
            with open(self.INPUT_FILE_NAME, "r") as input_file:
                for line in input_file:

                    updated_line = urllib.parse.unquote_plus(line)
                    updated_line = updated_line.replace("&", "&amp;")


                    for old in self.REPLACE_DICT:
                        updated_line = updated_line.replace(old, self.REPLACE_DICT[old])

                    output_file.write(updated_line)

    def match_acronym(self, acronym):
        """Returns none if no match, otherwise returns the matched def
        """
        acronym_index = len(acronym) - 1
        last_matched_index = acronym_index # TODO: change this to be the length of the acronym not -1
        buffer_index = 1
        MAX_FAILED_MATCHES = 3
        failed_matches = 0
        definition = ""

        # get the first word before the acronym in the buffer
        next_word = self.__buffer.get_from_end(buffer_index)

        # iterate until a definition is found or acronym is found to not have a definiton
        while last_matched_index > 0 \
              and self.__buffer.is_index_from_end_in_bounds(buffer_index) \
              and failed_matches <= MAX_FAILED_MATCHES:

            # if the current word does not match and of the letters that have not been matched
            # and we have not failed to match a word for MAX_FAILED_MATCHES times
            if acronym_index < 0 and failed_matches <= MAX_FAILED_MATCHES:

                failed_matches = failed_matches + 1
                buffer_index = buffer_index + 1

                # reset the current index to the index after the last successful match
                acronym_index = last_matched_index - 1

                if not self.__buffer.is_index_from_end_in_bounds(buffer_index):
                    return None

                # add the word to the def and go to the next word to try matching that
                definition = "{} {}".format(next_word, definition)
                next_word = self.__buffer.get_from_end(buffer_index)

            # ignore non letters at the beginning of the word
            test_word = re.sub("^(([^A-Za-z&])|(&amp)|(&lt)|(&gt)|(&quot)|(&#39))*", "", next_word)

            # check if the test word's first letter matches the current index of the acronym
            if test_word.lower().startswith(acronym[acronym_index].lower()):

                # reset the failed matches
                failed_matches = 0

                # we matched at this index, so save that as the last matched
                last_matched_index = acronym_index

                acronym_index = acronym_index - 1
                buffer_index = buffer_index + 1

                # add the matched word to the definition and go to the next word
                definition = "{} {}".format(next_word, definition)
                next_word = self.__buffer.get_from_end(buffer_index)

            # if we dont have a match, try again on the next letter in the acronym
            else:
                acronym_index = acronym_index - 1

        # return the definition unless we did not find a complete definition match
        return definition[0:len(definition) - 1] if last_matched_index == 0 else None



    def build_dictionary(self):
        with open(self.PREPROCESS_FILENAME, "r") as input_file:
            for line in input_file:
                words = line.split()
                #words.remove("") #TODO: ignore empty strings

                for word in words:
                    self.__buffer.add(word)

                    match = re.fullmatch("\(([A-Z][A-Za-z]*[A-Z])[s]?[)]*([:;?.,]|(&quot)|(&#39))*", word)
                    if match is not None:
                        acronym = match.group(1)
                        definition = self.match_acronym(acronym)

                        if definition is not None and not acronym in self.acronyms:
                            self.acronyms.add(acronym, definition)

        self.acronyms.sort() # TODO: sort by acronym length to do longest matching

    def replace_acronyms(self):
        with open(self.REPLACE_FILENAME, "w") as output_file:
            with open(self.PREPROCESS_FILENAME, "r") as input_file:
                for line in input_file:

                    updated_line = line

                    # TODO: change color on acronyms that are not in the dictionary
                    for old, replacement in self.acronyms:
                        updated_line = re.sub("(^|[^>A-Z]){}([^<A-Z]|$)".format(old), r"\1<font color='RED'>{} ({})</font>\2".format(replacement, old), updated_line)

                    updated_line = updated_line.replace("\n", "<br />")

                    output_file.write(updated_line)



if __name__ == "__main__":
    ua = Unacronym()
    #print(ua.match_acronym("TCP"))
    ua.preprocess()
    ua.build_dictionary()
    ua.replace_acronyms()






