from utils.utilities import Utilities
from utils.constants import Constants
from core.student import Student
from core.source_report import SourceReport
import copy
class IndividualAssignment(dict):

    def __init__(self, name, student, course_name, grade=100, wrong_lines=[], source_report=None, compiled=False, ran=False):
        self.name = name
        self.student = student
        self.course_name = course_name
        self.grade = grade
        self.wrong_lines = []
        self.compiled = compiled
        self.ran = ran
        self.source_report = source_report

    @classmethod
    def from_json(cls, data):
        ia = cls(**data)
        ia.student = Student.from_json(data["student"])
        if not data["source_report"] == {}:
            ia.source_report = SourceReport.from_json(data["source_report"])
        return ia
        
    def to_dict(self):
        dic = copy.deepcopy(self.__dict__)
        dic["student"] = self.student.to_dict()
        if self.source_report is None:
            dic["source_report"] = {}
        else:
            dic["source_report"] = self.source_report.to_dict()

        return dic

    def reset(self):
        self.source_report = None
        self.wrong_lines = []

    def get_local_repo_path(self):
        #return Utilities.get_home_directory() + Constants.CLONE_DIRECTORY + "/" + self.course_name + "/" + self.repo_name + "/" + self.student.username
        return Utilities.get_home_directory() + Constants.CLONE_DIRECTORY + "/" + Utilities.construct_repo_path(self, self.student)

    def get_output_path(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + self.course_name + "/" + self.name + "/" + self.name +  "_" + self.student.username + ".txt"
    
    def get_compile_output_dir(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + self.course_name + "/" + self.name + "/" + "compile-temp/"
    
    def get_compile_output_path(self):
        return self.get_compile_output_dir() + self.name +  "_" + self.student.username + ".txt"

    def get_runtime_error_output_path(self):
        return self.get_compile_output_dir() + self.name +  "_" + self.student.username + "_runtime" + ".txt"