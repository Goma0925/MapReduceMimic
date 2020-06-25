#Responsible for prompting, retrieving, and validating user inputs.
from classes.abstract_classes.AbstractUserInterface import AbstractUserInterface
from os import path as Path
from classes.abstract_classes import AbstractMapper
from classes.abstract_classes import AbstractReducer
from classes.Job import Job

class TestInputInterface(AbstractUserInterface):
    def accept_command(self):
        """RUN"""
        # args = ["AComp_Passenger_data_no_error.csv", "Top30_airports_LatLong.csv"]
        # command = "run"
        jobrunner_file_name =  "(4)HighestMileage.py"

        """CLEAN"""
        args = ["AComp_Passenger_data.csv", "Top30_airports_LatLong.csv"]
        command = "CLEAN"

        print("   command        :", command)
        print("   jobrunner file :", jobrunner_file_name)
        print("   command_args   :", args)
        return {"command": command, "jobrunner_file_name": jobrunner_file_name, "args": args}

    def display_activation(self):
        print("Adoop started")

    def display_job_queue(self, job_queue:list):
        print("   job_queue      :", str(len(job_queue)) + " jobs in queue.")

    def display_job(self, job: Job):
        print("   JOB              :  " + str(job))

    def display_thematic_break(self):
        print("--------------------------------------------------------------------------")

    def display_mapping_start(self, mapper_class: AbstractMapper):
        print("   Mapping..........:  " + str(mapper_class))

    def display_mapping_end(self, mapper_class: AbstractMapper):
        print("   Mapping finished :  " + str(mapper_class))

    def display_shuffle_and_sort_end(self):
        print("   Shuffling & sorting finished")

    def display_reducing_start(self, reducer_class: AbstractReducer):
        print("   Reducing.........:  " + str(reducer_class))

    def display_reducing_end(self, reducer_class: AbstractReducer):
        print("   Reducing finished:  " + str(reducer_class))

    def display_output_save_message(self, output_path:Path):
        print("   Output saved     :  " + output_path)

    def display_all_jobs_finished(self):
        print("   All jobs executed successfully.")