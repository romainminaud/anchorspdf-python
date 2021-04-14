# Yousign API v2 example

This parsing tooling can be used for instance to automatically place signatures on dynamically generated PDF files.

We show an example to use this technique with [Yousign API v2](https://dev.yousign.com/).

For this example we provided a basic Python wrapper for using the API `examples/yousign-v2/client.py` but you can easily adaptat it to your own implementation.

## Pre-requesite

- Install Python 3.6 or newer

- Install anchorspdf

  - `git clone https://github.com/romainminaud/romainminaud/anchorspdf`
  - `cd anchorspdf`
  - `python setup.py install`

## Usage

### Without anchorspdf

Usually when adding a File Object to a Procedure you need to provide its exact coordinated using the attribute `position` with `position = "x0,y0_orig,x1,y1_orig"` where:

- x0: lower left x-coordinate of the File Object
- y0_orig: lower left y-coordinate of the anchor occurence, y-axis going from bottom 
- x1: upper right x-coordinate of the File Object
- y1_orig: upper right y-coordinate of the anchor occurence, y-axis going from bottom

Example:

```json
{
  "mention": "Read and approved",
  "mention2": "Signature",
  "position": "214,400,350,433"
}
```

### With anchorspdf

- Prepare your PDF file by placing anchors where you want to have the signature.

> :warning: To hide the anchor from the generated document we recommend using the same color as the background for the anchor.

- Prepare the File Object without the attribute `position` but with the attributes: `anchor` (name of the anchor in the PDF), `width` (width of the target File Object), `height` (height of the target File Object).

```json
{
  "mention": "Read and approved",
  "mention2": "Signature",
  "anchor": "signature1",
  "width": 120,
  "height": 50
}
```

- Use anchorspdf to get the coordinates of the corresponding anchors and automatically create and enrich the related File Objects with the position attribute using `enrich_field`function in `yousign.py`

- Iter on the output to add the File Objects to the procedure

### Demo

`cd examples`

Rename `config.ini.dist` into `config.ini`
Fill it with your Yousign API v2 API Key.

`python yousign.py`