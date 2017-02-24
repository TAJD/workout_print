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
from pylatex import Document, PageStyle, Head, MiniPage, LargeText, \
    MediumText, LineBreak, simple_page_number, Package, Section,  Tabular,\
    MultiColumn, VerticalSpace, Subsection
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
    pc = np.array([[0.65, 0.75, 0.8], [0.7, 0.8, 0.85], [0.75, 0.85, 0.9],
                  [0.4, 0.5, 0.6]])
    reps = ([[8, 8, 8], [6, 6, 6], [8, 6, 3], [10, 10, 10]])
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
    r_and_w = calc_main_lift(one_rm, no)

    table = Tabular('|c|c|c|c|c|c|')
    # table.add_hline()
    # table.add_row((MultiColumn(3, align='|c|', data=lift + " workout " +
    #                str(no)),))
    table.add_hline()
    table.add_row(('Warm up', 'Warm up', 'Warm up', 'Set 1', 'Set 2', 'Set 3'))
    table.add_hline()
    table.add_row(('', '', '',
                   str(r_and_w[1][0])+' x ' + str(r_and_w[0][0]),
                   str(r_and_w[1][1])+' x ' + str(r_and_w[0][1]),
                   str(r_and_w[1][2])+' x '+str(r_and_w[0][2])))
    table.add_hline()
    return table


def gen_accessory_table(accessorys):
    """Function to return a table for accessory exercises.

    Function to return a 'table' object for a given set of accessory exercises.

    Arguments:
        3 x n table with [name, sets, reps]

    Return:
        Table with the required columns for sets reps and weights.
    """
    table = Tabular('|c|c|c|c|c|c|c|c|c|')
    table.add_hline()
    table.add_row(('Exercise', 'Weight', 'Reps', 'Weight', 'Reps', 'Weight',
                   'Reps', 'Weight', 'Reps'))
    table.add_hline()
    for i in range(len(accessorys)):
        table.add_row((str(accessorys[i]), '', '', '',  '', '',  '', '', ''))
        table.add_hline()
    return table


def print_workout(doc, lift, one_rm, no, accessorys):
    """Print one workout routine.

    Arguments:
        lift
        one_rm
        no
        accessorys

    Returns:
        One workout
    """
    doc.append(VerticalSpace("20pt"))
    doc.append(LineBreak())

    main_lift = gen_main_lift(lift, one_rm, no)
    access = gen_accessory_table(accessorys)

    with doc.create(MiniPage(width=r"0.5\textwidth")):
        doc.append(bold('Main Lift\n\n'))
        doc.append(main_lift)
        doc.append(VerticalSpace("20pt"))
        doc.append(LineBreak())
        doc.append(bold('Accessory Exercises\n\n'))
        doc.append(access)
        # doc.append(main_lift)

    doc.append(VerticalSpace("20pt"))
    doc.append(LineBreak())
    return doc


def gen_week(doc, main_lifts, no, accessorys):
    """ Function to generate a weeks workout"""
    with doc.create(Section('Week ' + str(no))):
        for i in range(len(main_lifts)):
            title = main_lifts[i][0]
            with doc.create(Subsection(title)):
                doc.append('Date: ')
                doc.append(LineBreak())
                doc.append('Weight: ')
                print_workout(doc, main_lifts[i][0], main_lifts[i][1], no,
                              accessorys[i])
    return doc


def generate_header():

    # Add document header
    header = PageStyle("header")
    # Create left header
    with header.create(Head("L")):
        header.append("Weights updated: 24/02/16")
        header.append(LineBreak())
    # Create center header
    with header.create(Head("C")):
        header.append("8/6/3 Workout with BB Accessories")
    # Create right header
    # with header.create(Head("R")):
    #     header.append(simple_page_number())
    return header


def compile_document_week(no):
    # currently testing the production of a weeks workout

    # input accessory lifts for main lifts
    bench = [('Incline DB Press (4 x 12)'),
             ('Face pull (4 x 12)'),
             ('Low/High flyes ss/w press (4 x 12)'),
             ('Press ups (4 x Max)')]
    # squat = [('Leg press (4 x 15)'), ('Leg extension (4 x 12)'),
    #          ('Leg curl (4 x 12)'), ('Roll out (4 x Max)')]
    squat = [('Smith Front/Back (4 x 12)'), ('Calf Raises (4 x 12)'),
             ('Reverse Lunges (4 x 12)'), ('Roll out (4 x Max)')]
    dead = [('BB Row (4 x 8-12)'), ('Hip thrust (4 x 8-12)'),
            ('Pull up (4 x Max)'), ('Leg raise (4 x 8-12)')]
    press = [('Landmine press (4 x 8-12)'), ('Lateral/Rear raises (4 x 8-12)'),
             ('DB Curls (4 x 8-12)'), ('Roll outs (4 x Max)')]

    acc = [bench, squat, press, dead]

    # input main lifts and one rep maxes
    # last updated 24/02/2017
    main_lifts = [('Bench', 87.5),
                  ('Squat', 123),
                  ('Military Press', 61),
                  ('Deadlift', 138)]

    date = t.strftime("%d/%m/%Y")
    doc = Document()
    doc.packages.append(Package('geometry', options=['margin=2cm']))
    doc.packages.append(Package('times'))
    doc.packages.append(Package('float'))
    doc.packages.append(Package('graphicx'))
    header = generate_header()
    doc.preamble.append(header)
    doc.change_document_style("header")

    # Add title
    doc.append(LineBreak())
    doc.append(LargeText(bold("8/6/3 Workout Routine")))
    doc.append(LineBreak())
    doc.append(MediumText(bold("As of: " + date)))
    doc.append(LineBreak())

    # Add workout for a week
    gen_week(doc, main_lifts, no, acc)
    date_1 = t.strftime("%Y%m%d")
    filename = "workout_routine_week_"+str(no)+"_"+date_1
    doc.generate_pdf(filename, clean_tex=True)


#  calculations for workout


def weight(w, base=2.5):
    "Lowest plate weight at my gym is 1.25 kg."
    return np.round(base*np.round(w/base), 2)


def produce_table():
    # create document structure
    doc = Document("testtable")
    section = Section('Produce accessories table')
    test1 = Subsection('Test accessories table production')

    # test input code
    bench = [('Incline BP (4 x 12)'),
             ('Pull up (4 x Max)')]

    # test code
    accesory = bench
    table = Tabular('|c|c|c|c|c|c|c|c|c|')
    table.add_hline()
    table.add_row((MultiColumn(9, align='|c|', data='Accessories'),))
    table.add_hline()
    table.add_row(('Exercise', 'Weight', 'Reps', 'Weight', 'Reps', 'Weight',
                   'Reps', 'Weight', 'Reps'))
    table.add_hline()
    for i in range(len(accesory)):
        table.add_row((str(accesory[i]), '', '', '',  '', '',  '', '', ''))
        table.add_hline()

    # append table to document
    test1.append(table)
    section.append(test1)
    doc.append(section)
    doc.generate_pdf(clean_tex=True)


if __name__ == "__main__":
    # one_rm = 100
    no = 2
    # calcs = calc_main_lift(one_rm, no)
    # print(calcs)
    # produce_table()
    compile_document_week(no)
