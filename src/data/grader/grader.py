import json
import os
import sys
import re
import Levenshtein as lev

from git.exc import GitCommandError
from autocorrect import spell
import data.grader.source_analyzer as source_analyzer
import data.report.report_generator as report_generator
from core.assignment import Assignment
from core.individual_assignment import IndividualAssignment
from core.student import Student
from custom.compilation_exception import CompilationException
from data.data_service.data_service import DataService
from utils.constants import Constants
from utils.utilities import Utilities


def load_students(assignment):
    """Loads all students from disk for an assignment

    Args:
        (Assignment): the assignment to retrieve students for

    Returns:
        ([Student]): list of students for that assignment
        
    """

    Utilities.log("Retrieving student data... ", True)
    data_service = DataService()
    students = data_service.load_students(assignment)
    Utilities.log(Constants.CHECK_MARK)
    return students

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

    Utilities.log("Initial equality check... ", True)
    Utilities.flush()
    if rubric_file_contents == assignment_file_contents:
        Utilities.log(Constants.CHECK_MARK)
    else:
        Utilities.log(Constants.CROSS_MARK + "\n" + "attempting line-by-line evaluation...")
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
            if not equal_lines(split_rubric[i], split_assignment[i], assignment):
                individual_assignment.wrong_lines.append(i + 1)
                try:
                    individual_assignment.grade = individual_assignment.grade - float(line_weights[i])
                except IndexError:
                    sys.exit("The Weights file is misconfigured. It might be shorter than the rubric. Cannot grade until fixed.")

        # if student output is missing some data compared to rubric output
        if length_rubric > length_assignment:
            Utilities.log("Student's answer is shorter than the rubric, deducting grades of missing lines.")
            individual_assignment.grade = individual_assignment.grade - sum([float(x) if i > length_assignment - 1 else 0 for i,x in enumerate(line_weights)])
            
        #elif length_rubric == length_assignment:
            #Utilities.log("Normal Case")
        # else:
        #     # TODO: Figure out how to handle this situation
        #     Utilities.log("CASE NOT HANDLED")

    return individual_assignment

def equal_lines(rubric_line, student_line, assignment):
    """Compares 1 line in the key to 1 line in the student output
    
    The comparison takes into account precision issues for numbers, ASCII table formatting,
    and strings that simply discribe the output but are not a part of the solution itself.

    The algorithm uses the tolerance within the assignment to determine how many significant
    digits to consider when comparing floats. If strings do not matter in the solution (i.e. 
    strings merely describe the output but are not a part of the solution), strings are ignored
    and numbers are extracted from the output instead. In addition, if the assignment includes
    some table formatting, special characters are filtered out of the output to prevent issues
    when comparing solutions with slightly different table formatting.

    Args:
        rubric_line (String): the line in the key to be evaluated against
        student_line (String): the line in the student output being evaluated
        assignment (Assignment): the current course assignment being evaluated

    Returns:
        (boolean): whether the lines are considered equal by the above standards
    
    """

    # find tolerance
    tolerance = 1e-09
    if assignment.tolerance == 1:
        tolerance = 1e-06
    elif assignment.tolerance == 2:
        tolerance= 1e-03
    elif assignment.tolerance == 3:
        tolerance = 1e-01

    # remove table characters if table formatting is enabled
    if assignment.table_formatting:
        rubric_line = re.sub(r"[^a-zA-Z0-9]+", lambda x: '.' if x.group() == '.' else ' ', rubric_line)
        student_line = re.sub(r"[^a-zA-Z0-9]+", lambda x: '.' if x.group() == '.' else ' ', student_line)

    # split result by spaces
    rubric_split = rubric_line.split()
    student_split = student_line.split()

    # if strings don't matter, extract and compare the numbers using the above tolerance
    if not assignment.strings_matter:
        # remove non-numbers
        rubric_line = ' '.join([word for word in rubric_line.split() if Utilities.is_number(word)])
        student_line = ' '.join([word for word in student_line.split() if Utilities.is_number(word)])

        # loop over remaining numbers after splitting
        for i in range(len(rubric_split)):
            if (Utilities.is_number(rubric_split[i])):
                if not Utilities.is_close(float(rubric_split[i]), float(student_split[i]), tolerance):
                    return False
            else:
                if not rubric_split[i] == student_split[i]:
                    return False
        return True

    else:
        for i in range(len(rubric_split)):

            if not Utilities.is_number(rubric_split[i]):
                if not words_hash_is_equal(rubric_split[i], student_split[i]):
                    return False
            else:
                if not Utilities.is_close(float(rubric_split[i]), float(student_split[i]), tolerance):
                    return False
        return True

def words_hash_is_equal(rubric, student):
    return spell(rubric) == spell(student) or lev.distance(rubric, student)< Constants.LEVENSHTEIN_DISTANCE

