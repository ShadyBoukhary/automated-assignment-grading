from utils.utilities import Utilities

class Assignment(dict):

    def __init__(self, name, course_name, individual_assignments, tolerance = 0, table_formatting = False, strings_matter = True, input_file=""):
        self.name = name
        self.course_name = course_name
        self.individual_assignments = individual_assignments
        self.skipped_assignments = []
        self.tolerance = tolerance # 0, 1, 2, or 3
        self.table_formatting = table_formatting
        self.strings_matter = strings_matter
        self.input_file = input_file
        if not input_file == "":
            contents = Utilities.read_file(input_file)
            Utilities.write_file(self.get_input_file_path(), contents, "w")
            self.input_file = self.get_input_file_path()

    def get_assignment_folder_path(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + self.course_name + "/" + self.name + "/"

    def get_rubric_file_path(self):
        return self.get_assignment_folder_path() + self.name + "_rubric.txt"
    
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
        return Utilities.get_full_dir_path() + "/../../resources/" + self.course_name + "/" + "students.txt"


