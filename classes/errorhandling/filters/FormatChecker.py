#This class is responsible for checking if an input is in a certain format
import re


class FormatChecker:
    def is_valid_passenger_id(id:str):
        pattern = r"^[A-Z][A-Z][A-Z]\d\d\d\d[A-Z][A-Z]\d$"
        return bool(re.match(pattern, id))

    def is_valid_flight_id(id:str):
        pattern = r"^[A-Z]{3}\d{4}[A-Z]{1}$"
        return bool(re.match(pattern, id))

    def is_valid_IATA_FAA_code(code:str):
        pattern = "^[A-Z]{3}$"
        return bool(re.match(pattern, code))

    def is_valid_departure_time(time:str):
        pattern = "^\d{10}$"
        return bool(re.match(pattern, time))

    def is_valid_flight_time(amount_of_time:str):
        pattern = "^\d{1,4}$"
        return bool(re.match(pattern, amount_of_time))

    def is_valid_airport_name(name:str):
        pattern = "^[A-Z]{3,20}$"
        return bool(re.match(pattern, name))

    def is_valid_latitude(latitude:str):
        try:
            latitude_float = float(latitude)
            if latitude_float <= float(90) and latitude_float >= float(-90):
                return True
            else:
                return False
        except:
            return False


    def is_valid_longitude(longitude:str):
        try:
            longitude_float = float(longitude)
            if longitude_float <= float(180) and longitude_float >= float(-180):
                return True
            else:
                return False
        except:
            return False


#
# correct_testcases = ["LLZ3798PE3", "SPR4484HA8", "WBE6935NU3"]
# wrong_testcases = ["PP2875LH3", "", "JJM4724R1F7", "AWBE6935NU3"]
#
# for case in correct_testcases:
#     if is_valid_passenger_id(case) == False:
#         raise Exception("Rejected a correct case: " + case)
#     else:
#         print("SUCCESS - Case '" + case + "' passed.")
#
# for case in wrong_testcases:
#     if is_valid_passenger_id(case):
#         raise Exception("Accepted a wrong case: " + case)
#     else:
#         print("SUCCESS - Case '" + case + "' rejected.")
#
# print()
# #Test is_valid_airport_name
# base = "A"
# for i in range(25):
#     name = base * i
#     if is_valid_airport_name(name):
#         print("VALID:", name)
#     else:
#         print("INVALID:", name)
#
# print(is_valid_latitude("79.554334"))
