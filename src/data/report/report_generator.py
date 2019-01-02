import random
from collections import Counter
from statistics import median, stdev

import pandas as pd


def generate_report(assignment):
    """Generates Report

    Generates a report for the course assignment. Loops through all individual assignments
    in the course assignment, generates graphs showing grade distribution, average, highest
    and lowest grades, skipped assignments, and more.

    Args:
        assignment (Assignment): Course assignment containing all individual assignments

    """
    print("\nGenerating report...")
    # All student grades for assignment
    grades = [individual_assignment.grade for individual_assignment in assignment.individual_assignments]
    grades.append(16)
    grades.append(46)

    grades.append(36)

    # grades.append(76)

    # grades.append(26)

    # grades.append(19)
    # grades.append(19)

    # grades.append(19)

    # grades.append(60)

    # grades.append(100)
    grades_counter = Counter(grades)

    # Prepare data
    cat_1 = ['Grades']
    index_1 = range(0, 101, 1)
    multi_iter1 = {'index': index_1}

    for cat in cat_1:
        multi_iter1[cat] = [grades_counter[x] if x in grades_counter else 0 for x in index_1]

    # Create a Pandas dataframe using the grades
    index_2 = multi_iter1.pop('index')
    data_frame = pd.DataFrame(multi_iter1, index=index_2)
    data_frame = data_frame.reindex(columns=sorted(data_frame.columns))
    
    # Createe Pandas Excel writer with XlsxWriter engine
    excel_file = assignment.get_reports_dir_path() +  assignment.course_name + "_" + assignment.repo_name + "_assignment_report.xlsx"
    sheet_name = "Report"

    writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")
    data_frame.to_excel(writer, sheet_name=sheet_name)

    # Access the XlsxWriter workbook and worksheet objects from data_frame
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Create a Chart object
    chart = workbook.add_chart({"type": "column"})

    # Configure chart series from dataframe
    chart.add_series({
    'categories': [sheet_name, 1, 0, 101, 0], #row #col #row #col
    'values':     [sheet_name, 1, 1, 101, 1],
    "gap":        50
    })

    # Configure the chart axes.
    chart.set_x_axis({'name': 'Grade', 'position_axis': 'on_tick'})
    chart.set_y_axis({'name': 'Number of Students', 'major_gridlines': {'visible': False}})

    # Turn off chart legend. It is on by default in Excel.
    chart.set_legend({'position': 'none'})

    # Insert the chart into the worksheet.
    worksheet.insert_chart('D10: J25', chart)


    # Generate table

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

    print("Report Generated \u2713")
