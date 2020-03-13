import random
from collections import Counter
from statistics import median, stdev
from utils.constants import Constants
from utils.utilities import Utilities
import pandas as pd
from colorama import Fore, Back, Style


def printSummary(assignment, dry_run):
    errorSummary(assignment)
    gradeSummary(assignment, dry_run)


def errorSummary(assignment):
    Utilities.log(f"\n{Fore.YELLOW}--------------- Error Details ---------------\n")

    for individual_assignment in assignment.individual_assignments + assignment.skipped_assignments:
        if individual_assignment.has_error():
            print(f"{Back.RED}{individual_assignment.student.name}{Back.RESET}: {Fore.RED}{individual_assignment.error_details}")


def gradeSummary(assignment, dry_run):
    Utilities.log(f"\n{Fore.YELLOW}--------------- Summary ---------------\n")

    Utilities.log("{:<25}".format("Student Name"), True)
    Utilities.log("{:>10}".format("Compiled"), True)
    Utilities.log("{:>20}".format("Ran Successfully"), True)

    if not dry_run:
        Utilities.log("{:>20}".format(f"{Fore.YELLOW}Grade"), True)
    Utilities.log("{:>15}".format("Skipped"), True)
    Utilities.log("{:>40}".format("Error (see above)"))
    Utilities.log("-" * 125)

    i_normal_list = [(f"{Fore.GREEN}NO", i) for i in assignment.individual_assignments]
    i_skipped_list = [(f"{Fore.RED}YES", i) for i in assignment.skipped_assignments]
    i_list = i_normal_list + i_skipped_list
    for skipped, individual_assignment in i_list:

        grade = individual_assignment.grade
        color = None
        if grade >= 90:
            color = Fore.GREEN
        elif grade >= 70:
            color = Fore.BLUE
        else:
            color = Fore.RED
        
        compiled = "YES"
        compiled_color = Fore.GREEN
        ran = "YES"
        ran_color = Fore.GREEN
        if not individual_assignment.compiled:
            compiled = "NO"
            compiled_color = Fore.RED
        if not individual_assignment.ran:
            ran = "NO"
            ran_color = Fore.RED
        Utilities.log("{:<25}".format(individual_assignment.student.name), True)
        Utilities.log("{:>15}".format(f"{compiled_color}{compiled}"), True)
        Utilities.log("{:>25}".format(f"{ran_color}{ran}"), True)

        if not dry_run:
            Utilities.log("{:>20}".format(f"{color}{individual_assignment.grade}"), True)
        Utilities.log("{:>20}".format(skipped), True)
        Utilities.log("{:>40}".format(individual_assignment.error))




def generate_report(assignment):
    """Generates Report

    Generates a report for the course assignment. Loops through all individual assignments
    in the course assignment, generates graphs showing grade distribution, average, highest
    and lowest grades, skipped assignments, and more.

    Args:
        assignment (Assignment): Course assignment containing all individual assignments

    """
    Utilities.log("\nGenerating report... ", True)
    # All student grades for assignment
    grades = [individual_assignment.grade for individual_assignment in assignment.individual_assignments]
    names = [individual_assignment.student.name for individual_assignment in assignment.individual_assignments]

    if len(grades) < 1:
        return


    grades_counter = Counter(grades)

    # Prepare data
    cat_1 = ['Grades']
    index_1 = names
    multi_iter1 = {'index': index_1}
    for cat in cat_1:
        multi_iter1[cat] = grades

    # Create a Pandas dataframe using the grades
    index_2 = multi_iter1.pop('index')
    data_frame = pd.DataFrame(multi_iter1, index=index_2)
    data_frame = data_frame.reindex(columns=sorted(data_frame.columns))
    
    # Createe Pandas Excel writer with XlsxWriter engine
    excel_file = assignment.get_reports_dir_path() +  assignment.course_name + "_" + assignment.name + "_assignment_report.xlsx"
    sheet_name = "Report"

    writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")
    data_frame.to_excel(writer, sheet_name=sheet_name)

    # Access the XlsxWriter workbook and worksheet objects from data_frame
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    #        # Set the column widths.
    worksheet.set_column("A:B", 18)

    # Set the column widths.
    worksheet.set_column("D:F", 18)

    currency_format = workbook.add_format({'num_format': '#,##0'})

    # Calculate statistics
    mean = sum(grades) / float(len(grades))
    med = median(grades)
    std_dev = stdev(grades)

    
    # Options for the table
    data = [[mean, med, std_dev]]

    options = {'data': data,
           'total_row': 1,
           'columns': [{'header': 'Mean'},
                       {'header': 'Median',
                        'format': currency_format,
                        },
                       {'header': 'Standard Deviation',
                        'format': currency_format,
                        }
                       ]}


    worksheet.add_table('D3:F5', options)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    Utilities.log(Constants.CHECK_MARK)
