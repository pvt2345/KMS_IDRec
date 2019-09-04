import os
import sys
import threading
from multiprocessing import cpu_count
from pathlib import Path

from PyQt5 import QtWidgets

from database import DataBase
from text_mining.multi_process import MultiExtractor
from text_mining.text_extraction.image_extraction import ImageExtraction


# from PyQt5 import QtWidgets, QtGui
class TimerThread(threading.Thread):
    def __init__(self, parentProgressBar: QtWidgets.QProgressBar, estimated_time):
        threading.Thread.__init__(self)
        self.parentProgressBar = parentProgressBar
        self.estimated_time = estimated_time
        self.step = 0

    def run(self):
        while (self.step < 100):
            self.step = self.step + 0.000125 / self.estimated_time
            self.parentProgressBar.setValue(self.step)
        self.parentProgressBar.setValue(100)


class TextMining_UI(QtWidgets.QWidget):
    def __init__(self):
        super(TextMining_UI, self).__init__()
        self.btn_SelectFile = QtWidgets.QPushButton('Chọn tệp')
        self.btn_SaveFile = QtWidgets.QPushButton('Lưu vào database')
        self.init_UI()
        self.extractor = MultiExtractor()

    def init_UI(self):
        self.label_ThongTin = QtWidgets.QLabel('Các trường được trích xuất từ văn bản: ')
        self.txt_ThongTin = QtWidgets.QTextEdit()
        self.progressBar = QtWidgets.QProgressBar()
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.setMinimumContentsLength(50)
        self.label_DanhSachVanBan = QtWidgets.QLabel('Danh sách các văn bản: ')
        self.comboBox.currentIndexChanged.connect(self.comboBox_indexChange)

        h_box_lbl_ThongTin = QtWidgets.QHBoxLayout()
        h_box_lbl_ThongTin.addStretch()
        h_box_lbl_ThongTin.addWidget(self.label_ThongTin)
        h_box_lbl_ThongTin.addStretch()

        h_box_btn_SaveFile = QtWidgets.QHBoxLayout()
        h_box_btn_SaveFile.addStretch()
        h_box_btn_SaveFile.addWidget(self.btn_SaveFile)

        h_box_comboBox = QtWidgets.QHBoxLayout()
        h_box_comboBox.addWidget(self.label_DanhSachVanBan)
        h_box_comboBox.addWidget(self.comboBox)
        h_box_comboBox.addStretch()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.btn_SelectFile)
        v_box.addWidget(self.progressBar)
        v_box.addLayout(h_box_comboBox)
        v_box.addLayout(h_box_lbl_ThongTin)
        v_box.addWidget(self.txt_ThongTin)
        v_box.addLayout(h_box_btn_SaveFile)

        self.btn_SelectFile.clicked.connect(self.btn_SelectFile_click)
        self.btn_SaveFile.clicked.connect(self.btn_SaveFile_click)

        self.setLayout(v_box)
        self.setWindowTitle('Text Mining')
        self.show()

    def comboBox_indexChange(self, i):
        try:
            self.txt_ThongTin.setText(self.textObj[i]._info)
        except:
            pass

    def btn_SelectFile_click(self):
        filename = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select File', str(Path.home()),
                                                          filter="Portable Document Format, Scanned File *.pdf *.doc *.docx *.jpg *.png")
        if (filename[0] != ''):
            if (filename[0][0].split('.')[-1] != 'pdf'):
                self.txt_ThongTin.setText(' ')
                self.progressBar.setValue(0)
                self.textObj = []

                for item in filename[0]:
                    self.textObj.append(ImageExtraction(item))
                estimated_time = len(self.textObj) * 29
                self.timerthread = TimerThread(parentProgressBar=self.progressBar, estimated_time=estimated_time)
                self.timerthread.start()
                for item in self.textObj:
                    item.extract()
                    self.comboBox.addItem(item.loai_van_ban + ' ' + item.so_van_ban)
                self.txt_ThongTin.setText(self.textObj[0]._info)
                self.timerthread.join()
            else:
                # lấy estimated time theo số trang
                self.txt_ThongTin.setText(' ')
                self.progressBar.setValue(0)
                sum = 0
                for item in filename[0]:
                    size = os.path.getsize(item)
                    print(size)
                    ext = item.rsplit('.')[-1]
                    if ext in ['doc', 'docx']:
                        size *= 5
                        size += 1000
                    sum += size / 80000
                sum /= max(cpu_count() - 2, 2) / 2
                estimated_time = sum * 1.1
                if (estimated_time > 0):
                    self.textObj = []
                    self.comboBox.clear()
                    self.timerthread = TimerThread(parentProgressBar=self.progressBar, estimated_time=estimated_time)
                    self.timerthread.start()

                    self.textObj = self.extractor.extract(filename[0])

                    for item in self.textObj:
                        self.comboBox.addItem(item.loai_ban_ban + ' ' + item.so_van_ban)
                    if len(self.textObj) > 0:
                        self.txt_ThongTin.setText(self.textObj[0]._info)
                    self.timerthread.join()
                    # return

    def btn_SaveFile_click(self):
        filename = [
            'save']  # QtWidgets.QFileDialog.getSaveFileName(self, 'Select File', str(Path.home()), filter="Excel File *.xlsx *.xls")
        if (filename[0] != ''):
            database = DataBase()
            # database.create_table('info')
            # database.create_table('content',columns=['id', 'parent', 'type', 'stt', 'tieu_de', 'content'])
            for obj in self.textObj:
                if database.insert(obj.to_record(), table='info') != -1: #insert thành công info
                    obj.data.to_database(database, parent=obj.so_van_ban, table='content', parent_ref=obj.so_van_ban,
                                         title_ref=obj.trich_yeu_nd)

            print('writing...')

            # if(os.path.exists(filename[0])):
            #     open(filename[0], 'a').close()

            # write = pd.ExcelWriter(filename[0], engine='xlsxwriter')
            # database.to_excel(write, 'Sheet1')
            # write.close()
            database.save()
            print('write to {0}'.format(filename[0]))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    TextMining_Window = TextMining_UI()
    sys.exit(app.exec_())
