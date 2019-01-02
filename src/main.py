import os
import sys
import json
from git.exc import GitCommandError
import data.report.report_generator as report_generator
from core.assignment import Assignment
from core.individual_assignment import IndividualAssignment
from core.student import Student
from data.data_service.data_service import DataService
from utils.constants import Constants
from utils.utilities import Utilities


def load_students(assignment):

    print("Retrieving student data...")
    data_service = DataService()
    return data_service.load_students(assignment)

def grade_assignment(rubric_file_contents, assignment_file_contents, individual_assignment, assignment):
    """Grades an assignment

    Grades an assignment based on a comparison between the rubric output and the student
    output. If the outputs match, a grade of 100 is assigned. If the outputs do not match,
    grades are deducted per line depending on the weight of each line.
    
    Args:
        rubric_file_contents (str): The output of the rubric file
        assignment_file_contents (str): The output of the student file
        individual_assignment (IndividualAssignment): The student's assignment being evaluated
        assignment (Assignment): The course assignment

    Returns:
        IndividualAssignment: The updated student's assignment

    """

    if rubric_file_contents == assignment_file_contents:
        print("PASSED " + u'\u2713')
    else:
        print("DID NOT PASS, attempting line-by-line evaluation...")
        split_rubric = rubric_file_contents.split('\n')
        split_assignment = assignment_file_contents.split('\n')
        length_rubric = len(split_rubric)
        length_assignment = len(split_assignment)
    
        # loop according to shortest string
        length = length_rubric if length_rubric < length_assignment else length_assignment
        line_weights = Utilities.read_file(assignment.get_weights_file_path())
        line_weights = line_weights.split()

        # check for line-by-line inequality
        for i in range(length):

            #line-by-line inequality and deduct grades
            if split_rubric[i] != split_assignment[i]:
                individual_assignment.wrong_lines.append(i + 1)
                individual_assignment.grade = individual_assignment.grade - float(line_weights[i])

        # if student output is missing some data compared to rubric output
        if length_rubric > length_assignment:
            print("Student's answer is shorter than the rubric, deducting grades of missing lines.")
            individual_assignment.grade = individual_assignment.grade - sum([float(x) if i > length_assignment - 1 else 0 for i,x in enumerate(line_weights)])
            
        elif length_rubric == length_assignment:
            print("Normal Case")
        else:
            # TODO: Figure out how to handle this situation
            print("CASE NOT HANDLED")

        print("RESULT - Wrong answers: " + str(len(individual_assignment.wrong_lines)) + " | Wrong lines: " + str(individual_assignment.wrong_lines) + " | Grade: " + str(round(individual_assignment.grade)))

    return individual_assignment


def run_assignment_executable(individual_assignment):
    """Runs executable file of an assignment and dumps the output to a file
    
    Args:
        local_repo_path (str): The path of the cloned repo on disk.
        repo_name (str): The name of the repo as cloned from Github.

    Returns:
        str: The relative path to the output file generated when executing the assignment

    """

    executable_path = individual_assignment.get_local_repo_path() + "/main" + Utilities.get_os_file_extension()

    if not Utilities.path_exists(executable_path):
        err_message = "Executable path does not exist: " + executable_path
        e = IOError(err_message)
        e.strerror = err_message
        raise e

    relative_output_path = individual_assignment.get_output_path()
    shell_command = executable_path + Constants.OUT_TO_FILE + relative_output_path
    Utilities.run_program(shell_command)

    return relative_output_path

def print_student_header(student):
    print("----------------------------------------")
    print("Student: " + student.name + " | Username: " + student.username)

def grade_assignmets(students, assignment):
    """Grade Assignments

    Loops through all students and clones, runs, and grades their assignments.
    It keeps track of all skipped assignments if one grading procedure fails.

    Args:
        students ([Student]): List of students to grade assignments for
        assignment (Assignment): Course assignment to be graded

    Returns:
        Assignment: Course assignment containing all individual assignments with results

    """

    print("Grading assignments...")
    data_service = DataService()

    # Loop through individual assignments
    for current_student in students:

        # Create and add individual assignment to list 
        print_student_header(current_student)
        individual_assignment = IndividualAssignment(assignment.repo_name, current_student, assignment.course_name)
        assignment.individual_assignments.append(individual_assignment)

        try:
            # clone the current student's assignment 
            data_service.clone_repo(current_student, assignment)
            # get output file path after running the student's program
            relative_output_path = run_assignment_executable(individual_assignment)
            # get the rubric output file contents
            rubric_file_contents = Utilities.read_file(assignment.get_rubric_file_path())
            # get the student output file contents
            assignment_file_contents = Utilities.read_file(relative_output_path)
            # grade assignment
            individual_assignment = grade_assignment(rubric_file_contents, assignment_file_contents, individual_assignment, assignment)
        except IOError as e:
            # Keep track of skipped assignments due to errors
            print(e.strerror)
            assignment.skipped_assignments.append((individual_assignment, e.strerror))

        # Handle other errors
        except GitCommandError as e:
            print("Git Error - skipping student:" + e.stderr)
            assignment.skipped_assignments.append((individual_assignment, e))


    return assignment

def get_assignments(checkFirst):
    data_service = DataService()
    try:
        if checkFirst:
            data_service.create_assignments_file()
        return data_service.get_assignments()
    except IOError:
        sys.exit("Failed to retreve assignments. Make sure that the file exists. Perhaps enter a new assignment first?")
    except json.JSONDecodeError:
        sys.exit("JSON File is corrupted. Failed to retrieve assignments")

def save_assignments(assignments):
    data_service = DataService()
    try:
        data_service.save_assignments(assignments)
        print("Assignment saved!")
    except Exception as e:
        print("ERROR: " + e)
        print("Failed to save data... Try again.")

def enter_new_assignment():
    print("--------------------------")
    course_name = input("Course name (e.g: CMPS-3410): ")
    repo_name = input("Repository name (this will be used when cloning from GitHub): ")
    confirm = "N"
    while not confirm.upper() == "Y" or confirm.upper == "N":
        confirm = input("Save assignment? (Y/n) ")
        if confirm.upper() == "Y":
            assignment = Assignment(repo_name, course_name, [])
            assignments = get_assignments(True)
            assignments.append(assignment)
            save_assignments(assignments)
            return assignment
        elif confirm.upper() == "N":
            print("Cancelled.")
            return None
        else:
            print("Try again.")

def get_assignment_to_grade():
    assignments = get_assignments(False)
    try_again = True
    print("\n--------------- Assignment Repo Names ---------------")
    for assignment in assignments:
        print(assignment.repo_name + "\n")
    print("\nEnter the name of the repo to start grading assignments")
    while try_again:
        repo_name = input()
        found = [assignment if assignment.repo_name == repo_name else None for assignment in assignments]
        if found == [] or found[0] == None:
            print("Try again.")
        else:
            try_again = False
            return found[0]


def display_menu():
    print("Enter the the number of the command.\nCTRL-C to exit.\n")
    print("1. " + "Grade an Assignments.")
    print("2. " + "Enter a new assignment.")

def get_menu_option():
    valid = False 
    while not valid:
        try:
            val = int(input())
            valid = True
            return val
        except ValueError:
            print("Must be an integer.")

def grade_option_selected():
    assignment = get_assignment_to_grade()
    students = load_students(assignment)
    assignment = grade_assignmets(students, assignment)
    report_generator.generate_report(assignment)
    
def main():
    display_menu()
    option = get_menu_option()
    while option < 3:
        grade_option_selected() if option == 1 else enter_new_assignment()
        print("\n")
        display_menu()
        option = get_menu_option()

main()
