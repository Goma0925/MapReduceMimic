from abc import *
from classes.Job import Job
from classes.abstract_classes.AbstractJobRunner import AbstractJobRunner
from classes.abstract_classes.AbstractContext import AbstractContext
from classes.abstract_classes.AbstractMapper import AbstractMapper
from classes.abstract_classes.AbstractReducer import AbstractReducer
from datetime import datetime, timedelta
import os.path as Path


class PassengerDataMapper(AbstractMapper):
    """
        Map the passenger data into the following format
            <flight_id>: <String of the row>
    """
    def map(self, key: str, value: str, context: AbstractContext):
        value_list = value.split(",")
        flight_id = value_list[1]
        context.write(flight_id, value)


class Reducer(AbstractReducer):
    def reduce(self, key: str, values: list, context: AbstractContext):
        flight_id_txt_box =  "┌──────────────────────────────────────────────────\n"
        flight_id_txt_box += "│ FLIGHT ID - " + key


        #Because a flight with the same ID has the same basic information, just take the first one.
        data_txt = values[0].rstrip("\n")
        data_list = data_txt.split(",")

        #Get the basic info
        departure_airport_code = data_list[2]
        arrival_airport_code = data_list[3]

        departure_time_datetime = datetime.fromtimestamp(int(data_list[4]))
        departure_time_str = departure_time_datetime.strftime('%c')

        flight_time_datetime = timedelta(minutes=int(data_list[5]))
        flight_time_str = data_list[5] + " minutes"

        arrival_time_datetime = departure_time_datetime + flight_time_datetime
        arrival_time_str = arrival_time_datetime.strftime('%c')

        #Get all the passengers on the flight
        passenger_id_list = []
        for line in values:
            passenger_id = line.split(",")[0]
            passenger_id_list.append(passenger_id)

        #Create the text format to record in output.
        result = "\n"
        result += "├──────────────────────────────────────────────────\n"
        result += "│ DEPARTURE AIRPORT: " + departure_airport_code + "\n"
        result += "│ ARRIVAL AIRPORT  : " + arrival_airport_code + "\n"
        result += "│ DEPARTED AT      : " + departure_time_str + "\n"
        result += "│ ARRIVED  AT      : " + arrival_time_str + "\n"
        result += "│ FLIGHT TIME      : " + flight_time_str + "\n"
        result += "│ PASSENGER ID LIST: NUMBER OF PASSENGERS = " + str(len(passenger_id_list)) + "\n"
        for passenger_id in passenger_id_list:
            result += "│    - " + passenger_id + "\n"
        result += "└──────────────────────────────────────────────────\n"

        context.write(flight_id_txt_box, result)


class JobRunner(AbstractJobRunner):
    def run(self, commandArgs: list, tempoFileBufferPath: Path):
        job = Job()
        job.set_mapper(PassengerDataMapper, commandArgs[0])
        job.set_reducer(Reducer, "(2)List_of_flights_by_FlightID.txt")
        self.add_to_job_queue(job)