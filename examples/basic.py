#!/usr/bin/env python3

import os
from anchorspdf import AnchorsParser

# Instantiate parser

parser = AnchorsParser(
    left_delimiter="{{",
    right_delimiter="}}",
    password=None
)

# Parse PDF file

rel_path = "../examples/pdf/demo2.pdf"
script_dir = os.path.dirname(__file__)

with open(os.path.join(script_dir, rel_path), 'rb') as f:
    anchors =  parser.parse_file(f)

print(anchors)