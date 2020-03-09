import json
import sys
import re
import Levenshtein as lev
from git.exc import GitCommandError
from autocorrect import spell
import data.grader.source_analyzer as source_analyzer
import data.report.report_generator as report_generator
from custom.compilation_exception import CompilationException
from core.assignment import Assignment
from core.individual_assignment import IndividualAssignment
from data.data_service.data_service import DataService
from utils.constants import Constants
from utils.utilities import Utilities
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from custom.runtime_exception import RuntimeException


def load_students(assignment):
    """Loads all students from disk for an assignment

    Args:
        (Assignment): the assignment to retrieve students for

    Returns:
        ([Student]): list of students for that assignment

    """

    Utilities.log("Retrieving student data... ", True)
    students = DataService.load_students(assignment)
    Utilities.log(Constants.CHECK_MARK)
    return students


def deduct_grade(individual_assignment, deduction):
    try:
        individual_assignment.grade = individual_assignment.grade - \
            float(deduction)
    except IndexError:
        sys.exit(
            "The Weights file is misconfigured. They have to be numbers. \
                 Cannot grade until fixed.")


def grade_assignment(rubric_file_dicts, assignment_file_contents, ia, a):
    """Grades an assignment

    Grades an assignment based on a comparison between the rubric
    output and the student
    output. If the outputs match, a grade of 100 is assigned.
    If the outputs do not match,
    grades are deducted per line depending on the weight of each line.

    Args:
        rubric_file_contents (str): The output of the rubric file
        assignment_file_contents (str): The output of the student file
        individual_assignment (IndividualAssignment): The student's
        assignment being evaluated
        assignment (Assignment): The course assignment

    Returns:
        IndividualAssignment: The updated student's assignment

    """
    individual_assignment = ia
    assignment = a
    # find tolerance
    tolerance = 1e-09
    if assignment.tolerance == 1:
        tolerance = 1e-06
    elif assignment.tolerance == 2:
        tolerance = 1e-03
    elif assignment.tolerance == 3:
        tolerance = 1e-01

    for rubric_dict in rubric_file_dicts:
        is_wrong = False
        k = rubric_dict["key"]
        v = rubric_dict["value"]
        w = rubric_dict["weight"]
        regex = Constants.RUBRIC_REGEX.replace("REPLACE", k)
        matches = re.search(regex, assignment_file_contents)
        if matches:
            match = matches.group(2)

            # If the value being graded is a number,
            # see if it is close to the rubric
            if Utilities.is_number(match):
                if not Utilities.is_close(float(v), float(match), tolerance):
                    is_wrong = True
            else:
                if not words_hash_is_equal(v, match):
                    is_wrong = True

        else:
            # no match was found
            is_wrong = True
        if is_wrong:
            deduct_grade(individual_assignment, w)
            if not matches:
                individual_assignment.wrong_lines.append(
                    {'key': k, 'value': "Not found", 'correct': v})
            else:
                individual_assignment.wrong_lines.append(
                    {'key': k, 'value': matches.group(2)
                        if match else "Not found", 'correct': v})

    return individual_assignment


def words_hash_is_equal(rubric, student):
    return spell(rubric) == spell(student) \
         or lev.distance(rubric, student) < Constants.LEVENSHTEIN_DISTANCE


def run_assignment_executable(individual_assignment, assignment):
    """Runs executable file of an assignment and dumps the output to a file

    Args:
        individual_assignment (IndividualAssignment): student
                            assignment to execute

    Returns:
        str: The relative path to the output file generated
            when executing the assignment

    """

    executable_path = \
        individual_assignment.get_compile_output_dir() + "main" + \
        Utilities.get_os_file_extension()
    additional_args = " 2> " + \
        individual_assignment.get_runtime_error_output_path()

    if not Utilities.path_exists(executable_path):
        err_message = "Executable path does not exist: " + executable_path
        e = IOError(err_message)
        e.strerror = err_message
        raise e
    print(assignment.input_file)
    if not assignment.input_file == "":
        additional_args = additional_args + " <" + assignment.get_input_file_path()

    relative_output_path = individual_assignment.get_output_path()
    shell_command = executable_path + additional_args + \
        Constants.OUT_TO_FILE + relative_output_path
    print("Shell command " + str(shell_command))
    Utilities.run_program(shell_command)

    # Check for errors
    runtime_results = Utilities.read_file(
        individual_assignment.get_runtime_error_output_path())
    Utilities.delete_file(
        individual_assignment.get_runtime_error_output_path())

    if len(runtime_results) > 1 \
            and not runtime_results == "sh: pause: command not found":
        raise RuntimeException(runtime_results, runtime_results)

    return relative_output_path


