#!/usr/bin/env python

from data.grader import grader
import colorama
import click
from utils.utilities import Utilities
from utils.constants import Constants
from core.assignment import Assignment
from data.data_service.data_service import DataService
from custom.deletion_exception import DeletionException
from custom.assignment_exception import AssignmentException
from custom.mutually_exclusive_option import MutuallyExclusiveOption
from PyInquirer import prompt
from colorama import Fore

print_color = Fore.LIGHTMAGENTA_EX


@click.group()
@click.help_option('--help', '-h')
def main():
    colorama.init(autoreset=True)


@main.command()
@click.argument('course_name')
@click.argument('assignment_name')
@click.option('--input-file', '-i', help='The input file to be used for the assignment')
@click.option('--rubric-file', '-r', help=Constants.RUBRIC_HELP)
@click.option('--student-file', '-s', help=Constants.STUDENT_HELP)
@click.help_option('--help', '-h')
def create(course_name, assignment_name, input_file, rubric_file, student_file):
    '''Creates a new assignment'''

    if DataService.assignment_exists(course_name, assignment_name):
        raise click.UsageError(f'Assignment {assignment_name} in course {course_name} already exists')

    input_file = click.prompt('Please enter the input file path',
                              default=input_file)

    if not Utilities.path_exists(input_file):
        raise click.FileError(input_file, 'Path does not exist')

    rubric_file = click.prompt('Please enter the rubric file path',
                               default=rubric_file)

    if not Utilities.path_exists(rubric_file):
        raise click.FileError(rubric_file, 'Path does not exist')

    assignment = Assignment(assignment_name, course_name, [], strings_matter=False,
                            table_formatting=False, input_file=input_file)

    if not Utilities.path_exists(assignment.get_students_file_path()):
        student_file = click.prompt('Please enter the student file path',
                                    default=student_file)
        if not Utilities.path_exists(student_file):
            raise click.FileError(student_file, 'Path does not exist')

        assignment.create_student_file(student_file)
    assignment.create_rubric_file(rubric_file)
    DataService.create_assignment(assignment)


@main.command()
@click.argument('course_name')
@click.argument('assignment_name')
@click.option('--input-file', '-i', help='The input file to be used for the assignment')
@click.option('--rubric-file', '-r', help=Constants.RUBRIC_HELP)
@click.help_option('--help', '-h')
def edit(course_name, assignment_name, input_file, rubric_file):
    '''Edits an assignment'''

    try:
        assignment, assignments = DataService.get_assignment_and_assignments(course_name, assignment_name)
        if input_file is None and rubric_file is None:
            raise click.exceptions.UsageError('You must select an option to edit with.')

        if input_file is not None:
            if Utilities.path_exists(input_file):
                assignment.create_input_file(input_file)
            else:
                raise click.FileError(input_file, 'Path does not exist')

        if rubric_file is not None:
            if Utilities.path_exists(rubric_file):
                assignment.create_rubric_file(rubric_file)
            else:
                raise click.FileError(rubric_file, 'Path does not exist')

        DataService.save_assignments(assignments)

    except AssignmentException as e:
        raise click.UsageError(e.message)


@main.command()
@click.argument('course_name')
@click.argument('assignment_name')
@click.help_option('--help', '-h')
def delete(course_name, assignment_name):
    '''Deletes an assignment'''
    try:
        DataService.delete_assignment(course_name, assignment_name)
    except DeletionException as e:
        raise click.UsageError(e.message)


@main.command()
@click.option('--interactive', '-i',
              is_flag=True,
              help='Interactive list',
              cls=MutuallyExclusiveOption,
              mutually_exclusive=['course_name'])
@click.option('--course_name', '-c',
              help='Assignments in course',
              cls=MutuallyExclusiveOption,
              mutually_exclusive=['interactive'])
@click.help_option('--help', '-h')
def alist(interactive, course_name):
    '''Lists all the assignments'''
    assignments, assignments_by_full_name, courses = categorizeAssignments()

    if interactive:
        questions = [
            {
                'type': 'list',
                'message': 'Select course',
                'name': 'Courses',
                'choices': courses.keys()
            }
        ]
        answer = prompt(questions, style=Constants.STYLE)
        for assignment in courses[answer['Courses']]:
            print(f'{print_color}{assignment}{Fore.RESET}')

    elif course_name:
        for assignment in courses[course_name]:
            print(f'{print_color}{assignment}{Fore.RESET}')
    else:
        for cname in courses.keys():
            print(f'{Fore.GREEN}=== {cname} ==={Fore.RESET}')
            for assignment in courses[cname]:
                print(f'{print_color}{assignment}{Fore.RESET}')


