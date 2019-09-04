import re
from database import DataBase
from preprocess.preprocess import process_text
class Extraction:
    def __init__(self, corpus):
        self.corpus = corpus
        self.remove_quoc_hieu()

    def remove_quoc_hieu(self):
        quoc_hieu = []
        quoc_hieu.append(r'C\w{1,2}NG\s*H\w{2,4}\s*X\w{1,2}\s*H\w{1,2}I\s*CH\w{1,2}\s*NGH\w{1,2}A\s*VI\w{1,2}T\s*NAM')
        quoc_hieu.append(r'\w{2,4}c *l\w{1,2}p *[-–] *T\w{1,2} *do *[-–] *H\w{1,2}nh *ph\w{1,2}c')
        pattern = '|'.join(quoc_hieu)
        doan_dau_vb = self.corpus[:200]
        doan_dau_vb = re.sub(pattern, '', doan_dau_vb)
        self.corpus = ''.join([doan_dau_vb, self.corpus[200:]])

    def detect_so_van_ban_nbh(self):
        # pattern = r'S\w{1,2}\:\s*[\w\/\-\–]+\s'
        pattern = r'S\w{1,2}\:\s*[\w\-\–]+ *(?:\/ *[\w\-\–]+)+'
        temp = re.findall(pattern, self.corpus[:300])
        if len(temp) == 0:
            pattern = r'Luật +số\: *[\w\/\-\–]+\s'
            temp = re.findall(pattern, self.pages[0])
        if len(temp) == 0:
            return "", ""
        else:
            self.so_van_ban = temp[0]
        doan_dau_vb = self.corpus[:self.corpus.find(self.so_van_ban)]
        self.noi_ban_hanh = self.detect_noi_ban_hanh(doan_dau_vb)
        self.corpus = ''.join([self.corpus[:200].replace(self.so_van_ban, ''), self.corpus[200:]])
        self.so_van_ban = re.sub(r'\s{2,}', ' ', self.so_van_ban).strip()
        self.so_van_ban = self.so_van_ban[self.so_van_ban.find(':') + 1:].strip().replace(' ', '')
        return self.so_van_ban, self.noi_ban_hanh

    def detect_noi_ban_hanh(self, doan_dau_vb):
        self.corpus = self.corpus.replace(doan_dau_vb, '', 1)
        dd, tg = self.detect_place_date()
        if dd != '':
            doan_dau_vb = doan_dau_vb[:doan_dau_vb.find(dd)]
        doan_dau_vb = doan_dau_vb.replace('_', '')
        pattern = r'[\w\s]+'
        nbh = re.findall(pattern, doan_dau_vb)
        if len(nbh)>0:
            nbh = nbh[0]
        else:
            nbh=''
        return nbh.strip()

    def detect_place_date(self):
        pattern = r'(?:Th\w{1,2}nh *ph\w{1,2} *)?[A-Z][^A-Z\W]+(?:\s[A-Z][^A-Z\W]+)*, *ng\w{2,4} *\d+ *th\w{1,2}ng *\d+ *n\w{1,2}m *\d+'
        _temp = re.findall(pattern, self.corpus[:300])
        if len(_temp) == 0:
            return "", ""
        else:
            self.place_date = _temp[0]
        self.corpus = ''.join([self.corpus[:300].replace(self.place_date, '', 1), self.corpus[300:]])
        self.place_date = re.sub(r'\s{2,}', ' ', self.place_date)
        index = self.place_date.find(',')
        self.dia_diem = self.place_date[:index]
        temp = self.place_date[index:]
        num = re.findall(r'\d+', temp)
        self.thoi_gian = '/'.join([item for item in num])
        return self.dia_diem, self.thoi_gian

    def cut_noi_dung(self):
        pattern = r'\n *(?:PHẦN|CHƯƠNG|Chương|Mục|Điều) *[IVX\d]+ *\n'
        temp = re.search(pattern, self.corpus)
        self.doan_dau = self.corpus[:temp.start()]
        self.noi_dung = self.corpus[temp.start():]

    def detect_tieu_de(self):
        temp = re.search(r'[^0-9a-z_\W]', self.corpus[:100])
        self.corpus = self.corpus[temp.start():]
        pattern_lvb = r'[^0-9a-z\W][^0-9a-z\W]+(?: [^0-9a-z\W][^0-9a-z\W]+)*(?:\d|(?: *\n))'
        self.loai_van_ban = re.findall(pattern_lvb, self.corpus[:100])
        self.corpus = ''.join([self.corpus[:100].replace(self.loai_van_ban[0], ''), self.corpus[100:]])
        self.loai_van_ban = re.sub(r'\d', '', self.loai_van_ban[0]).strip()
        # print(self.corpus[:200])
        return self.loai_van_ban

    def detect_noi_nhan(self):
        index = self.noi_dung.rfind('Nơi nhận:')
        doan_cuoi_vb = self.noi_dung[index:]
        self.noi_dung = self.noi_dung.replace(doan_cuoi_vb, '')
        self.noi_dung = self.noi_dung.replace('XÁC THỰC VĂN BẢN HỢP NHẤT', '')
        doan_cuoi_vb = doan_cuoi_vb.replace('(đã ký)', '')
        doan_cuoi_vb = doan_cuoi_vb.replace('(Đã ký)', '')
        doan_cuoi_vb = doan_cuoi_vb.replace('THỨ TRƯỞNG', '')
        # index = doan_cuoi_vb.rfind('.')
        # doan_cuoi_vb = doan_cuoi_vb[:index] + doan_cuoi_vb[index:].replace('.', ';')
        pattern = r'[-–]\s*[\w\,\.\-\:\(\) \n]+\;'
        noi_nhan_tmp = re.findall(pattern, doan_cuoi_vb)
        if len(noi_nhan_tmp)>0 and noi_nhan_tmp[-1].find('Lưu') > -1:
            noi_nhan_tmp = noi_nhan_tmp[:-1]
        self.noi_nhan = []
        for item in noi_nhan_tmp:
            # doan_cuoi_vb = doan_cuoi_vb.replace(item, '')
            self.noi_nhan.append(re.sub(r' {2,}', ' ' , re.sub(r'\n+', ' ', re.sub(r'[-–]\s*', '', item))).replace(';', ''))
        pattern_Luu = r'Lưu\: *[\w\,\&\.\-\–\:\;\(\) ]+(?:\n| {2,})'
        temp = re.findall(pattern_Luu, doan_cuoi_vb)[0].strip()
        self.noi_nhan.append(re.split(r'\s{2,}', temp, 1)[0])
        return self.noi_nhan

    def detect_noi_dung(self):
        # self.detect_chuong()
        # self.in_ra_du_lieu_phan_cap()
        open('output/text', 'w', encoding='utf-8').write(self.noi_dung)
        self.data = Item(self.noi_dung)
        return self.data

    def remove_line(self):
        self.pages = [re.sub('-{5,}', '\n', page) for page in self.pages]

    def detect_footer(self):
        pass

