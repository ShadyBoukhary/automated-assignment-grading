from utils.utilities import Utilities

class Assignment:

    def __init__(self, repo_name, course_name, individual_assignments):
        self.repo_name = repo_name
        self.course_name = course_name
        self.individual_assignments = individual_assignments
        self.skipped_assignments = []

    def get_rubric_file_path(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + self.repo_name + "_rubric.txt"
    
    def get_weights_file_path(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + self.repo_name + "_weights.txt"