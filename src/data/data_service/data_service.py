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
        """Retrieves students for an assignment from a file on disk"""
        
        try:
            student_dicts = Utilities.json_deserialize(assignment.get_students_file_path())
            print(student_dicts)
            students = []

            for s_dict in student_dicts:
                firstName = s_dict['firstName']
                lastName = s_dict['lastName']
                username = s_dict['username']
                repo = f"{assignment.course_name}-{username}"
                students.append(Student(firstName, lastName, username, repo))
            #return [Student.from_json(s_dict) for s_dict in student_dicts]
            return students
        except Exception as e:
            print(e)
            print(Constants.CROSS_MARK)
            sys.exit("Could not read students file. Please make sure the following file exists: "+ assignment.get_students_file_path())

    

    def get_assignments(self):
        """Retrieves assignments from json file. Converts the dict retrieved to a list of assignments """

        try:
            assignment_dicts =  Utilities.json_deserialize(Utilities.get_assignment_data_file_path())

            if assignment_dicts[0] == {}:
                return []
            # convert list of dict containing an assignment into list of Assignment objects
            return [Assignment.from_json(a_dict) for a_dict in assignment_dicts]

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
            Utilities.json_serialize(Utilities.get_assignment_data_file_path(), assignments)
        except json.JSONDecodeError as e:
            raise e

    def clone_repo(self, current_student, assignment):
        """Clones a github repo for a specific username into a specific directory
        
        Args:
            current_student (Student): The student to clone the repo for
            assignment (Assignment): The assignment being cloned
        
        """

        #path_to_clone_to = Utilities.get_home_directory() + Constants.CLONE_DIRECTORY + "/" + assignment.course_name + repo + "/" + current_student.username
        path_to_clone_to = Utilities.get_home_directory() + Constants.CLONE_DIRECTORY + "/" + Utilities.construct_repo_path(assignment, current_student)

        path_to_clone_from = Constants.BASE_URL + current_student.username  + "/" + current_student.repo + ".git"

        try:

            if Utilities.path_exists(path_to_clone_to):
                Utilities.log("Path Exists for username: " + current_student.username  + ", Repo: " + assignment.name + ", Pulling instead... ", True)
                Utilities.flush()
                local_repo = Repo(path_to_clone_to)
                local_repo.remotes.origin.pull()
                Utilities.log(Constants.CHECK_MARK)
            else:
                Utilities.log("Cloning " + path_to_clone_from + " to " + path_to_clone_to + "... ", True)
                Utilities.flush()

                Repo.clone_from(path_to_clone_from, path_to_clone_to)
                Utilities.log(Constants.CHECK_MARK)
        except GitError as e:
            Utilities.log(Constants.CROSS_MARK)
            raise e


    def create_assignments_file(self):
        """ Creates the file containing the assignments if it does not exist"""

        if not Utilities.path_exists(Utilities.get_assignment_data_file_path()):
            open(Utilities.get_assignment_data_file_path(), 'a').close()

