import re

from preprocess.preprocess import process_text
from .text_extraction.extraction import Extraction
import os
from .utils.pdf_reader import PDFAnalyzer


class TextMining:

    def __init__(self, path, tmp_path='output'):
        self.path = path.replace('\\', '/')
        pdf = PDFAnalyzer(path)
        self.pages = []
        for i, page in enumerate(pdf.pages):
            print('----------------')
            print(page['textlines'])
            text = ' '.join([textline['text'] for textline in page['textlines']])
            self.pages.append(text)

    def extraction(self):
        extObj = Extraction(self.pages)
        self.pages = extObj.pages
        self.so_van_ban, self.noi_ban_hanh = extObj.detect_so_van_ban_nbh()
        self.dia_diem, self.thoi_gian = extObj.detect_place_date()
        self.loai_ban_ban, self.trich_yeu_nd = extObj.detect_tieu_de()
        self.can_cu = extObj.detect_can_cu()
        self.yeu_cau = extObj.detect_yeu_cau()
        self.phu_luc = extObj.detect_phu_luc()
        self.quy_che = extObj.detect_quy_che()
        self.noi_nhan = extObj.detect_noi_nhan()
        self.thoi_gian_ban_hanh = extObj.remove_chu_ki()
        self.data = extObj.detect_noi_dung()
        self.text = extObj.text

    def Info(self):
        strings = ""
        strings = strings + "NƠI BAN HÀNH: " + self.noi_ban_hanh
        strings += '\n'
        strings = strings + "\nSỐ VĂN BẢN: " + self.so_van_ban
        strings += '\n'
        strings = strings + "\nĐỊA ĐIỂM: " + self.dia_diem
        strings += '\n'
        strings = strings + "\nTHỜI GIAN: " + self.thoi_gian
        strings += '\n'
        strings = strings + "\nLOẠI VĂN BẢN: " + self.loai_ban_ban
        strings += '\n'
        strings = strings + "\nTRÍCH YẾU NỘI DUNG: " + self.trich_yeu_nd
        strings += '\n'
        strings = strings + "\nCÁC CĂN CỨ:"
        for item in self.can_cu:
            strings = strings + "\n    " + item
        strings += '\n'
        strings = strings + "\nYÊU CẦU CỦA:\n" + self.yeu_cau
        strings += '\n'
        strings += "\nCÁC NƠI NHẬN:"
        for item in self.noi_nhan:
            strings = strings + "\n    + " + item
        strings += '\n'
        if self.phu_luc == -1:
            strings = strings + "\nKHÔNG CÓ PHỤ LỤC!"
        else:
            strings = strings + self.phu_luc
        strings += '\n'
        if self.quy_che == -1:
            strings = strings + "\nKHÔNG CÓ QUY CHẾ!"
        else:
            strings = strings + self.quy_che
        strings += '\n\nMỤC LỤC\n'
        strings += self.data.print(pad='    ', print_content=False)
        self._info = strings
        return strings

    def to_record(self):
        strings = self.data.print(pad='    ', print_content=False, display=False)
        cac_de_muc = re.findall(r'\: [\w \,\.]+\n', strings)
        for i in range(len(cac_de_muc)):
            cac_de_muc[i] = cac_de_muc[i][1:-1]
        # print("\"" + textObj.trich_yeu_nd + "\"")  # textObj.trich_yeu_nd la cai tieu de
        # print(cac_de_muc)               #cac_de_muc la list cua cac subtitle
        content = self.data.get_content(tokenized=True)
        # for item in cac_de_muc:
        #     content = content.replace(item, '')
        subtitle = ' '.join([process_text(demuc) for demuc in cac_de_muc])
        # dictionary = {'title': self.trich_yeu_nd, 'subtitle': cac_de_muc, 'content': content}

        return {'Loại văn bản': self.loai_ban_ban, 'Nơi ban hành': self.noi_ban_hanh,
                'Số văn bản': self.so_van_ban, 'Địa điểm': self.dia_diem, 'Thời gian': self.thoi_gian,
                'Trích yếu nội dung': self.trich_yeu_nd, 'Căn cứ': self.can_cu, 'Nơi nhận': self.noi_nhan,
                'Phụ lục': self.phu_luc, 'Yêu cầu': self.yeu_cau,
                'path': self.path, 'title': process_text(self.trich_yeu_nd), 'subtitle': subtitle, 'content': content}

    def to_json(self):
        return {'Loại văn bản': self.loai_ban_ban, 'Nơi ban hành': self.noi_ban_hanh,
                'Số văn bản': self.so_van_ban, 'Địa điểm': self.dia_diem, 'Thời gian': self.thoi_gian,
                'Trích yếu nội dung': self.trich_yeu_nd, 'Căn cứ': self.can_cu, 'Nơi nhận': self.noi_nhan,
                'Yêu cầu': self.yeu_cau, 'Nội dung': self.data.to_json()['children']}

    def classification(self):
        pass

    def print(self, pad=' '):
        print("Nơi ban hành: " + self.noi_ban_hanh)
        print("Số văn bản: " + self.so_van_ban)
        print("Địa điểm: " + self.dia_diem)
        print("Thời gian: " + self.thoi_gian)
        print("Loại văn bản: " + self.loai_ban_ban)
        print("Trích yếu nội dung: " + self.trich_yeu_nd)
        print("Căn cứ:")
        for can_cu in self.can_cu:
            print('\t{0}'.format(can_cu))
        print("Yêu cầu: " + self.yeu_cau)
        print("----------------------------------------------")
        self.data.print(pad=pad)
        if self.noi_nhan != "":
            print("Các nơi nhận:")
            for item in self.noi_nhan:
                print(" + " + item)
        if self.thoi_gian_ban_hanh != "":
            print("Thời gian ban hành:\n\t" + self.thoi_gian_ban_hanh)
        if len(self.phu_luc) > 0:
            print('Phụ lục:')
            print(self.phu_luc)
        if len(self.quy_che) > 0:
            print('Quy chế:')
            print(self.quy_che)
