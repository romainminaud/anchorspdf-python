# Anchors Pdf - Python

A simple tool designed to give the coordinates of text anchors within PDF files.

This can be used to target specific spots in the body of a dynamically generated PDF.

For parsing the PDF files the tool rely on [pdfminer.six](https://github.com/pdfminer/pdfminer.six).

## Installation

- Install Python 3.6 or newer

- Install anchorspdf

  - `git clone https://github.com/romainminaud/romainminaud/anchorspdf`
  - `cd anchorspdf`
  - `python setup.py install`

## Usage

- Prepare a PDF with text anchors, for instance {{anchor1}}, {{anchor2}}, etc. [Example PDF](examples/pdf/demo.pdf)

> :warning: The text anchors should not be flattened in the PDF (the tool does not perform OCR but merely text parsing)

- Import and instantiate an AnchorsParser class with the following arguments:

  - left_delimiter (required, left delimiter of the anchor)
  - right_delimiter (required, right delimiter of the anchor)
  - password (optional, provide it if the PDF file is password protected)

- Open the PDF file and use the parse_file method of the AnchorsParser class

```python

from anchors_pdf import AnchorsParser

parser = AnchorsParser(
  left_delimiter = "{{",
  right_delimiter = "}}",
  # password = "12345678
)

with open(os.path.join(script_dir, rel_path), 'rb') as f:
  anchors = parser.parse_file(f)

print(anchors)

```

- Output:

A dictionnary with the name of each anchor (excluding the delimiters) as a key (for instanc "anchor1", "anchor2", ...), and an array as a value containing for each anchor occurence in the document its page, coordinate, height and width.

```json
{
  "anchor1": [
    {
      "page": 1,
      "x0": 72,
      "x1": 138,
      "y0": 84,
      "y0_orig": 707,
      "y1_orig": 721,
      "width": 66,
      "height": 14
    },
    {
      "page": 1,
      "x0": 72,
      "x1": 138,
      "y0": 171,
      "y0_orig": 620,
      "y1_orig": 634,
      "width": 66,
      "height": 14
    }
  ],
  "anchor2": [
    {
      "page": 1,
      "x0": 72,
      "x1": 131,
      "y0": 244,
      "y0_orig": 547,
      "y1_orig": 561,
      "width": 59,
      "height": 14
    }
  ]
}
```

| Key     | Description                                                                |
| ------- | -------------------------------------------------------------------------- |
| page    | page of the anchor occurence (starting at 1)                               |
| x0      | lower left x-coordinate of the anchor occurence                            |
| x1      | upper right x-coordinate of the anchor occurence                           |
| y0      | lower left y-coordinate of the anchor occurence, y-axis going from top     |
| y1      | upper right y-coordinate of the anchor occurence, y-axis going from top    |
| y0_orig | lower left y-coordinate of the anchor occurence, y-axis going from bottom  |
| y1_orig | upper right y-coordinate of the anchor occurence, y-axis going from bottom |
| width   | width of the anchor occurence                                              |
| height  | height of the anchor occurence                                             |
