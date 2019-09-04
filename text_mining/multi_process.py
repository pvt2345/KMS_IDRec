from multiprocessing import Pool
from .utils.file_convert import to_pdf
from text_mining.text_mining import TextMining
from threading import Thread
import multiprocessing as mp
def process_one_pdf(pdf_path):
    obj = TextMining(pdf_path)
    obj.extraction()
    obj.Info()
    return obj
    # return {'Loại văn bản': loai_ban_ban, 'Nơi ban hành': noi_ban_hanh,
    #         'Số văn bản': so_van_ban, 'Địa điểm': dia_diem,'Thời gian':thoi_gian,
    #         'Trích yếu nội dung': trich_yeu_nd, 'Căn cứ': can_cu, 'Nơi nhận': noi_nhan,
    #         'Phụ lục': phu_luc, 'Yêu cầu': yeu_cau,'Quy chế':quy_che,'Thời gian ban hành':thoi_gian_ban_hanh,
    #         'text':text,
    #         'data':data}



class DatabaseThread(Thread):
    def __init__(self,database,path):
        Thread.__init__(self)
        self.db= database
        self.path = path
        # self.i = i
    def run(self):
        print(self.path)
        process_one_pdf(self.path)['data'].to_database(self.db)
        print(self.path)

class MultiExtractor:
    def __init__(self,number_process=None,temp='output'):
        if number_process==None:
            number_process = max(mp.cpu_count()-2,1)
        self.number_process = number_process
        # self.database = DataBase()
        self.temp = temp

    def extract(self,paths):
        if isinstance(paths,str):
            paths = [paths]
        pdf_paths = to_pdf(paths,self.temp)
        self.pool = Pool(self.number_process)
        datas = self.pool.map(process_one_pdf,pdf_paths)
        self.pool.close()
        return datas



