#!/usr/bin/env python3

import os
import base64
import configparser
from anchorspdf import AnchorsParser
from client import Client

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

client = Client(
    api_key=config.get('API', 'API_KEY_STAGING'),
    production=False,
    debug=True
)

# Create New Procedure
procedure = client._create_procedure({
    "name": "Test Procedure with Anchors",
    "description": "Description of my procedure",
    "start": False
})

# Add a File to the Procedure

rel_path = "../pdf/demo2.pdf"
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, rel_path)

with open(file_path, "rb") as pdf:
    encoded_string = base64.b64encode(pdf.read())

file = client._create_file({
    'name': 'contract.pdf',
    'content': encoded_string.decode('utf-8')
}, procedure['id'])

pdf.close

# Add a Member to the Procedure
member = client._create_member({
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@yousign.fr",
    "phone": "+33612345678"
}, procedure['id'])

# Instantiate Anchors Parser

parser = AnchorsParser(
    left_delimiter="{{",
    right_delimiter="}}",
    password=None
)

# Start Parsing
with open(file_path, 'rb') as f:
    anchors = parser.parse_file(f)

file_objects = []

file_objects.append({
    'anchor': "signature1",
    'width': 150,
    'height': 34
})

file_objects.append({
    'anchor': "signature2",
    'width': 150,
    'height': 34
})

file_objects.append({
    'type': 'text',
    'content': 'First Name',
    'anchor': "text1",
    'width': 150,
    'height': 20
})

file_objects.append({
    'type': 'text',
    'content': 'First Name',
    'anchor': "text2",
    'width': 150,
    'height': 20
})

file_objects.append({
    'type': 'text',
    'content': 'First Name',
    'anchor': "text3",
    'width': 150,
    'height': 20
})

def enrich_field(field, anchors):
    fields = []
    if 'anchor' in field:
        if field['anchor'] in anchors:
            for anchor in anchors[field['anchor']]:
                newField = field.copy()
                # newField.update(anchor)

                if "width" in field:
                    anchor['x1'] = anchor['x0'] + field['width']
                    del newField['width']

                if "height" in field:
                    anchor['y1_orig'] = anchor['y0_orig'] + field['height']
                    del newField['height']

                newField['page'] = anchor['page']

                newField['position'] = "{0},{1},{2},{3}".format(
                    anchor['x0'], anchor['y0_orig'], anchor['x1'], anchor['y1_orig'])

                del newField['anchor']

                fields.append(newField)

            return fields
    else:
        return None


# Iter on Anchors found in PDF file to generate File Objets based on File Object definition
for file_object in file_objects:
    output = enrich_field(file_object, anchors)
    print(output)
    # Add the File Objects generated to the Procedure
    for new_file_objects in output:
        client._create_file_object(
            new_file_objects, procedure['id'], file['id'], member['id'])


# Start Procedure and print signature link

start = client._start_procedure(procedure['id'])

for i in start['members']:
    print(client._get_signature_link(i['id']))
