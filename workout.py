"""
Tool to print workout routine to latex document.

Code plan:
1. Start with calculating a table of weights given a workout number and 1rm.
2. Have a list of exercise names and 1rm - convert to 90% of one rep max.
3. Function to generate workout
    - Main exercise name, sets, reps and Weights
    - List of accessory exercises and reps
4. Generate 16 workouts
    - List of tuples for the 4 main workouts and their 1rm
    - 4 lists of exercises for each lift
5. Need to generate a table for the main lift
6. Need to generate a table for the accesory lifts


Generate one array of weights and reps per main exercise per week?

Function to generate workout for a given main exercise and week number?
    - Generate one whole workout series
    - Generate any given week
"""

import numpy as np
from pylatex import Document, PageStyle, Head, MiniPage, Foot, LargeText, \
    MediumText, LineBreak, simple_page_number, Package, Section,  Tabular,\
    MultiRow,  MultiColumn
from pylatex.utils import bold
import time as t


def calc_main_lift(one_rm, no):
    """ Return the reps and weights for any given week.

    Arguments:
        one_rm: One rep max (kg)
        no: Workout number

    Returns:
        array (2 columns x 3 rows)
    """
    one_rm *= 0.90  # convert one rep max to 90% of 1rm
    pc = np.array([[0.65, 0.75, 0.8], [0.7, 0.8, 0.85], [0.75, 0.85, 0.9]])
    reps = ([[8, 8, 8], [6, 6, 6], [8, 6, 3]])
    wo = no - 1
    return (weight(pc[wo]*one_rm), reps[wo])


def gen_main_lift(lift, one_rm, no):
    """Function to return a table for the reps and weights for a given week.

    Arguments:
        lift: Name of the lift
        one_rm: One rep max for the lift
        no: Number of workout (1 - 4)

    Return:
        pylatex table object
    """
    table = Tabular('|c|c|c|')
    table.add_hline()
    table.add_row((MultiColumn(3, align='|c|', data=lift + " workout " +
                   str(no)),))
    table.add_hline()
    table.add_row(('Set 1', 'Set 2', 'Set 3'))
    table.add_hline()
    table.add_row(())
    return table


def gen_accessory_table(accessorys):
    """Function to return a table for accessory exercises.

    Function to return a 'table' object for a given set of accessory exercises.

    Arguments:
        3 x n table with [name, sets, reps]

    Return:
        Table with the required columns for sets reps and weights.
    """
    table = Tabular('|c|c|c|c|c|c|')
    table.add_hline()
    table.add_row((MultiColumn(6, align='|c|', data='Accessory Exercises'),))
    return table


def gen_week(doc, main_lifts):
    """ Function to generate a weeks workout"""
    for i in range(len(main_lifts)):
        title = main_lifts[i][0]
        with doc.create(Section(title)):
            doc.append('1 RM is ' + str(main_lifts[i][1]) + 'kg\n')
            doc.append('insert reps and weights here')
    return doc


def generate_header():

    # Add document header
    header = PageStyle("header")
    # Create left header
    with header.create(Head("L")):
        header.append("Weights updated: 25/01/16")
        header.append(LineBreak())
        # header.append("R3")
    # Create center header
    with header.create(Head("C")):
        header.append("Workout Routine")
    # Create right header
    with header.create(Head("R")):
        header.append(simple_page_number())
    # # Create left footer
    # with header.create(Foot("L")):
    #     header.append("Left Footer")
    # # Create center footer
    # with header.create(Foot("C")):
    #     header.append("Center Footer")
    # # Create right footer
    # with header.create(Foot("R")):
    #     header.append("Right Footer")
    return header


def compile_document():
    bench = [('Incline BP', '(4 x 12)'),
             ('Pull up', '(4 x Max)')]
    main_lifts = [('Bench', 85),
                  ('Squat', 100),
                  ('Military Press', 45),
                  ('Deadlift', 110)]

    date = t.strftime("%d/%m/%Y")
    doc = Document()
    doc.packages.append(Package('geometry', options=['margin=2cm']))
    doc.packages.append(Package('times'))
    doc.packages.append(Package('float'))
    doc.packages.append(Package('graphicx'))
    header = generate_header()

    doc.preamble.append(header)
    doc.change_document_style("header")

    # Add Heading
    with doc.create(MiniPage(align='c')):
        doc.append(LargeText(bold("8/6/3 Workout Routine")))
        doc.append(LineBreak())
        doc.append(MediumText(bold("As of: " + date)))

    gen_week(doc, main_lifts)
    doc.append(gen_main_lift('bench', 85, 1))
    doc.generate_pdf("workout_routine", clean_tex=True)


#  calculations for workout


def weight(w, base=2.5):
    return np.round(base*np.round(w/base), 2)


if __name__ == "__main__":
    one_rm = 100
    no = 1
    calcs = calc_main_lift(one_rm, no)
    print(calcs)
    # compile_document()
