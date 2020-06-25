import os
import importlib.machinery
import ntpath
from threading import Thread
import math
from copy import deepcopy
import sys
from shutil import copyfile

from classes import Commands
from classes.Context import Context
from classes.WorkerNode import WorkerNode
from classes.abstract_classes.AbstractUserInterface import AbstractUserInterface
from classes.errorhandling.CSVDataLoader import CSVDataLoader
from classes.errorhandling.filters.PassengerDataFilter import DataFilter
from classes.abstract_classes.AbstractJobRunner import AbstractJobRunner

class MasterNode:
    def __init__(self, interface: AbstractUserInterface, is_production: bool):
        #Command line interface to deal with the interface input.
        self.interface = interface

        #File storages
        if is_production:
            # For production
            self.maindir = os.path.dirname(sys.argv[0])
            self.input_file_dir = os.path.join(self.maindir, "./inputfiles")
            self.tempo_buffer_file_path = os.path.join(self.maindir, "./tempobuffer/tempo.txt")
            self.final_output_file_dir = os.path.join(self.maindir, "./outputfiles")
            self.jobrunner_file_dir = os.path.join(self.maindir, "./mapreduce_mods")
            self.data_loader_error_log_dir = os.path.join(self.maindir, "./dataloader_error_log")
        else:
            # For development on local
            print("- DEVELOPMENT MODE -")
            self.maindir = os.path.dirname(__file__)
            self.input_file_dir = os.path.join(self.maindir, "../inputfiles")
            self.tempo_buffer_file_path = os.path.join(self.maindir, "../tempobuffer/tempo.txt")
            self.final_output_file_dir = os.path.join(self.maindir, "../outputfiles")
            self.jobrunner_file_dir = os.path.join(self.maindir, "./mapreduce_mods")
            self.data_loader_error_log_dir = os.path.join(self.maindir, "../dataloader_error_log")

        #User map reduce
        self.worker_num = 3
        self.jobrunner_file_name = os.path.join(self.jobrunner_file_dir, "")
        self.jobrunner = None
        self.jobrunner_file_name = ""

        #Which mapper will take which file/
        self.mapper_and_inputdata_pairs = []
        self.reducer_and_outputpath_pairs = []

        #Data loader
        self.data_loader = CSVDataLoader(DataFilter())


    def _clean_input_data(self, input_file_name):
        self.data_loader.set_error_log_dir_path(self.data_loader_error_log_dir)
        self.data_loader.set_clean_data_dir_path(self.input_file_dir)
        input_file_path = os.path.join(self.input_file_dir, input_file_name)
        self.data_loader.clean_data(input_file_path)

    def _load_data(self, input_file_path) -> list:
        data_arr = []
        with open(input_file_path, "r") as file:
            line = file.readline()
            while line != "":
                data_arr.append(line)
                line = file.readline()
        return data_arr

    def _load_jobrunner_module(self, module_name) -> AbstractJobRunner:
        module_path = os.path.join(self.jobrunner_file_dir, module_name)

        jobrunner_mod = importlib.machinery.SourceFileLoader(module_name, module_path).load_module()

        # If the module does not have implementation of JobRunner class, raise an error.
        jobrunner_instance = None
        try:
            jobrunner_instance = jobrunner_mod.JobRunner()
        except:
            raise Exception("JobRunner class is not found in the provided mapreduce module.")
        return jobrunner_instance

    def _save_final_result(self, reduce_contexts: list, output_path):
        result = ""
        for reduce_context in reduce_contexts:
            for pair in reduce_context.get_key_val_pairs():
                key = pair[0]
                val = pair[1]
                result += str(key) + ":" + str(val) + "\n"
        with open(output_path, "w") as file:
            file.write(result)

        self.interface.display_output_save_message(output_path)

    def split_input_arr(self, input_arr: list):
        """
        :param data_arr: An array that contains all the lines from input data.
        :return: An array of tuples, each of which contains work
        """
        chunk_size = math.ceil(len(input_arr) / self.worker_num)
        work_chunks = []

        # Split the input_arr into chunks of the number of workers.
        # e.g) number of workers = 3 → work_chunks would have 3 chunks.
        for i in range(0, len(input_arr), chunk_size):
            work_chunks.append(input_arr[i:i + chunk_size])
        return work_chunks


    def _wait_until_all_threads_finish(self, all_threads: list):
        """
        :param all_threads:
        :void: Stop process until all the threads in the list finish.
        """
        for thread in all_threads:
            thread.join()


    def _run_mapreduce(self):
        # Array to keep track of all the worker instances
        workers = []
        for worker_index in range(self.worker_num):
            worker = WorkerNode()
            workers.append(worker)

        # Map

        # An array to keep track of the contexts to store map results.
        result_map_contexts = []

        # Execute the mapping process for "each mapper class & input data pair" by allocating the work for
        #  mutiple WorkerNodes.
        for pair in self.mapper_and_inputdata_pairs:
            # Get a mapper class
            mapper_class = pair["mapper_class"]

            # Get all the entire input data that is to be processed with the mapper class above
            input_arr = pair["inputdata"]

            # Split the work by the number of workers.
            work_chunks = self.split_input_arr(input_arr)

            # Set each worker the mapper class, allocate them a work_chunk, and start the thread.
            self.interface.display_mapping_start(mapper_class)
            all_threads = []
            for index in range(len(work_chunks)):
                worker = workers[index]
                worker.set_mapper(mapper_class)
                worker.set_lines_to_map(work_chunks[index])

                #Run the mapping process
                thread = Thread(target=worker.map())
                thread.start()
                all_threads.append(thread)

            self._wait_until_all_threads_finish(all_threads)

            # Get the mapper result from each node as context objects
            for worker in workers:
                mapper_context = deepcopy(worker.get_mapper_context())
                result_map_contexts.append(mapper_context)
                worker.clear_contexts()

            self.interface.display_mapping_end(mapper_class)

        # Shuffle
        shuffled_key_vals_pairs = {} #{key:[val, val,]}
        for map_context in result_map_contexts:
            for pair in map_context.get_key_val_pairs():
                key = pair[0]
                val = pair[1]
                if key not in shuffled_key_vals_pairs:
                    shuffled_key_vals_pairs[key] = []
                shuffled_key_vals_pairs[key].append(val)


        # Sort
        sorted_key_vals_pairs = {}
        for key in shuffled_key_vals_pairs:
            sorted_key_vals_pairs[key] = sorted(shuffled_key_vals_pairs[key])

        self.interface.display_shuffle_and_sort_end()

        # Reduce
        for pair in self.reducer_and_outputpath_pairs:
            outputfile_name = pair["output_path"]
            reducer_class = pair["reducer_class"]
            self.interface.display_reducing_start(reducer_class)

            # Set each worker the reducer class
            for worker_index in range(self.worker_num):
                workers[worker_index].set_reducer(reducer_class)

            workers_in_progress = []
            result_reduce_contexts = []
            worker_index = 0
            all_threads = []
            for key in sorted_key_vals_pairs:
                worker = workers[worker_index]
                worker.set_key_and_vals_pair_to_reduce(key, sorted_key_vals_pairs[key])
                # Run the reducing process
                thread = Thread(target=worker.reduce())
                thread.start()
                workers_in_progress.append(worker)
                all_threads.append(thread)

                # Once it activated all the available workers, wait until all the workers finish their assigned job,
                # and then start feeding them with the rest of keys & values.
                worker_index += 1
                if worker_index == self.worker_num:
                    self._wait_until_all_threads_finish(all_threads)

                    # Get the reducer result from each worker node as context objects
                    for worker in workers:
                        reducer_context = deepcopy(worker.get_reducer_context())
                        result_reduce_contexts.append(reducer_context)
                        worker.clear_contexts()

                    # Reset worker index to start with the first worker.
                    worker_index = 0
                    workers_in_progress.clear()

            # Once all the workers finish their job, get the reducer result from each worker node as context objects
            self._wait_until_all_threads_finish(all_threads)
            for worker in workers_in_progress:
                reducer_context = deepcopy(worker.get_reducer_context())
                result_reduce_contexts.append(reducer_context)
                worker.clear_contexts()

            self.interface.display_reducing_end(reducer_class)
            self._save_final_result(result_reduce_contexts, outputfile_name)


    """The code bellow is the fisrt sigle threaded prototype"""
    # def _run_single_threaded_mapreduce(self):
    #     # Mapping phase
    #     map_contexts = []
    #     for pair in self.mapper_and_inputdata_pairs:
    #         map_context = Context()
    #         mapper_class = pair["mapper_class"]
    #         mapper_class = mapper_class()
    #         data_arr = pair["inputdata"]
    #         for i in range(len(data_arr)):
    #             line = data_arr[i]
    #             mapper_class.map(str(i), line, map_context)
    #         map_contexts.append(map_context)
    #
    #     # Shuffling phase
    #     shuffled_key_vals_pairs = {} #{key:[val, val,]}
    #     for map_context in map_contexts:
    #         for pair in map_context.get_key_val_pairs():
    #             key = pair[0]
    #             val = pair[1]
    #             if key not in shuffled_key_vals_pairs:
    #                 shuffled_key_vals_pairs[key] = []
    #             shuffled_key_vals_pairs[key].append(val)
    #
    #     # Sorting phase
    #     sorted_key_vals_pairs = {}
    #     for key in shuffled_key_vals_pairs:
    #         sorted_key_vals_pairs[key] = sorted(shuffled_key_vals_pairs[key])
    #
    #     # Reducing phase
    #     for pair in self.reducer_and_outputpath_pairs:
    #         reduce_context = Context()
    #         outputfile_name = pair["output_path"]
    #         reducer_class = pair["reducer_class"]
    #         reducer = reducer_class()
    #
    #         for key in sorted_key_vals_pairs:
    #             sorted_values = sorted_key_vals_pairs[key]
    #             reducer.reduce(key, sorted_values, reduce_context)
    #         self._save_final_result(reduce_context, outputfile_name)
    #
    #


    def start(self):
        self.interface.display_activation()
        self.interface.display_thematic_break()
        data_filter = DataFilter()
        csv_loader = CSVDataLoader(data_filter)

        is_done = False
        while not is_done:
            command_obj = self.interface.accept_command()
            command = command_obj["command"]
            jobrunner_file_name = command_obj["jobrunner_file_name"]
            command_args = command_obj["args"]
            self.jobrunner_file_name = jobrunner_file_name
            if command == Commands.run:
                self.jobrunner = self._load_jobrunner_module(jobrunner_file_name)
                self.jobrunner.run(command_args, self.tempo_buffer_file_path)
                job_queue = self.jobrunner.get_job_queue()

                self.interface.display_job_queue(job_queue)
                self.interface.display_thematic_break()
                for job in job_queue:
                    self.interface.display_job(job)

                    self.mapper_and_inputdata_pairs.clear()
                    self.reducer_and_outputpath_pairs.clear()

                    #Load each input file, and store its data with a corresponding mapper.
                    for pair in job.get_mapper_inputfile_pairs():

                        if pair["inputfile"] == self.tempo_buffer_file_path:
                            input_data_file_path = self.tempo_buffer_file_path
                        else:
                            input_data_file_path = os.path.join(self.input_file_dir, pair["inputfile"])


                        input_data_arr = self._load_data(input_data_file_path)
                        mapper_and_inputdata_pair = {"mapper_class": pair["mapper_class"], "inputdata": input_data_arr}
                        self.mapper_and_inputdata_pairs.append(mapper_and_inputdata_pair)

                    for pair in job.get_reducer_outputfile_pairs():
                        if pair["outputfile"] == self.tempo_buffer_file_path:
                            output_path = self.tempo_buffer_file_path
                        else:
                            output_path = os.path.join(self.final_output_file_dir, pair["outputfile"])
                        reducer_and_outputfile_pair = {"reducer_class": pair["mapper_class"], "output_path": output_path}
                        self.reducer_and_outputpath_pairs.append(reducer_and_outputfile_pair)
                    self._run_mapreduce()
                    self.interface.display_thematic_break()

                self.interface.display_all_jobs_finished()
            elif command == Commands.clean:
                file_name = command_args[0]
                self._clean_input_data(file_name)
                self.interface.display_done_cleaning(file_name)

            elif command == Commands.quit:
                is_done = True
        self.interface.display_quit()
