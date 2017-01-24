"""
Tool to print workout routine to latex document.

Code plan:
1. Start with calculating a table of weights given a workout number and 1rm.
2. Have a list of exercise names and 1rm - convert to 90% of one rep max.

"""

import numpy as np
from pylatex import Document, PageStyle, Head, MiniPage, Foot, LargeText, \
    MediumText, LineBreak, simple_page_number
from pylatex.utils import bold

#  document formatting


def generate_header():

    # Add document header
    header = PageStyle("header")
    # Create left header
    with header.create(Head("L")):
        header.append("Page date: ")
        header.append(LineBreak())
        header.append("R3")
    # Create center header
    with header.create(Head("C")):
        header.append("Company")
    # Create right header
    with header.create(Head("R")):
        header.append(simple_page_number())
    # Create left footer
    with header.create(Foot("L")):
        header.append("Left Footer")
    # Create center footer
    with header.create(Foot("C")):
        header.append("Center Footer")
    # Create right footer
    with header.create(Foot("R")):
        header.append("Right Footer")


def compile_document():
    geometry_options = {"margin": "0.7in"}
    doc = Document(geometry_options=geometry_options)
    header = generate_header()

    doc.preamble.append(header)
    doc.change_document_style("header")

    # Add Heading
    with doc.create(MiniPage(align='c')):
        doc.append(LargeText(bold("Title")))
        doc.append(LineBreak())
        doc.append(MediumText(bold("As at:")))
    doc.generate_pdf("header", clean_tex=False)


#  calculations for workout


def weight(w, base=2.5):
    return round(base*round(w/base), 2)


if __name__ == "__main__":
    compile_document()
