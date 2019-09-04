
import difflib
import os

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTTextLineHorizontal
from pdfminer.converter import PDFPageAggregator
from PyPDF2 import PdfFileWriter, PdfFileReader

SPECIAL_CHARS = ['.', '/', '-']


class PDFAnalyzer(object):
    def __init__(self, pdf_file):
        print('pdf analysis')
        self.pdf_file = pdf_file
        self.pages = []
        self.page_size = []
        self._layouts = []
        self.header_lines = []
        self.footer_lines = []
        self.extract_layouts()
        self.extract_textline()
        print('done.')
        # self.header_size = self.detect_header_size()
        # self.footer_size = self.detect_footer_size()

    def extract_layouts(self):
        f = open(self.pdf_file, 'rb')
        self.parser = PDFParser(f)
        self.document = PDFDocument(self.parser)
        if not self.document.is_extractable:
            raise PDFTextExtractionNotAllowed
        self.rsrcmgr = PDFResourceManager()
        self.laparams = LAParams()
        self.device = PDFPageAggregator(self.rsrcmgr, laparams=self.laparams)
        self.interpreter = PDFPageInterpreter(self.rsrcmgr, self.device)

        for page in PDFPage.create_pages(self.document):
            self.interpreter.process_page(page)
            layout = self.device.get_result()

            (x0, y0, x1, y1) = page.mediabox
            w = int(x1 - x0)
            h = int(y1 - y0)
            # print(page.mediaBox)
            self.page_size.append((w, h))
            self._layouts.append((layout,w,h))
        f.close()

    def extract_textline(self):
        for i,(layout,witdh,height) in enumerate(self._layouts):
            lines = []
            for obj in layout._objs:
                if isinstance(obj, LTTextLineHorizontal):
                    line = _make_line_obj(obj,witdh,height)
                    if len(line['text'].strip())>0:
                        lines.append(line)
                if isinstance(obj, LTTextBoxHorizontal):
                    for o in obj:
                        if isinstance(o, LTTextLineHorizontal):
                            line = _make_line_obj(o,witdh,height)
                            if len(line['text'].strip()) > 0:
                                lines.append(line)
            sorted_lines = sorted(lines, key=lambda item: (item['y0'], item['x0']), reverse=False)
            if len(sorted_lines)>0:
                if sorted_lines[0]['text'].strip() in [str(i),str(i+1),str(i+1)]:
                    if len(sorted_lines)==1:
                        sorted_lines = sorted_lines[1:]
                    elif sorted_lines[0]['y1']<=sorted_lines[1]['y0']:
                        sorted_lines = sorted_lines[1:]
                elif sorted_lines[-1]['text'].strip() in [str(i),str(i+1),str(i+1)]:
                    if len(sorted_lines)==1:
                        sorted_lines = sorted_lines[:-1]
                    elif sorted_lines[-2]['y1']<=sorted_lines[-1]['y0']:
                        sorted_lines = sorted_lines[:-1]
            self.pages.append({
                'textlines':sorted_lines,
                'width':witdh,
                'height':height,
                'index':i+1,
            })
        return self.pages

def _make_line_obj(pdf_text_line,witdh,height):  # make compatible with PyPDF2
    text = pdf_text_line.get_text() #.strip()
    return {
        "text": text,
        "x0": pdf_text_line.x0,
        "x1": pdf_text_line.x1,
        "y0": height-pdf_text_line.y1,
        "y1": height-pdf_text_line.y0
    }
