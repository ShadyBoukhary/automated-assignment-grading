import os
import sys
from utils.utilities import Utilities 
from utils.constants import Constants

from data_service.data_service import DataService
 
def main():
    
    data_service = DataService()
    repo_name = "test-cpp"
    
    #data_service.get_user_repos("shadyboukhary")
    local_repo_path = data_service.clone_repo("Shady Boukhary", repo_name, "CMPS-3410")

    executable_path = local_repo_path+ "/main" + Utilities.get_os_file_extension()
    relative_output_path = "../resources/" + repo_name + "_boukhary.txt"
    shell_command = executable_path + Constants.OUT_TO_FILE + relative_output_path
    Utilities.run_program(shell_command)


    rubric_file_contents = Utilities.read_file("../resources/hello.txt")
    assignment_file_contents = Utilities.read_file(relative_output_path)
    print(rubric_file_contents)
    print(assignment_file_contents)

    if rubric_file_contents == assignment_file_contents:
        print("PASSED")
    else:
        print("DID NOT PASS, attempting line-by-line evaluation...")

        split_rubric = rubric_file_contents.split()
        split_assignment = assignment_file_contents.split()
        length_rubric = len(split_rubric)
        length_assignment = len(split_assignment)
        length = length_rubric if length_rubric < length_assignment else length_assignment

        wrong_lines = []
        # check for line-by-line inequality
        for i in range(length):
            print(split_rubric[i] + " VS " + split_assignment[i])
            if split_rubric[i] != split_assignment[i]:
                wrong_lines.append(i + 1)

        print("RESULT - Wrong answers: " + str(len(wrong_lines)) + "| Wrong lines: " + str(wrong_lines))



main()
