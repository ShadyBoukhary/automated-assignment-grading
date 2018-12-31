import sys

import requests
from git import Repo
from git.exc import GitError

from utils.constants import Constants
from utils.utilities import Utilities
from core.student import Student


class DataService:

    def load_students(self, assignment):
        try:
            contents = Utilities.read_file(assignment.get_students_file_path())
            return [Student(s.split()[0] + " " + s.split()[1], s.split()[2]) for s in contents.splitlines()]
        except:
            print()
            sys.exit("Could not read students file. Please make sure the following file exists: "+ assignment.get_students_file_path())

    
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
                print(e)
                raise e
