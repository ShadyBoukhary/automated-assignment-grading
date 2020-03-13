from utils.utilities import Utilities
from core.individual_assignment import IndividualAssignment
import copy


class Assignment(dict):

    def __init__(self, name, course_name, individual_assignments, tolerance=0, table_formatting = False, strings_matter = True, input_file="", skipped_assignments=[], executionOnly=False):
        self.name = name
        self.course_name = course_name
        self.individual_assignments = individual_assignments
        self.skipped_assignments = skipped_assignments
        self.tolerance = tolerance
        self.table_formatting = table_formatting
        self.strings_matter = strings_matter
        self.input_file = input_file
        self.executionOnly = executionOnly
        if not input_file == "" and not Utilities.path_exists(self.get_input_file_path()):
            contents = Utilities.read_file(input_file)
            Utilities.create_file_dir_if_not_exists(self.get_input_file_path())
            Utilities.write_file(self.get_input_file_path(), contents, "w+")
            self.input_file = self.get_input_file_path()

    @classmethod
    def from_json(cls, data):
        assignment = Assignment(**data)
        assignment.skipped_assignments = list(map(IndividualAssignment.from_json, data["skipped_assignments"]))
        assignment.individual_assignments = list(map(IndividualAssignment.from_json, data["individual_assignments"]))

        return assignment
        
    def to_dict(self):
        dic = copy.deepcopy(self.__dict__)
        dic["individual_assignments"] = [i.to_dict() for i in self.individual_assignments]
        dic["skipped_assignments"] = [i.to_dict() for i in self.skipped_assignments]
        return dic

    def get_assignment_folder_path(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + self.course_name + "/" + self.name + "/"

    def get_clone_path(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + self.course_name + "/repositories/"

    def get_rubric_file_path(self):
        return self.get_assignment_folder_path() + self.name + "_rubric.json"
    
    def get_weights_file_path(self):
        return self.get_assignment_folder_path() + self.name + "_weights.txt"

    def get_input_file_path(self):
        return self.get_assignment_folder_path() + self.name + "_interactive_input.txt"

    def get_reports_dir_path(self):
        path = Utilities.get_full_dir_path() + "/../../reports/" + self.course_name + "/"
        if not Utilities.path_exists(path):
            Utilities.create_dir(path)
        return path

    def get_students_file_path(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + self.course_name + "/" + "students.json"

    def create_student_file(self, student_file):
        contents = Utilities.read_file(student_file)
        Utilities.create_file_dir_if_not_exists(self.get_students_file_path())
        Utilities.write_file(self.get_students_file_path(), contents, "w+")

    def create_rubric_file(self, rubric_file):
        contents = Utilities.read_file(rubric_file)
        Utilities.create_file_dir_if_not_exists(self.get_rubric_file_path())
        Utilities.write_file(self.get_rubric_file_path(), contents, "w+")

    def create_input_file(self, input_file):
        contents = Utilities.read_file(input_file)
        Utilities.create_file_dir_if_not_exists(self.get_input_file_path())
        Utilities.write_file(self.get_input_file_path(), contents, "w+")
        self.input_file = self.get_input_file_path()
