from abc import *


class AbstractDataFilter(metaclass=ABCMeta):

    @abstractmethod
    def filter(self, line_index: str, csv_line: str):
        """
            This abstract method takes each csv line and returns the following values.
            :rtype:
                is_valid_line  -  A boolean to specify if the line input was valid.
                filtered_line  -  A string of the reformatted/cleaned csv_line. This will be used for processing.
                post_process_message - A string to tell the result of the cleaning. Return an error message if
                errors occurred while filtering the data.
        """
        pass