def print_student_header(student):
    Utilities.log(
        "-------------------------------------- \
            -----------------------------------------")
    Utilities.log("Student: " + student.name +
                  " | Username: " + student.username)


def grade_assignmets(students, assignment):
    """Grade Assignments

    Loops through all students and clones, runs, and grades their assignments.
    It keeps track of all skipped assignments if one grading procedure fails.

    Args:
        students ([Student]): List of students to grade assignments for
        assignment (Assignment): Course assignment to be graded

    Returns:
        Assignment: Course assignment containing all individual
                    assignments with results

    """

    Utilities.log("Grading assignments...")
    assignment.skipped_assignments = []
    assignment.individual_assignments = []

    # get the rubric output file contents

    # Loop through individual assignments
    for current_student in students:

        # Create and add individual assignmenti to list
        print_student_header(current_student)
        individual_assignment = IndividualAssignment(
            assignment.name, current_student, assignment.course_name)

        try:
            # clone the current student's assignment
            DataService.clone_repo(current_student, assignment)
            # check if the source compiles at all
            source_report = source_analyzer. \
                analyze_source(current_student.get_assignment_path(
                    individual_assignment), assignment, individual_assignment)

            individual_assignment.compiled = True
            # get output file path after running the student's program
            relative_output_path = run_assignment_executable(
                individual_assignment, assignment)
            individual_assignment.ran = True
            if not assignment.executionOnly:
                rubric_file_dicts = Utilities.json_deserialize(
                    assignment.get_rubric_file_path())
                # get the student output file contents
                assignment_file_contents = Utilities.read_file(
                    relative_output_path)
                # grade assignment
                individual_assignment = grade_assignment(
                    rubric_file_dicts, assignment_file_contents,
                    individual_assignment, assignment)
                # copy source report to individual assignment
                individual_assignment.source_report = source_report
                # to avoid grades like 0.001
                if individual_assignment.grade < 1:
                    individual_assignment.grade = 0
            assignment.individual_assignments.append(individual_assignment)

        except IOError as e:
            # Keep track of skipped assignments due to errors
            Utilities.log(e.strerror)
            assignment.skipped_assignments.append(individual_assignment)

        # Handle other errors
        except GitCommandError as e:
            Utilities.log("Git Error - skipping student:" + e.stderr)
            assignment.skipped_assignments.append(individual_assignment)

        except CompilationException as e:
            Utilities.log(e.message)
            Utilities.log(e.details)
            # TODO decide how much to deduct exactly
            individual_assignment.grade = 0
            assignment.individual_assignments.append(individual_assignment)

        except RuntimeException as e:
            Utilities.log(e.message)
            # TODO: decide how much to deduct exactly
            individual_assignment.grade = 0
            assignment.individual_assignments.append(individual_assignment)

        finally:
            strr = " | Functions: " + str(len(individual_assignment
                                              .source_report.functions)
                                          ) if individual_assignment \
                                               .source_report \
                                               is not None else ""

            Utilities.log("RESULT - Wrong answers: "
                          + str(len(individual_assignment.wrong_lines))
                          + " | Wrong lines: " +
                          str(individual_assignment.wrong_lines) +
                          " | Grade: " + str(round(individual_assignment.grade))
                          + strr)

    return assignment


