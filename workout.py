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
    MediumText, LineBreak, simple_page_number, Package, Section
from pylatex.utils import bold
import time as t

#  document formatting


def gen_accessory_table(accesorys):
    return


def gen_week(doc, main_lifts):
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


def compile_document(main_lifts):

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
    doc.generate_pdf("workout_routine", clean_tex=True)


#  calculations for workout


def weight(w, base=2.5):
    return round(base*round(w/base), 2)


if __name__ == "__main__":
    bench = [('Incline BP', '(4 x 12)'),
             ('Pull up', '(4 x Max)')]
    main_lifts = [('Bench', 85),
                  ('Squat', 100),
                  ('Military Press', 45),
                  ('Deadlift', 110)]
    compile_document(main_lifts)