def run_assignment_executable(individual_assignment):
    """Runs executable file of an assignment and dumps the output to a file
    
    Args:
        individual_assignment (IndividualAssignment): student assignment to execute

    Returns:
        str: The relative path to the output file generated when executing the assignment

    """

    executable_path = individual_assignment.get_compile_output_dir() + "/main" + Utilities.get_os_file_extension()

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
    Utilities.log("-------------------------------------------------------------------------------")
    Utilities.log("Student: " + student.name + " | Username: " + student.username)

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

    Utilities.log("Grading assignments...")
    data_service = DataService()

    # Loop through individual assignments
    for current_student in students:

        # Create and add individual assignment to list 
        print_student_header(current_student)
        individual_assignment = IndividualAssignment(assignment.name, current_student, assignment.course_name)
        assignment.individual_assignments.append(individual_assignment)

        try:
            # clone the current student's assignment 
            data_service.clone_repo(current_student, assignment)
            # check if the source compiles at all
            source_report = source_analyzer.analyze_source(current_student.get_assignment_path(individual_assignment) + "main.cpp", assignment, individual_assignment)
            # get output file path after running the student's program
            relative_output_path = run_assignment_executable(individual_assignment)
            # get the rubric output file contents
            rubric_file_contents = Utilities.read_file(assignment.get_rubric_file_path())
            # get the student output file contents
            assignment_file_contents = Utilities.read_file(relative_output_path)
            # grade assignment
            individual_assignment = grade_assignment(rubric_file_contents, assignment_file_contents, individual_assignment, assignment)
            # copy source report to individual assignment
            individual_assignment.source_report = source_report

        except IOError as e:
            # Keep track of skipped assignments due to errors
            Utilities.log(e.strerror)
            assignment.skipped_assignments.append((individual_assignment, e.strerror))

        # Handle other errors
        except GitCommandError as e:
            Utilities.log("Git Error - skipping student:" + e.stderr)
            assignment.skipped_assignments.append((individual_assignment, e))

        except CompilationException as e:
            Utilities.log(e.message)
            # TODO decide how much to deduct exactly
            individual_assignment.grade = 0

        finally:
            strr = " | Functions: " + str(len(individual_assignment.source_report.functions)) if not individual_assignment.source_report == None else ""
            Utilities.log("RESULT - Wrong answers: " + str(len(individual_assignment.wrong_lines)) + " | Wrong lines: " + str(individual_assignment.wrong_lines) + " | Grade: " + str(round(individual_assignment.grade)) + strr)

    return assignment

def get_assignments(checkFirst):
    """Gets all assignments from disk 
    
    Args:
        checkFirst (boolean): Flag indicating whether to check if the assignment file exists

    Returns:
        ([Assignment]): list of assignments

    """
    data_service = DataService()
    try:
        if checkFirst:
            data_service.create_assignments_file()
        return data_service.get_assignments()
    except IOError:
        sys.exit("Failed to retrieve assignments. Make sure that the file exists. Perhaps enter a new assignment first?")
    except json.JSONDecodeError:
        sys.exit("JSON File is corrupted. Failed to retrieve assignments")

def save_assignments(assignments):
    """Saves assignmetns on disk """
    
    data_service = DataService()
    try:
        data_service.save_assignments(assignments)
        Utilities.log("Assignment saved!")
    except Exception as e:
        Utilities.log("ERROR: " + e)
        Utilities.log("Failed to save data... Try again.")

def enter_new_assignment():
    """Prompts the user to enter a new assignment
    
    Returns:
        (Assignment): The newly created assignment

    """
    Utilities.log("--------------------------")
    course_name = input("Course name (e.g: CMPS-3410): ")
    name = input("The name of the assignment (should be a folder in student repositories): ")
    confirm = "N"
    while not confirm.upper() == "Y" or confirm.upper == "N":
        confirm = input("Save assignment? (Y/n) ")
        if confirm.upper() == "Y":
            assignment = Assignment(name, course_name, [])
            assignments = get_assignments(True)
            assignments.append(assignment)
            save_assignments(assignments)
            return assignment
        elif confirm.upper() == "N":
            Utilities.log("Cancelled.")
            return None
        else:
            Utilities.log("Try again.")

def get_assignment_to_grade():
    """Retrieves an assignment to grade
    
    Returns:
        (Assignment): the assignment to grade

     """

    assignments = get_assignments(False)
    try_again = True
    Utilities.log("\n--------------- Assignment Repo Names ---------------")
    for assignment in assignments:
        Utilities.log(assignment.name + "\n")
    Utilities.log("\nEnter the name of the repo to start grading assignments")
    while try_again:
        name = input()
        found = [assignment if assignment.name == name else None for assignment in assignments]
        if found == [] or found[0] == None:
            Utilities.log("Try again.")
        else:
            try_again = False
            return found[0]

def grade():
    """Grades an assignment for all students and generates a report """

    assignment = get_assignment_to_grade()
    students = load_students(assignment)
    assignment = grade_assignmets(students, assignment)
    report_generator.generate_report(assignment)
