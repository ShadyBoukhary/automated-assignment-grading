import json
import sys
import re
import Levenshtein as lev
from git.exc import GitCommandError
from autocorrect import spell
import data.grader.source_analyzer as source_analyzer
import data.report.report_generator as report_generator
from custom.compilation_exception import CompilationException
from core.individual_assignment import IndividualAssignment
from data.data_service.data_service import DataService
from utils.constants import Constants
from utils.utilities import Utilities
from custom.runtime_exception import RuntimeException
from tqdm import tqdm
from colorama import Fore


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
    if not assignment.input_file == "":
        additional_args = additional_args + " <" + assignment.get_input_file_path()

    relative_output_path = individual_assignment.get_output_path()
    shell_command = executable_path + additional_args + Constants.OUT_TO_FILE + relative_output_path
    Utilities.Debug("Shell command " + str(shell_command))
    Utilities.run_program(shell_command)

    # Check for errors
    runtime_results = Utilities.read_file(individual_assignment.get_runtime_error_output_path())
    Utilities.delete_file(individual_assignment.get_runtime_error_output_path())

    if len(runtime_results) > 1 \
            and not runtime_results == "sh: pause: command not found":
        raise RuntimeException(runtime_results, runtime_results)

    return relative_output_path


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
    s_index = -1
    s_total = len(students)
    # Loop through individual assignments
    t = tqdm(students, bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET), desc='')
    for current_student in t:
        s_index = s_index + 1
        t.set_description(f"Grading {current_student.name}")
        # Create and add individual assignmenti to list
        individual_assignment = IndividualAssignment(assignment.name, current_student, assignment.course_name)
        remaining = 7
        step = 1
        ind_pbar = tqdm(total=remaining)
        with ind_pbar:
            try:
                # clone the current student's assignment
                ind_pbar.set_description_str(f"{current_student.name} - Retrieving assignment")
                DataService.clone_repo(current_student, assignment)
                ind_pbar.update(step)
                remaining = remaining - step

                # check if the source compiles at all
                ind_pbar.set_description_str(f"{current_student.name} - Compiling")
                source_report = source_analyzer.analyze_source(current_student.get_assignment_path(individual_assignment),
                                                               assignment, individual_assignment)
                individual_assignment.compiled = True
                ind_pbar.update(step)
                remaining = remaining - step

                # get output file path after running the student's program
                ind_pbar.set_description_str(f"{current_student.name} - Running")
                relative_output_path = run_assignment_executable(individual_assignment, assignment)
                individual_assignment.ran = True
                ind_pbar.update(step)
                remaining = remaining - step

                if not assignment.executionOnly:
                    ind_pbar.set_description_str(f"{current_student.name} - Retrieving rubric")
                    rubric_file_dicts = Utilities.json_deserialize(assignment.get_rubric_file_path())
                    ind_pbar.update(step)
                    remaining = remaining - step

                    ind_pbar.set_description_str(f"{current_student.name} - Grading")
                    # get the student output file contents
                    assignment_file_contents = Utilities.read_file(relative_output_path)
                    # grade assignment
                    individual_assignment = grade_assignment(rubric_file_dicts, assignment_file_contents,
                                                             individual_assignment, assignment)
                    # copy source report to individual assignment
                    individual_assignment.source_report = source_report
                    ind_pbar.update(step)
                    remaining = remaining - step
                    # to avoid grades like 0.001
                    if individual_assignment.grade < 1:
                        individual_assignment.grade = 0
                    
                ind_pbar.set_description_str(f"{Fore.GREEN}{current_student.name} - Finished grading")
                ind_pbar.update(remaining)
                assignment.individual_assignments.append(individual_assignment)

            except IOError as e:
                individual_assignment.seterr(e.strerror[:30], e.strerror)
                ind_pbar.set_description_str(f"{Fore.RED}{current_student.name} - Skipped")

            # Handle other errors
            except GitCommandError as e:
                individual_assignment.seterr("Could not pull assignment...", e.stderr)
                ind_pbar.set_description_str(f"{Fore.RED}{current_student.name} - Skipped")
                assignment.skipped_assignments.append(individual_assignment)

            except CompilationException as e:
                individual_assignment.seterr(f"{e.details[:30]}...", e.details)
                # TODO decide how much to deduct exactly
                individual_assignment.grade = 0
                individual_assignment.compiled = False
                individual_assignment.ran = False
                assignment.individual_assignments.append(individual_assignment)
                ind_pbar.set_description_str(f"{Fore.RED}{current_student.name} - Compilation Error")

            except RuntimeException as e:
                individual_assignment.seterr(f"{e.message[:30]}...", e.message)

                # TODO: decide how much to deduct exactly
                individual_assignment.grade = 0
                individual_assignment.ran = False
                assignment.individual_assignments.append(individual_assignment)
                ind_pbar.set_description_str(f"{Fore.RED}{current_student.name} - Runtime Exception")

            finally:
                if s_index == s_total - 1:
                    t.set_description_str(f"{Fore.GREEN}Grading Complete{Fore.RESET}")

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
    except Exception as e:
        Utilities.log("ERROR: " + e.__traceback__.__str__)
        Utilities.log("Failed to save data... Try again.")


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


def grade(assignment, dry_run):
    """Grades an assignment for all students and generates a report """

    if dry_run:
        print(f"{Fore.YELLOW}Dry run option is true. Will not save results or display grades.")
    students = load_students(assignment)
    assignment = grade_assignmets(students, assignment)
    report_generator.printSummary(assignment, dry_run)
    if not dry_run:
        report_generator.generate_report(assignment)
        update_assignment(assignment)


def summarize(assignment):
    """Prints summary of assignment"""
    report_generator.printSummary(assignment)
