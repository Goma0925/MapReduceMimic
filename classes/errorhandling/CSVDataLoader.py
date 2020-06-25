#Data cleaner is responsible for removing the errors from the input file and save the clean data.
from classes.abstract_classes.AbstractDataFilter import *
import os
import ntpath

class CSVDataLoader:
    """
        This class loads and clean data from a CSV file using a DataFilter class.
    """
    def __init__(self,  data_filter: AbstractDataFilter):
        self.data_filter = data_filter
        self.is_done_loading = False
        self.error_messages = []
        self.error_log_dir_path = None
        self.clean_data_dir_path = None

    def set_data_filter(self, data_filter: AbstractDataFilter):
        self.data_filter = data_filter

    def set_error_log_dir_path(self, path: os.path):
        self.error_log_dir_path = path

    def set_clean_data_dir_path(self, path: os.path):
        self.clean_data_dir_path = path

    def _load_data(self, file_path: os.path):
        data_loaded = []
        with open(file_path, "r") as file:
            line = file.readline()
            while line != "":
                data_loaded.append(line)
                line = file.readline()
        return data_loaded


    def _save_error_log(self):
        if self.is_done_loading and self.error_log_dir_path != "":
            log = ""
            for message in self.error_messages:
                log += message + "\n"
            try:
                file_path = self.error_log_dir_path + "-test"
                with open(file_path, "w") as file:
                    file.write(log)
            except FileNotFoundError as e:
                raise e
            except TypeError:
                raise Exception("CSVDataLoader does not have a specified error log file path. Set a error log directory by using set_error_log_file_path before saving an error log.")

        else:
            if not self.is_done_loading:
                raise Exception("CSVDataLoader does not have any error log. Load data by using clean_data() before saving an error log.")


    def _path_leaf(self, path: os.path):
        """
            Extract a file name from a path.
        :return:
        """
        path_str = str(path)
        head, tail = ntpath.split(path_str)
        return tail or ntpath.basename(head)


    def _save_cleaned_data(self, cleaned_data: list, uncleaned_file_path: os.path):
        cleaned_text = ""
        for line in cleaned_data:
            cleaned_text += line

        uncleaned_file_name = self._path_leaf(uncleaned_file_path).split(".")[0]
        try:
            uncleaned_file_extension = self._path_leaf(uncleaned_file_path).split(".")[1]
        except:
            uncleaned_file_extension = ""

        cleaned_data_file_name = str(uncleaned_file_name) + "_CLEANED." + str(uncleaned_file_extension)
        with open(os.path.join(self.clean_data_dir_path, cleaned_data_file_name), "w") as file:
            file.write(cleaned_text)


    def clean_data(self, file_path):
        raw_data = self._load_data(file_path)
        cleaned_data = []
        error_messages = []
        if self.data_filter is not None:
            #Filter each line of input file.
            for i in range(len(raw_data)):
                is_valid_line, filtered_line, post_process_message = self.data_filter.filter(str(i), raw_data[i])
                if is_valid_line:
                    #If a line is a valid line, add it to the cleaned_data
                    cleaned_data.append(filtered_line)
                else:
                    #If a line is not valid, do not add it to the cleaned data, and keep the log.
                    error_messages.append(post_process_message)

            self.error_messages = error_messages
            self.is_done_loading = True
            self._save_cleaned_data(cleaned_data, file_path)
        else:
            raise Exception("CSVDataLoader needs to have a filter to clean raw data. Set a filter by using DataCleaner.set_data_filter()")

