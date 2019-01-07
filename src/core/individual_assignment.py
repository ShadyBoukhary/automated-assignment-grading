from utils.utilities import Utilities
from utils.constants import Constants

class IndividualAssignment:

    def __init__(self, repo_name, student, course_name):
        self.repo_name = repo_name
        self.student = student
        self.course_name = course_name
        self.grade = 100
        self.wrong_lines = []
        
    def get_local_repo_path(self):
        return Utilities.get_home_directory() + Constants.CLONE_DIRECTORY + "/" + self.course_name + "/" + self.repo_name + "/" + self.student.username

    def get_output_path(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + self.course_name + "/" + self.repo_name + "/" + self.repo_name +  "_" + self.student.username + ".txt"
    
    def get_compile_output_dir(self):
        return Utilities.get_full_dir_path() + "/../../resources/" + self.course_name + "/" + self.repo_name + "/" + "compile-temp/"
    
    def get_compile_output_path(self):
        return self.get_compile_output_dir() + self.repo_name +  "_" + self.student.username + ".txt"