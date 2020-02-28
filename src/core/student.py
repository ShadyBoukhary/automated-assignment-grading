from utils.utilities import Utilities

class Student(dict):
    def __init__(self, firstName, lastName, username, repo):
        self.name = firstName + " " + lastName
        self.username = username
        self.repo = repo

    @classmethod
    def from_json(cls, data):
        name = data['name'].split()
        return cls(name[0], name[1], data['username'], data['repo'])

    def to_dict(self):
        return self.__dict__
        
    def get_assignment_path(self, individual_assignment):
        return individual_assignment.get_local_repo_path() + "/" + individual_assignment.name + "/"