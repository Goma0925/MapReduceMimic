from classes.Context import Context
from classes.abstract_classes import AbstractMapper as MapperClass
from classes.abstract_classes import AbstractReducer as ReducerClass
from classes.ModuleImporter import *

class WorkerNode:
    def __init__(self):
        self.assigned_lines_to_map = [] # This is a job for this worker to map
        self.assigned_key_to_reduce = ""
        self.assigned_vals_to_reduce = [] # This is a job for this worker to reduce
        self.mapper = None
        self.reducer = None
        self.map_context = Context()
        self.reduce_context = Context()

    def set_mapper(self, mapper_class: MapperClass):
        self.mapper = mapper_class()

    def set_reducer(self, reducer_class: ReducerClass):
        self.reducer = reducer_class()

    def set_lines_to_map(self, assigned_lines_to_map:list):
        self.assigned_lines_to_map = assigned_lines_to_map

    def set_key_and_vals_pair_to_reduce(self, assigned_key_to_reduce: str, assigned_vals_to_reduce: list):
        self.assigned_key_to_reduce = assigned_key_to_reduce
        self.assigned_vals_to_reduce = assigned_vals_to_reduce

    def map(self):
        for i in range(len(self.assigned_lines_to_map)):
            self.mapper.map(str(i), self.assigned_lines_to_map[i], self.map_context)


    def reduce(self): #Fix parameters
        self.reducer.reduce(self.assigned_key_to_reduce, self.assigned_vals_to_reduce, self.reduce_context)


    def get_mapper_context(self):
        return self.map_context

    def get_reducer_context(self):
        return self.reduce_context

    def clear_contexts(self):
        self.map_context.clear()
        self.reduce_context.clear()