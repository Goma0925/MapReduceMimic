from abc import *
from os import path as Path
from classes.abstract_classes import AbstractMapper
from classes.abstract_classes import AbstractReducer
from classes.Job import Job

class AbstractUserInterface(metaclass=ABCMeta):
    @abstractmethod
    def accept_command(self):
        pass

    @abstractmethod
    def display_activation(self):
        pass

    @abstractmethod
    def display_quit(self):
        pass

    @abstractmethod
    def display_done_cleaning(self, file_name: str):
        pass

    @abstractmethod
    def display_job_queue(self, job_queue:list):
        pass

    @abstractmethod
    def display_job(self, job: Job):
        pass

    @abstractmethod
    def display_thematic_break(self):
        pass

    @abstractmethod
    def display_mapping_start(self, mapper_class: AbstractMapper):
        pass

    @abstractmethod
    def display_mapping_end(self, mapper_class: AbstractMapper):
        pass

    @abstractmethod
    def display_shuffle_and_sort_end(self):
        pass

    @abstractmethod
    def display_reducing_start(self, reducer_class: AbstractReducer):
        pass

    @abstractmethod
    def display_reducing_end(self, reducer_class: AbstractReducer):
        pass

    @abstractmethod
    def display_output_save_message(self, output_path:Path):
        pass

    @abstractmethod
    def display_all_jobs_finished(self):
        pass