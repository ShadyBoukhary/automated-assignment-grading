import sys

import requests
from git import Repo

from utils.constants import Constants
from utils.utilities import Utilities


class DataService:
    
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
            Repo.clone_from(path_to_clone_from, path_to_clone_to)
