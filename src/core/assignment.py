from utils.utilities import Utilities

class Assignment(dict):

    def __init__(self, repo_name, course_name, individual_assignments, tolerance = 0, table_formatting = False, strings_matter = True):
        self.repo_name = repo_name
        self.course_name = course_name
        self.individual_assignments = individual_assignments
        self.skipped_assignments = []
        self.tolerance = tolerance # 0, 1, 2, or 3
        self.table_formatting = table_formatting
        self.strings_matter = strings_matter

    def get_assignment_folder_path(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + self.course_name + "/" + self.repo_name + "/"

    def get_rubric_file_path(self):
        return self.get_assignment_folder_path() + self.repo_name + "_rubric.txt"
    
    def get_weights_file_path(self):
        return self.get_assignment_folder_path() + self.repo_name + "_weights.txt"

    def get_reports_dir_path(self):
        path = Utilities.get_full_dir_path() + "/../../reports/" + self.course_name + "/"
        if not Utilities.path_exists(path):
            Utilities.create_dir(path)
        return path

    def get_students_file_path(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + self.course_name + "/" + "students.txt"