@main.command()
@click.option('--interactive', '-i',
              is_flag=True,
              help='Interactive list',
              cls=MutuallyExclusiveOption,
              mutually_exclusive=['course_name, assignment_name'])
@click.option('--course_name', '-c',
              help='Assignment in course',
              cls=MutuallyExclusiveOption,
              mutually_exclusive=['interactive'])
@click.option('--assignment_name', '-a',
              help='Assignment',
              cls=MutuallyExclusiveOption,
              mutually_exclusive=['interactive'])
@click.option('--dry-run', '-d',
              is_flag=True,
              help='Compiles and runs without assigning a grade or saving results.')
@click.help_option('--help', '-h')
def grade(interactive, course_name, assignment_name, dry_run):
    '''Grades an assignment'''
    assignments, assignments_by_full_name, courses = categorizeAssignments()

    if interactive:
        questions = [
            {
                'type': 'list',
                'message': 'Select course',
                'name': 'Courses',
                'choices': courses.keys()
            }
        ]
        answer = prompt(questions, style=Constants.STYLE)
        full_name = answer['Courses']
        questions[0]['message'] = 'Select assignment to grade'
        questions[0]['name'] = 'Assignments'
        questions[0]['choices'] = courses[full_name]
        answer = prompt(questions, style=Constants.STYLE)
        full_name = f"{full_name}{answer['Assignments']}"

        assignment_to_grade = assignments_by_full_name[full_name]
        grader.grade(assignment_to_grade, dry_run)
    elif course_name and assignment_name:
        try:
            assignment_to_grade, assignments = DataService.get_assignment_and_assignments(course_name, assignment_name)
            grader.grade(assignment_to_grade, dry_run)
        except AssignmentException as e:
            raise click.UsageError(e.message)
    else:
        raise click.UsageError('''Must provide course_name and assignment_name.
E.g.: aaa grade -c course -a assignment.
Use `--help` for more information''')


@main.command()
@click.option('--interactive', '-i',
              is_flag=True,
              help='Interactive list',
              cls=MutuallyExclusiveOption,
              mutually_exclusive=['course_name, assignment_name'])
@click.option('--course_name', '-c',
              help='Assignment in course',
              cls=MutuallyExclusiveOption,
              mutually_exclusive=['interactive'])
@click.option('--assignment_name', '-a',
              help='Assignment',
              cls=MutuallyExclusiveOption,
              mutually_exclusive=['interactive'])
@click.help_option('--help', '-h')
def sum(interactive, course_name, assignment_name):
    '''Shows the summary of a graded assignment'''

    assignments, assignments_by_full_name, courses = categorizeAssignments()

    if interactive:
        questions = [
            {
                'type': 'list',
                'message': 'Select course',
                'name': 'Courses',
                'choices': courses.keys()
            }
        ]
        answer = prompt(questions, style=Constants.STYLE)
        full_name = answer['Courses']
        questions[0]['message'] = 'Select assignment to to summarize'
        questions[0]['name'] = 'Assignments'
        questions[0]['choices'] = courses[full_name]
        answer = prompt(questions, style=Constants.STYLE)
        full_name = f"{full_name}{answer['Assignments']}"

        assignment_to_summarize = assignments_by_full_name[full_name]
        if len(assignment_to_summarize.individual_assignments) < 1:
            raise click.UsageError("An assignment must be graded before it can be summarized")

        grader.summarize(assignment_to_summarize)
    elif course_name and assignment_name:
        try:
            assignment_to_summarize, assignments = DataService.get_assignment_and_assignments(course_name, assignment_name)
            if len(assignment_to_summarize.individual_assignments) < 1:
                raise click.UsageError("An assignment must be graded before it can be summarized")

            grader.summarize(assignment_to_summarize)
        except AssignmentException as e:
            raise click.UsageError(e.message)
    else:
        raise click.UsageError('''Must provide course_name and assignment_name.
E.g.: aaa sum -c course -a assignment or aaa sum -i
Use `--help` for more information''')


def categorizeAssignments():
    assignments = DataService.get_assignments()
    if len(assignments) == 0:
        raise click.UsageError("Error: There are no assignments.")
    assignments_by_full_name = {}
    courses = {}
    for assignment in assignments:
        courses[assignment.course_name] = []
    for assignment in assignments:
        courses[assignment.course_name].append(assignment.name)
        assignments_by_full_name[f'{assignment.course_name}{assignment.name}'] = assignment

    return assignments, assignments_by_full_name, courses,

if __name__ == "__main__":
    main()
