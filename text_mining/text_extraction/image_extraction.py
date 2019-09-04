import re
import pytesseract
from PIL import Image
import cv2
import numpy as np
import re
import os

class ImageExtraction:
    def __init__(self, imgpath):
        self.path = imgpath

    def extract(self):
        img = cv2.imread(self.path, 0)
        # img = cv2.imread("C:\mupdf-1.14.0-windows\\158580_TT_20_2010_BCT1.png", 0)
        kernel = np.ones((4, 6), np.uint8)
        erosion = cv2.erode(img, kernel, iterations=10)

        filepath = "\\".join(self.path.split("\\")[:-1])
        # pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

        cv2.imwrite(os.path.join(filepath, 'erosion.jpg'), erosion)
        cv2.imwrite(os.path.join(filepath, 'original.jpg'), img)

        ret, thresh = cv2.threshold(erosion, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.drawContours(img, contours, -1, (0,255,0), 3)
        del contours[0]  # xóa khung viền
        boundingRect = []
        i = 0

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if (h > 40):
                boundingRect.append(np.zeros((4), np.uint8))
                boundingRect[i] = [x, y, w, h]
                i += 1

        boundingRect = boundingRect[::-1]
        if (boundingRect[-1][2] < 200):
            del boundingRect[-1]  # xóa số trang

        i = 0
        # with_signature = False
        # if(with_signature == False):
        for Rect in boundingRect:
            img_ = img[Rect[1]:Rect[1] + Rect[3], Rect[0]:Rect[0] + Rect[2]]
            cv2.imwrite(os.path.join(filepath, 'original_{}.jpg'.format(i)), img_)
            i = i + 1
        n = i
        text = []

        for i in range(0, n):
            text_ = pytesseract.image_to_string(Image.open(os.path.join(filepath, 'original_{}.jpg'.format(i))), lang='vie')
            text.append(text_)
        #    print(text_)s

        # noi_ban_hanh = text[1]
        if (len(text[1]) <= len(text[0])):
            self.noi_ban_hanh = text[1]
        else:
            self.noi_ban_hanh = text[0]

        self.so_van_ban = text[2]
        pattern = r'S\w{1,2}:\s*'
        temp = re.search(pattern, self.so_van_ban)
        self.so_van_ban = self.so_van_ban[temp.end():]

        thoi_gian_dia_diem = text[3]
        loai_vb_trich_yeu = text[4]

        can_cu_yeu_cau = '\n'.join(text[5:-3])
        pattern = r'\n *(PHẦN|CHƯƠNG|Chương|Mục|Điều)\s1[\.\,\:]'
        temp = re.search(pattern, can_cu_yeu_cau)
        can_cu_yeu_cau = can_cu_yeu_cau[:temp.start()]
        self.can_cu = " ".join(can_cu_yeu_cau.split(';')[:-1])
        self.yeu_cau = can_cu_yeu_cau.split(';')[-1]
        self.thoi_gian = thoi_gian_dia_diem.split(',')[1]
        self.dia_diem = thoi_gian_dia_diem.split(',')[0]
        self.loai_van_ban = loai_vb_trich_yeu.splitlines()[0]
        self.trich_yeu = " ".join(loai_vb_trich_yeu.splitlines()[1:])

        self.noi_nhan = text[-2]
        if (len(self.noi_nhan) < 30):
            self.noi_nhan = text[-3]
        if (len(self.noi_nhan) < 30):
            self.noi_nhan = text[-4]

        text = ''
        text += 'NƠI BAN HÀNH: ' + self.noi_ban_hanh + 2*'\n'
        text += 'SỐ VĂN BẢN: ' + self.so_van_ban + 2*'\n'
        text += 'ĐỊA ĐIỂM: ' + self.dia_diem + 2*'\n'
        text += 'THỜI GIAN: ' + self.thoi_gian + 2*'\n'
        text += 'LOẠI VĂN BẢN: ' + self.loai_van_ban + 2*'\n'
        text += 'TRÍCH YẾU NỘI DUNG: ' + self.trich_yeu + 2*'\n'
        text += 'CÁC CĂN CỨ: ' + self.can_cu + 2*'\n'
        text += 'YÊU CẦU CỦA: ' + self.yeu_cau + 2*'\n'
        text += 'CÁC NƠI NHẬN: ' + self.noi_nhan + 2*'\n'
        self._info = text

    def Info(self):
        text = ''
        text += 'NƠI BAN HÀNH: ' + self.noi_ban_hanh + '\n'
        text += 'SỐ VĂN BẢN: ' + self.so_van_ban + '\n'
        text += 'ĐỊA ĐIỂM: ' + self.dia_diem + '\n'
        text += 'THỜI GIAN: ' + self.thoi_gian + '\n'
        text += 'LOẠI VĂN BẢN: ' + self.loai_van_ban + '\n'
        text += 'TRÍCH YẾU NỘI DUNG: ' + self.trich_yeu + '\n'
        text += 'CÁC CĂN CỨ: ' + self.can_cu + '\n'
        text += 'YÊU CẦU CỦA: ' + self.yeu_cau + '\n'
        text += 'CÁC NƠI NHẬN: ' + self.noi_nhan + '\n'
        self._info = text
        return text
