from utils.utilities import Utilities
from utils.constants import Constants
from core.student import Student
from core.source_report import SourceReport
import copy


class IndividualAssignment(dict):

    def __init__(self, name, student, course_name, grade=100, wrong_lines=[], source_report=SourceReport(), compiled=False, ran=False, error='', error_details=''):
        self.name = name
        self.student = student
        self.course_name = course_name
        self.grade = grade
        self.wrong_lines = wrong_lines
        self.compiled = False
        self.ran = ran
        self.source_report = source_report
        self.error = error
        self.error_details = error_details

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
        dic["source_report"] = self.source_report.to_dict()

        return dic

    def reset(self):
        self.source_report = None
        self.wrong_lines = []

    def get_clone_path(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + self.course_name + "/repositories/"

    def get_local_repo_path(self):
        return self.get_clone_path() + Utilities.construct_repo_path(self.student)

    def get_output_path(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + \
            self.course_name + "/" + self.name + "/" + self.name +  \
            "_" + self.student.username + ".txt"

    def get_compile_output_dir(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + \
            self.course_name + "/" + self.name + "/" + "compile-temp/"

    def get_compile_output_path(self):
        return self.get_compile_output_dir() + self.name + "_" + \
            self.student.username + ".txt"

    def get_runtime_error_output_path(self):
        return self.get_compile_output_dir() + self.name + "_" + \
            self.student.username + "_runtime" + ".txt"

    def seterr(self, error, details):
        self.error_details = details
        self.error = error

    def has_error(self):
        return self.error != ''
