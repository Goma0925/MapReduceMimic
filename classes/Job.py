from classes.abstract_classes import AbstractMapper
from classes.abstract_classes import AbstractReducer

class Job:
    """
        This class keeps track of the mapper & the input file combination
        and the reducer & output file combination.
    """
    def __init__(self):
        self.mapper_inputfile_pairs = [] #[(mapperClass:AbstractMapper, inputFileName:str), ....]
        self.reducer_outputfile_pairs = [] #[{"file_name", file_name, "mapper_class", reducer_class}, ....]

    def set_mapper(self, mapper_class: AbstractMapper, file_name: str):
        pair = {"inputfile": file_name, "mapper_class": mapper_class}
        self.mapper_inputfile_pairs.append(pair)

    def set_reducer(self, reducer_class: AbstractReducer, file_name: str):
        pair = {"outputfile": file_name, "mapper_class": reducer_class}
        self.reducer_outputfile_pairs.append(pair)

    def get_mapper_inputfile_pairs(self):
        return self.mapper_inputfile_pairs

    def get_reducer_outputfile_pairs(self):
        return self.reducer_outputfile_pairs

