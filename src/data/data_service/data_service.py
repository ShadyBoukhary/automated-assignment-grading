import sys

import requests
from git import Repo
from git.exc import GitError
import json

from utils.constants import Constants
from utils.utilities import Utilities
from core.student import Student
from core.assignment import Assignment
from core.individual_assignment import IndividualAssignment


class DataService:

    def load_students(self, assignment):
        try:
            contents = Utilities.read_file(assignment.get_students_file_path())
            return [Student(s.split()[0] + " " + s.split()[1], s.split()[2]) for s in contents.splitlines()]
        except:
            print()
            sys.exit("Could not read students file. Please make sure the following file exists: "+ assignment.get_students_file_path())

    

    def get_assignments(self):
    
        try:
            assignment_dicts =  Utilities.json_deserialize(Utilities.get_assignment_data_file_path())

            if assignment_dicts[0] == {}:
                return []
            # convert list of dict containing an assignment into list of Assignment objects
            return [Assignment(a_dict["repo_name"], a_dict["course_name"], 
            [IndividualAssignment(i_dict["repo_name"],
            Student(i_dict["student"]["name"], i_dict["student"]["username"]),
            i_dict["course_name"]) 
            for i_dict in a_dict["individual_assignments"]]) 
            for a_dict in assignment_dicts]

        except json.JSONDecodeError:
            print("No assignments found or file is corrupted.")
            return []

    # def assignments_dict_to_object(assignment_dicts):
    #     return

    def save_assignments(self, assignments):
        """Saves all assignments to a JSON file

        Args:
            assignments ([Assignment]): the list of assignments to save

        Raises:
            JSONDecoderError
        """

        try:
            Utilities.json_serialize(Utilities.get_assignment_data_file_path(), [assignment.__dict__ for assignment in assignments])
        except json.JSONDecodeError as e:
            raise e

    def clone_repo(self, current_student, assignment):
        """Clones a github repo for a specific username into a specific directory
        
        Args:
            current_student (Student): The student to clone the repo for
            assignment (Assignment): The assignment being cloned
        
        """

        #username = Constants.USERS_USERNAMES_MAP[name]
        repo = "/" + assignment.repo_name
        path_to_clone_to = Utilities.get_home_directory() + Constants.CLONE_DIRECTORY + "/" + assignment.course_name + repo + "/" + current_student.username
        path_to_clone_from = Constants.BASE_URL + current_student.username  + repo + ".git"

        if Utilities.path_exists(path_to_clone_to):
            print("Path Exists for username: " + current_student.username  + ", Repo: " + assignment.repo_name + ", Pulling instead...")
            local_repo = Repo(path_to_clone_to)
            local_repo.remotes.origin.pull()
        else:
            print("Cloning " + path_to_clone_from + " to " + path_to_clone_to)
            try:
                Repo.clone_from(path_to_clone_from, path_to_clone_to)

            except GitError as e:
                raise e


    def create_assignments_file(self):
        """ Creates the file containing the assignments if it does not exist"""

        if not Utilities.path_exists(Utilities.get_assignment_data_file_path()):
            open(Utilities.get_assignment_data_file_path(), 'a').close()

