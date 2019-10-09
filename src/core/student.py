from utils.utilities import Utilities

class Student(dict):
    def __init__(self, name, username, repo):
        self.name = name
        self.username = username
        self.repo = repo

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_dict(self):
        return self.__dict__
        
    def get_assignment_path(self, individual_assignment):
        return individual_assignment.get_local_repo_path() + "/" + individual_assignment.name + "/"