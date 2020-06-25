#Responsible for prompting, retrieving, and validating user inputs.
from classes.abstract_classes.AbstractUserInterface import AbstractUserInterface
from os import path as Path
from classes.abstract_classes import AbstractMapper
from classes.abstract_classes import AbstractReducer
from classes.Job import Job
from classes import Commands

class CLI(AbstractUserInterface):
    def accept_command(self):
        is_valid_input = False
        input_args = []
        while not is_valid_input:
            command_input = input("adoop=# ")
            input_args = " ".join(command_input.split()).split(" ")

            if self._is_valid_command(input_args[0]):
                is_valid_input = True
            else:
                is_valid_input = False
                print("  INVALID INPUT: Command '" + input_args[0] + "' is not a valid command.")

            # Check if second command line arg is provided
            if input_args[0] == Commands.run or input_args[0] == Commands.clean:
                if len(input_args) >= 2:
                    is_valid_input = True
                else:
                    is_valid_input = False
                    if input_args[0] == Commands.run:
                        print("  INVALID INPUT: Please specify the name of the mapreduce file in the second argument.")
                    elif input_args[0] == Commands.clean:
                        print("  INVALID INPUT: Please specify at least one absolute file path of a file to clean.")

        if input_args[0] == Commands.run:
            command = input_args[0]
            jobrunner_file_name = input_args[1]
            try:
                args = input_args[2:]
            except:
                args = []
            print("   command        :", command)
            print("   jobrunner file :", jobrunner_file_name)
            print("   command_args   :", args)
            return {"command": command, "jobrunner_file_name": jobrunner_file_name, "args": args}

        elif input_args[0] == Commands.clean:
            command = input_args[0]
            try:
                args = input_args[1:]
            except:
                args = []
            print("   command        :", command)
            print("   command_args   :", args)
            return {"command": command, "jobrunner_file_name": "NONE", "args": args}
        elif input_args[0] == Commands.quit:
            command = input_args[0]
            print("   command        :", command)
            return {"command": command, "jobrunner_file_name": "NONE", "args": []}
        else:
            raise Exception("Could not handle an invalid command.")

    def _is_valid_command(self, command):
        if command == Commands.run or command == Commands.clean or command == Commands.quit:
            return True
        else:
            return False

    def display_activation(self):
        print("Adoop started")

    def display_quit(self):
        print("Adoop exited process.")

    def display_done_cleaning(self, file_name: str):
        print("   Finished cleaning the input file. Created a new cleaned file in the inputfiles directory.")

    def display_job_queue(self, job_queue:list):
        print("   job_queue      :", str(len(job_queue)) + " jobs in queue.")

    def display_job(self, job: Job):
        print("   JOB              :  " + str(job))

    def display_thematic_break(self):
        print("   --------------------------------------------------------------------------")

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
        print("   All jobs executed successfully. Check the outputfiles directory for the results.")