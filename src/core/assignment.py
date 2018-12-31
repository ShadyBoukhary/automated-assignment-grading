from utils.utilities import Utilities

class Assignment:

    def __init__(self, repo_name, course_name, individual_assignments):
        self.repo_name = repo_name
        self.course_name = course_name
        self.individual_assignments = individual_assignments
        self.skipped_assignments = []

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

