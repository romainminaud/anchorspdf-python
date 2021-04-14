from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
from collections import defaultdict


class AnchorsParser(object):

    left_delimiter = None
    right_delimiter = None
    password = None

    def __init__(self, left_delimiter, right_delimiter, password=None):

        self.left_delimiter = left_delimiter
        self.right_delimiter = right_delimiter
        self.password = password

    def parse_obj(self, lt_objs, page_number, page):

        fields = {}

        for obj in lt_objs:

            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):

                text = obj.get_text().replace('\n', '')

                if text.startswith(self.left_delimiter):

                    anchor = text.split(self.left_delimiter)[
                        1].split(self.right_delimiter)[0]

                    x0, y0_orig, x1, y1_orig = obj.bbox

                    if anchor not in fields:
                        fields[anchor] = []

                    newAnchor = {
                        "page": int(page_number),
                        'x0': int(x0),
                        'x1': int(x1),
                        'y0': int(page.mediabox[3] - y0_orig),
                        'y1': int(page.mediabox[3] - y1_orig),
                        'y0_orig': int(y0_orig),
                        'y1_orig': int(y1_orig),
                        'width': int(x1 - x0),
                        'height': int(y1_orig - y0_orig)
                    }

                    fields[anchor].append(newAnchor)

            elif isinstance(obj, pdfminer.layout.LTFigure):
                self.parse_obj(obj._objs, page_number, page)

        return fields

    def parse_file(self, pdf):
        parser = PDFParser(pdf)

        if self.password is not None:
            document = PDFDocument(parser, self.password.encode('utf-8'))
        else:
            document = PDFDocument(parser)

        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        rsrcmgr = PDFResourceManager()
        device = PDFDevice(rsrcmgr)
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        page_number = 0

        results_dict = defaultdict(list)

        for page in PDFPage.create_pages(document):

            page_number += 1

            interpreter.process_page(page)
            layout = device.get_result()
            results = self.parse_obj(layout._objs, page_number, page)

            for key, value in results.items():
                results_dict[key] += value

        return dict(results_dict)