all_pattern = [
    (r'Chương *[IVX]+', "Chương"),  # Chương
    (r'Mục *\d+', "Mục"),  # Mục
    (r'\n *Điều *\d+[\.\:]', "Điều"),  # Điều
    (r'\n *\d{1,2}\.\d* ', "Khoản"),  # Khoản
    (r'\n *[a-zđ]\)\d* ', "Điểm"),  # Điểm
    (r'\n *[a-zđ]\.\d+\)\d* ', "Hạ Điểm"),  # Hạ điểm
    # (r'[\.\;\:\?]{1} *\n+ *[-–]{1} *', "Hạ điểm"),
]
class Item:
    def __init__(self,content,item_type=0,stt='',type='Text'):
        self.stt = stt.strip()
        self.item_type = item_type
        self.type = type
        self.content = content.strip()
        self.tieu_de = ""
        self.childrents = []

        if item_type<len(all_pattern) and len(self.content)>1:
            print('analisys',self.stt)
            self.pattern = all_pattern[item_type][0]
            # self.type = all_pattern[item_type][1]
            self.analisys_content()
            self.has_data = True
        else:
            self.has_data = False
        self.tokens = process_text(self.content)

    def analisys_content(self):
        pattern_tieu_de = r'[^\n]+'
        if self.stt != '' and self.item_type<4:
            self.tieu_de = re.search(pattern_tieu_de, self.content).group().strip()
            self.content = re.sub(pattern_tieu_de,'',self.content,count=1)
        for i in range(self.item_type,len(all_pattern)):
            stt_childents = re.findall(all_pattern[i][0], self.content)
            if len(stt_childents)>0:
                print('found',stt_childents)
                childrent_type = all_pattern[i][1]
                childrents = re.split(all_pattern[i][0],self.content)
                self.content = childrents[0]
                childrents = childrents[1:]
                for stt,text in zip(stt_childents,childrents):
                    # if text.strip()!='' or stt.strip()!='':
                    self.childrents.append(Item(text,i+1,stt,childrent_type))
                break

    def print(self,pad_current = '',pad=' ',print_content=True,display=True):
        text = '{0}{1}: {2}'.format(pad_current,self.stt.strip().rstrip(':.,)'),self.tieu_de.strip())
        if display:
            print(text)
        if print_content:
            content = '{0}{1}{2}'.format(pad_current,pad,self.content.strip())
            if display:
                print(content)
            text +='\n'+content
        for childrent in self.childrents:
            child_content = childrent.print(pad_current+pad,pad,print_content)
            text +='\n'+child_content
        return text

    def get_content(self,tokenized=False):
        if tokenized:
            content = self.tokens.strip()
        else:
            content = self.content.strip()
        for childrent in self.childrents:
            child_content = childrent.get_content(tokenized)
            content +=' '+ child_content
        return content

    def to_json(self):
        return {
            'stt': self.stt,
            'tieu_de': self.tieu_de,
            'type': self.type,
            'content': self.content,
            'childrents': [childrent.to_json() for childrent in self.childrents]
        }

    def to_database(self,database=None,parent=None,table='content',parent_ref='',title_ref = ''):
        if database==None:
            database = DataBase()
        reference = '{0}/{1}'.format(parent_ref.strip().rstrip(':.,)/\\'),self.stt.strip().rstrip(':.,)'))
        if len(self.tieu_de.strip())>0:
            if len(title_ref.strip())>0:
                tieu_de = '{0} | {1}'.format(title_ref.strip(),self.tieu_de.strip())
            else:
                tieu_de = self.tieu_de.strip()
        else:
            tieu_de = title_ref
        record = {
            'parent': parent,
            'stt': self.stt.strip(),
            'type': self.type,
            'tieu_de': tieu_de,
            'content': self.content.strip(),
            'reference':reference,
            'tokens':self.tokens
        }
        parent = database.insert(record,table=table)
        for childrent in self.childrents:
            childrent.to_database(database,parent,table=table,parent_ref=reference,title_ref=tieu_de)
        return database

