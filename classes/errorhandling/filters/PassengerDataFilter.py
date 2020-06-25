import re
from abc import *
from .FormatChecker import FormatChecker
from classes.abstract_classes.AbstractDataFilter import AbstractDataFilter

class DataFilter(AbstractDataFilter):
    def filter(self, line_index: str, csv_line: str):
        is_valid_line = True
        filtered_line = ""
        post_process_message = ""

        line_items = csv_line.split(",")
        line_items[-1] = line_items[-1].rstrip("\n")

        if not FormatChecker.is_valid_passenger_id(line_items[0]):
            is_valid_line = False
            #print("REJECTED passenger ID:", line_items[0])
        if not FormatChecker.is_valid_flight_id(line_items[1]):
            is_valid_line = False
            #print("REJECTED flight ID:", line_items[1])
        if not FormatChecker.is_valid_IATA_FAA_code(line_items[2]):
            is_valid_line = False
            #print("REJECTED departure airport code:", line_items[2])
        if not FormatChecker.is_valid_IATA_FAA_code(line_items[3]):
            is_valid_line = False
            #print("REJECTED arrival airport code:", line_items[3])
        if not FormatChecker.is_valid_departure_time(line_items[4]):
            is_valid_line = False
            #print("REJECTED departure time:", line_items[4])
        if not FormatChecker.is_valid_flight_time(line_items[5]):
            is_valid_line = False
            #print("REJECTED flight time:", line_items[5])

        if is_valid_line:
            for item in line_items:
                filtered_line += item + ","
            filtered_line = filtered_line.rstrip(",")
            filtered_line += "\n"
        else:
            post_process_message += ("   line " + str(line_index) + ": " + csv_line)

        return is_valid_line, filtered_line, post_process_message
