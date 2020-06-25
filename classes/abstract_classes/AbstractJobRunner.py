from abc import *
from classes.Job import Job
import os

class AbstractJobRunner(metaclass=ABCMeta):
    def __init__(self):
        self.job_queue = []

    @abstractmethod
    def run(self, command_args: list, tempo_file_buffer: os.path):
        pass

    def add_to_job_queue(self, job: Job):
        self.job_queue.append(job)

    def get_job_queue(self):
        return self.job_queue
