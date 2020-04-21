import urllib.parse
import re
import io
from buffer import Buffer
from ordered_dict import OrderedDict, AcronymDict
from match_state import MatchState

ENCODING = 'utf8'

REPLACE_DICT = OrderedDict()
REPLACE_DICT.add("&", "&amp;")
REPLACE_DICT.add("<", "&lt;")
REPLACE_DICT.add(">", "&gt;")
REPLACE_DICT.add("\"", "&quot;")
REPLACE_DICT.add("\'", "&#39;")

class Unacronym():
    """Class to remove acronyms from the text in INPUT_FILE_NAME"""

    INPUT_FILE_NAME = "/tmp/unacronym-in"
    PREPROCESS_FILENAME = "/tmp/unacronym-pre"
    REPLACE_FILENAME = "/tmp/unacronym-replace"

    def __init__(self):
        self.__buffer = Buffer()
        self.acronyms = AcronymDict()

    def preprocess(self):
        """Prepreocess the data in INPUT_FILE_NAME to remove HTML injection and only display as plain text"""
        with io.open(self.PREPROCESS_FILENAME, "w", encoding=ENCODING) as output_file:
            with io.open(self.INPUT_FILE_NAME, "r", encoding=ENCODING) as input_file:
                for line in input_file:

                    updated_line = urllib.parse.unquote_plus(line)

                    for old, replacement in REPLACE_DICT:
                        updated_line = updated_line.replace(old, replacement)

                    output_file.write(updated_line)

    def __define_if_match(self, acronym):
        """Adds the acronym to the acronym dictionary if it has a matching definition
        before it in the buffer

        :param str acronym: the acronym to find a definition for

        """
        state = MatchState(acronym, self.__buffer)

        # iterate until a definition is found or acronym is found to not have a definiton
        while state.is_not_matching():

            if state.is_at_end_of_unmatched_word():
                state.go_to_next_word(False)

            # check if the next word's first letter matches the current index of the acronym
            if state.does_next_letter_match():
                state.go_to_next_word(True)

            # if we dont have a match, try again on the next letter in the acronym
            else:
                state.go_to_next_letter()

        # add the definition only if we found a complete match
        if state.has_found_match():
            self.acronyms.add(acronym, state.get_definition())

    def build_dictionary(self):
        """Build the acronym dictionary from the preprocessed data"""
        with io.open(self.PREPROCESS_FILENAME, "r", encoding=ENCODING) as input_file:
            for line in input_file:
                for word in line.split():
                    self.__buffer.add(word)

                    match = re.fullmatch("\(([A-Z][A-Za-z]*[A-Z])[s]?[)]*([:;?.,]|(&quot)|(&#39))*", word)
                    if match is not None:
                        self.__define_if_match(match.group(1))

        # sort the acronyms so that longer ones come first - longer matches have priority
        self.acronyms.sort()

    def replace_acronyms(self):
        """Replace the acronyms in the preprocessed data with those in the acronym dictionary

        Outputs to REPLACE_FILENAME

        """
        with io.open(self.REPLACE_FILENAME, "w", encoding=ENCODING) as output_file:
            with io.open(self.PREPROCESS_FILENAME, "r", encoding=ENCODING) as input_file:
                for line in input_file:

                    updated_line = line

                    # replace each instance of an acronym with its definition
                    for old, replacement in self.acronyms:
                        updated_line = re.sub(r"(^|[^>A-Z]){}([^<A-Z]|$)".format(old), r"\1<font color='RED'>{} ({})</font>\2".format(replacement, old), updated_line)

                    updated_line = updated_line.replace("\n", "<br />")

                    output_file.write(updated_line)



if __name__ == "__main__":
    ua = Unacronym()
    ua.preprocess()
    ua.build_dictionary()
    ua.replace_acronyms()