def get_assignments(checkFirst):
    """Gets all assignments from disk

    Args:
        checkFirst (boolean): Flag indicating whether to check if the assignment file exists

    Returns:
        ([Assignment]): list of assignments

    """
    try:
        if checkFirst:
            DataService.create_assignments_file()
        return DataService.get_assignments()
    except IOError:
        sys.exit(
            "Failed to retrieve assignments. Make sure that the file exists. Perhaps enter a new assignment first?")
    except json.JSONDecodeError:
        sys.exit("JSON File is corrupted. Failed to retrieve assignments")


def save_assignments(assignments):
    """Saves assignmetns on disk """

    try:
        DataService.save_assignments(assignments)
        Utilities.log("Assignment saved!")
    except Exception as e:
        Utilities.log("ERROR: " + str(e))
        Utilities.log("Failed to save data... Try again.")


def enter_new_assignment():
    """Prompts the user to enter a new assignment

    Returns:
        (Assignment): The newly created assignment

    """
    Utilities.log("--------------------------")
    course_name = input("Course name (e.g: CMPS-3410): ")
    name = input(
        "The name of the assignment (should be a folder in student repositories): ")
    # Check if course already has student list

    strings_matter = input(
        "Should string values be a part of the grading procedure (y/N): ")
    strings_matter = True if strings_matter.upper() == "Y" else False
    table_formatting = input(
        "Does this assignment contain ASCII Tables? (y/N): ")
    table_formatting = True if table_formatting.upper() == "Y" else False
    input_file_used = input("Do you want to add an input file? (y/N): ")
    file_path = ""
    if input_file_used.upper() == "Y":
        Tk().withdraw()
        file_path = askopenfilename()
        print(file_path)

    confirm = "N"

    assignment = Assignment(name, course_name, [], strings_matter=strings_matter,
                            table_formatting=table_formatting, input_file=file_path)

    # Add rubric
    rubric_choice = input("Would you like enter to a rubric file? (y/N)")
    if rubric_choice.upper() == "Y":
        Tk().withdraw()
        file_path = askopenfilename()
        contents = Utilities.read_file(file_path)
        Utilities.create_file_dir_if_not_exists(
            assignment.get_rubric_file_path())
        Utilities.write_file(assignment.get_rubric_file_path(), contents, "w+")
    else:
        assignment.executionOnly = True
        Utilities.log(
            "Assignment will be graded only by compilation and execution.")

    # Add weights
    # Tk().withdraw()
    # file_path = askopenfilename()
    # contents = Utilities.read_file(file_path)
    # Utilities.create_file_dir_if_not_exists(assignment.get_weights_file_path())
    # Utilities.write_file(assignment.get_weights_file_path(), contents, "w+")
    while not confirm.upper() == "Y" or confirm.upper == "N":
        confirm = input("Save assignment? (Y/n) ")
        if confirm.upper() == "Y":
            assignments = get_assignments(True)
            matches = [x for x in assignments if x.course_name == course_name]

            # Add students
            if len(matches) == 0:
                print(
                    "This course does not have any students, please provide a file with student info in json format.\n")
                Tk().withdraw()
                file_path = askopenfilename()
                contents = Utilities.read_file(file_path)
                Utilities.create_file_dir_if_not_exists(
                    assignment.get_students_file_path())
                Utilities.write_file(
                    assignment.get_students_file_path(), contents, "w+")
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
        Utilities.log(assignment.name)
    Utilities.log("\nEnter the name of the repo to start grading assignments")
    while try_again:
        name = input()
        found = [assignment for assignment in assignments if assignment.name == name]
        if found == [] or found[0] is None:
            Utilities.log("Try again.")
        else:
            try_again = False
            return found[0]


def update_assignment(assignment):
    assignments = get_assignments(False)
    for i, a in enumerate(assignments):
        if a.name == assignment.name:
            assignments[i] = assignment
    save_assignments(assignments)


def grade(assignment):
    """Grades an assignment for all students and generates a report """

    # assignment = get_assignment_to_grade()
    students = load_students(assignment)
    assignment = grade_assignmets(students, assignment)
    update_assignment(assignment)
    report_generator.printSummary(assignment)
    report_generator.generate_report(assignment)
