import os
import sys
from utils.utilities import Utilities 
from utils.constants import Constants

from data_service.data_service import DataService
 
def main():
    rubric_file_contents = Utilities.read_file("../resources/hello.txt")
    assignment_file_contents = Utilities.read_file("../resources/hello_assignment.txt")
    print(rubric_file_contents)
    print(assignment_file_contents)

    if rubric_file_contents == assignment_file_contents:
        print("Pass")
    else:
        print("No Pass")

    full_executable_path = os.path.realpath(__file__)
    full_dir_path = os.path.dirname(full_executable_path)
    print(full_dir_path)

    Utilities.run_program(full_dir_path + "/../tests/cpp/hello_world/main" + Utilities.get_os_file_extension() + Constants.OUT_TO_FILE + "../resources/hello_answers1.txt")
    data_service = DataService()
    #data_service.get_user_repos("shadyboukhary")
    data_service.clone_repo("Shady Boukhary", "Ionic-3-Tutorial", "CMPS-3410")
    Utilities.get_home_directory()

main()
