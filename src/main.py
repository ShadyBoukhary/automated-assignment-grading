import os
import sys

from core.assignment import Assignment
from core.individual_assignment import IndividualAssignment
from core.student import Student
from data_service.data_service import DataService
from utils.constants import Constants
from utils.utilities import Utilities


def grade_assignment(rubric_file_contents, assignment_file_contents, individual_assignment):
    """Grades an assignment

    Grades an assignment based on a comparison between the rubric output and the student
    output. If the outputs match, a grade of 100 is assigned. If the outputs do not match,
    grades are deducted per line depending on the weight of each line.
    
    Args:
        rubric_file_contents (str): The output of the rubric file
        assignment_file_contents (str): The output of the student file
        individual_assignment (IndividualAssignment): The student's assignment being evaluated

    Returns:
        IndividualAssignment: The updated student's assignment

    """

    grade = 100
    if rubric_file_contents == assignment_file_contents:
        print("PASSED " + u'\u2713')
    else:
        print("DID NOT PASS, attempting line-by-line evaluation...")
        #print(rubric_file_contents)
        split_rubric = rubric_file_contents.split('\n')
        split_assignment = assignment_file_contents.split('\n')
        length_rubric = len(split_rubric)
        length_assignment = len(split_assignment)
    
        # loop according to shortest string
        #print(split_rubric)
        #print(split_assignment)
        length = length_rubric if length_rubric < length_assignment else length_assignment
        line_weights = Utilities.read_file(individual_assignment.get_weights_file_path())
        line_weights = line_weights.split()
        wrong_lines = []
        # check for line-by-line inequality
        #print(length)
        for i in range(length):
            #print(split_rubric[i] + " VS " + split_assignment[i])
            #print(i)
            if split_rubric[i] != split_assignment[i]:
                wrong_lines.append(i + 1)
                grade = grade - float(line_weights[i])

        if length_rubric > length_assignment:
            print("Student's answer is shorter than the rubric, deducting grades of missing lines.")
            grade = grade - sum([float(x) if i > length_assignment - 1 else 0 for i,x in enumerate(line_weights)])
            
        else:
            # TODO: Figure out how to handle this situation
            print("CASE NOT HANDLED")

        print("RESULT - Wrong answers: " + str(len(wrong_lines)) + " | Wrong lines: " + str(wrong_lines) + " | Grade: " + str(round(grade)))



def run_assignment_executable(individual_assignment):
    """Runs executable file of an assignment and dumps the output to a file
    
    Args:
        local_repo_path (str): The path of the cloned repo on disk.
        repo_name (str): The name of the repo as cloned from Github.

    Returns:
        str: The relative path to the output file generated when executing the assignment

    """

    executable_path = individual_assignment.get_local_repo_path() + "/main" + Utilities.get_os_file_extension()
    relative_output_path = individual_assignment.get_output_path()
    shell_command = executable_path + Constants.OUT_TO_FILE + relative_output_path
    Utilities.run_program(shell_command)
    return relative_output_path

def main():
    
    data_service = DataService()
    repo_name = "test-cpp"
    skipped_assignments = []
    current_student = Student("Shady Boukhary", "shadyboukhary")
    assignment = Assignment(repo_name, "CMPS-3410", [current_student])
    individual_assignment = IndividualAssignment(assignment.repo_name, current_student, assignment.course_name)
    #data_service.get_user_repos("shadyboukhary")
    data_service.clone_repo(current_student, assignment)

    relative_output_path = run_assignment_executable(individual_assignment)


    try:
        rubric_file_contents = Utilities.read_file(assignment.get_rubric_file_path())
        assignment_file_contents = Utilities.read_file(relative_output_path)
        #print(rubric_file_contents)
        #print(assignment_file_contents)
        grade_assignment(rubric_file_contents, assignment_file_contents, assignment)
    except IOError as e:
        # Keep track of skipped assignments due to errors
        skipped_assignments.append((individual_assignment, e.strerror))
    

    
    



main()
