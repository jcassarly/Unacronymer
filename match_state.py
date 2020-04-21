import re

class MatchState():
    """Class to handle state variables for the acronym matching algorithm"""
    MAX_FAILED_MATCHES = 3 # number of matches to fail after exceeeding

    def __init__(self, acronym, buffer):
        """Init the state

        :param str acronym: the acronym being matched to a definition
        :param Buffer buffer: the buffer to find the definition in

        """
        self.__acronym = acronym
        self.__buffer = buffer
        self.__acronym_index = len(acronym) - 1
        self.__last_matched_index = len(acronym) # TODO: change this to be the length of the acronym not -1
        self.__buffer_index = 1
        self.__failed_matches = 0
        self.__definition = ""
        self.__update_next_word()

    def __update_next_word(self):
        """Update the next word to the next on in the buffer
        (as specified by the previously updated buffer index)

        """
        self.__next_word = self.__buffer.get_from_end(self.__buffer_index)

    def __update_definition(self):
        """Concatenate the next word onto the running definition"""
        self.__definition = "{} {}".format(self.__next_word, self.__definition)

    def __update_last_matched_index(self, was_matched):
        """Update the last matched index if was_matched is true"""
        if was_matched:
            self.__last_matched_index = self.__acronym_index

    def get_definition(self):
        """Get the definition from the match state"""
        # remove the space from the end of the definition
        return self.__definition[:-1]

    def go_to_next_letter(self):
        """Update the state to look at the next letter in the acronym"""
        self.__acronym_index = self.__acronym_index - 1

    def go_to_next_word(self, was_matched):
        """Upate the state to look at the next word

        if the current word was matched, update the state as such, otherwise update
        the fail count and reset back to the last matched index

        :param bool was_matched:
            whether or not the current word was matched
        :returns:
            True if the state succesfully updated to the next word, false if the
            buffer ran out of words to read (if the current word was matched and that ends the
            acronym, has_found_match will return true after this exits)

        """
        self.__buffer_index = self.__buffer_index + 1

        self.__update_definition()

        self.__update_last_matched_index(was_matched)

        if not self.__is_buffer_in_bounds():
            return False # Need to not update the rest of the state if we cannot get the next word

        self.__update_next_word()

        if was_matched:
            # reset the failed matches
            self.__failed_matches = 0

            # we matched at this index, so save that as the last matched
            self.__last_matched_index = self.__acronym_index

            self.go_to_next_letter()
        else:
            self.__failed_matches = self.__failed_matches + 1

            # reset the current index to the index after the last successful match
            self.__acronym_index = self.__last_matched_index - 1

        return True

    def __has_not_failed(self):
        """Verify that the fail count has not gotten too high

        :returns: true if the max failed matches have not been exceeded

        """
        return self.__failed_matches < self.MAX_FAILED_MATCHES

    def __is_buffer_in_bounds(self):
        """verify the buffer index has not gone out of bounds

        :returns: true if the buffer index is in bounds of the buffer, false otherwise

        """
        return self.__buffer.is_index_from_end_in_bounds(self.__buffer_index)

    def is_not_matching(self):
        """Checks if the state is still not matched

        :returns:
            True if the state has not yet found a match and has also not failed to find a match
            False if the state found a match or definitively failed to find a match

        """
        return self.__last_matched_index > 0 and self.__is_buffer_in_bounds() and self.__has_not_failed()

    def is_at_end_of_unmatched_word(self):
        """Checks whether the state is looking at a word that cannot be matched

        :returns: true if the current word cannot be matched

        """
        return self.__acronym_index < 0

    def has_found_match(self):
        """Checks whether a matching definition for the acronym has been found

        :returns: true if a defintion has been matched to the acronym

        """
        return self.__last_matched_index == 0

    def does_next_letter_match(self):
        """Checks if the next letter to look at in the acronym matches the first alphabetical character
        at the beginning of the current word

        :returns: true if the first letter match (ignoring case and non alphabetical characters)

        """
        # ignore non-letters at the beginning of the word
        test_word = re.sub("^(([^A-Za-z&])|(&amp)|(&lt)|(&gt)|(&quot)|(&#39))*", "", self.__next_word)
        return test_word.lower().startswith(self.__acronym[self.__acronym_index].lower())
