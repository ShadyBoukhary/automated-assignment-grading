from utils.constants import Constants
import requests
import sys
from utils.utilities import Utilities
from git import Repo

class DataService:
    
    def get_user_repos(self, username):

        url = Constants.BASE_URL + Constants.USERS_URL + "/" + username + Constants.REPOS_URL
        response = requests.get(url)

        print(response.content)

        # Print the status code of the response.
        if response.status_code == 200:
            return response.content
        else:
            print("ERROR: API CALL ERROR")
            print(response.status_code)
            sys.exit()

    def clone_repo(self, name, reponame, classname):
        """Clones a github repo for a specific username into a specific directory"""

        username = Constants.USERS_USERNAMES_MAP[name]
        repo = "/" + reponame
        path_to_clone_to = Utilities.get_home_directory() + Constants.CLONE_DIRECTORY + "/" + classname + repo + "/" + username
        path_to_clone_from = Constants.BASE_URL + username  + repo + ".git"

        if Utilities.path_exists(path_to_clone_to):
            print("Path Exists for username: " + username + ", Repo: " + reponame + ", Pulling instead...")
            local_repo = Repo(path_to_clone_to)
            local_repo.remotes.origin.pull()
        else:
            print("Cloning " + path_to_clone_from + " to " + path_to_clone_to)
            Repo.clone_from(path_to_clone_from, path_to_clone_to)