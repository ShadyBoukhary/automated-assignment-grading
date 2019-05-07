from utils.utilities import Utilities
class Student:
    def __init__(self, name, username, repo):
        self.name = name
        self.username = username
        self.repo = repo

    def get_assignment_path(self, individual_assignment):
        return individual_assignment.get_local_repo_path() + "/" + individual_assignment.name + "/"