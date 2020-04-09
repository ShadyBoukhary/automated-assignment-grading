import sys

from git import Repo
from git.exc import GitError
import json

from utils.constants import Constants
from utils.utilities import Utilities
from core.student import Student
from core.assignment import Assignment
from custom.deletion_exception import DeletionException
from custom.assignment_exception import AssignmentException
from pprint import pprint


class DataService:

    @staticmethod
    def load_students(assignment):
        """Retrieves students for an assignment from a file on disk"""

        try:
            student_dicts = \
                Utilities.json_deserialize(assignment.get_students_file_path())
            students = []

            for s_dict in student_dicts:
                firstName = s_dict['firstName']
                lastName = s_dict['lastName']
                username = s_dict['username']
                repo = f"{assignment.course_name}-{username}"
                students.append(Student(firstName, lastName, username, repo))

            return students
        except Exception as e:
            print(e)
            print(Constants.CROSS_MARK)
            sys.exit("Could not read students file. Please make sure the \
                following file exists: " + assignment.get_students_file_path())

    @staticmethod
    def get_assignments():
        """Retrieves assignments from json file. Converts the dict \
            retrieved to a list of assignments """

        try:
            assignment_dicts = Utilities.json_deserialize(Utilities.get_assignment_data_file_path())
            if assignment_dicts == [] or assignment_dicts is None:
                return []
            # convert list of dict containing an assignment into
            #  list of Assignment objects
            return [Assignment.from_json(a_dict)
                    for a_dict in assignment_dicts]

        except json.JSONDecodeError:
            return []

    # def assignments_dict_to_object(assignment_dicts):
    #     return
    @staticmethod
    def save_assignments(assignments):
        """Saves all assignments to a JSON file

        Args:
            assignments ([Assignment]): the list of assignments to save

        Raises:
            JSONDecoderError
        """

        try:
            Utilities.json_serialize(
                Utilities.get_assignment_data_file_path(), assignments)
        except json.JSONDecodeError as e:
            raise e

    @staticmethod
    def clone_repo(current_student, assignment):
        """Clones a github repo for a specific username into a specific directory

        Args:
            current_student (Student): The student to clone the repo for
            assignment (Assignment): The assignment being cloned

        """

        path_to_clone_to = assignment.get_clone_path() + Utilities.construct_repo_path(current_student)

        path_to_clone_from = Constants.BASE_URL + \
            current_student.username + "/" + current_student.repo + ".git"

        try:

            if Utilities.path_exists(path_to_clone_to):
                Utilities.Debug("Path Exists for username: " +
                                current_student.username +
                                ", Repo: " + assignment.name
                                + ", Pulling instead... ")
                local_repo = Repo(path_to_clone_to)
                local_repo.remotes.origin.pull()
                Utilities.Debug(Constants.CHECK_MARK)
            else:
                Utilities.Debug("Cloning " + path_to_clone_from +
                                " to " + path_to_clone_to + "... ")

                Repo.clone_from(path_to_clone_from, path_to_clone_to)
        except GitError as e:
            raise e

    @staticmethod
    def create_assignments_file():
        """ Creates the file containing the assignments if it does not exist"""

        if not Utilities \
                .path_exists(Utilities.get_assignment_data_file_path()):
            open(Utilities.get_assignment_data_file_path(), 'a').close()

    @staticmethod
    def create_assignment(assignment):
        '''Appends new assignment'''

        DataService.create_assignments_file()
        assignments = DataService.get_assignments()
        assignments.append(assignment)
        DataService.save_assignments(assignments)

    @staticmethod
    def assignment_exists(course_name, assignment_name):
        '''Checks if an assignment exists'''
        DataService.create_assignments_file()
        assignments = DataService.get_assignments()
        idx = DataService.search_assignments(course_name, assignment_name, assignments)

        if idx < 0:
            return False
        return True

    @staticmethod
    def delete_assignment(course_name, assignment_name):
        DataService.create_assignments_file()
        assignments = DataService.get_assignments()
        idx = DataService.search_assignments(course_name, assignment_name, assignments)

        if idx < 0:
            raise DeletionException(f'Assignment {assignment_name} in course {course_name} does not exist')

        deleted_assignment = assignments.pop(idx)
        DataService.save_assignments(assignments)
        Utilities.delete_dir_recur(deleted_assignment.get_assignment_folder_path())

    def search_assignments(course_name, assignment_name, assignments):
        for i, assignment in enumerate(assignments):
            if assignment.name == assignment_name and assignment.course_name == course_name:
                return i
        return -1

    def get_assignment_and_assignments(course_name, assignment_name):
        assignments = DataService.get_assignments()
        idx = DataService.search_assignments(course_name, assignment_name, assignments)
        if idx < 0:
            raise AssignmentException(f'Assignment {assignment_name} in course {course_name} does not exist')

        return assignments[idx], assignments

