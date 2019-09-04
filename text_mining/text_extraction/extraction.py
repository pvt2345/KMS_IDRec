import re

from database import DataBase
from preprocess.preprocess import process_text


class Extraction:
    def __init__(self, pages):
        self.pages = pages
        self.remove_quoc_hieu()
        self.result = {
            'meta_data': {
                'date': None,
                'company': None,
                'document_number': None,
                'document_type': None,
                'person_sign': None,
                'address': None
            },
            'content': {
                'item 1': {
                    'paragraph': {
                        'sub_paragraph': None
                    }
                }
            }
        }

    def remove_quoc_hieu(self):
        quoc_hieu = []
        quoc_hieu.append(r'C\w{1,2}NG\s*H\w{2,4}\s*X\w{1,2}\s*H\w{1,2}I\s*CH\w{1,2}\s*NGH\w{1,2}A\s*VI\w{1,2}T\s*NAM')
        quoc_hieu.append(r'\w{2,4}c *l\w{1,2}p *[-–] *T\w{1,2} *do *[-–] *H\w{1,2}nh *ph\w{1,2}c')
        pattern = '|'.join(quoc_hieu)
        self.pages[0] = re.sub(pattern, '', self.pages[0])

    def detect_so_van_ban_nbh(self):
        # pattern = r'S\w{1,2}\:\s*[\w\/\-\–]+\s'
        pattern = r'S\w{1,2}\:\s*[\w\-\–]+ *(?:\/ *[\w\-\–]+)+'
        temp = re.findall(pattern, self.pages[0])
        if len(temp) == 0:
            pattern = r'Luật +số\: *[\w\/\-\–]+\s'
            temp = re.findall(pattern, self.pages[0])
        if len(temp) == 0:
            return "", ""
        else:
            self.so_van_ban = temp[0]
        doan_dau_vb = self.pages[0][:self.pages[0].find(self.so_van_ban)]
        self.noi_ban_hanh = self.detect_noi_ban_hanh(doan_dau_vb)
        self.pages[0] = self.pages[0].replace(self.so_van_ban, '')
        self.so_van_ban = re.sub(r'\s{2,}', ' ', self.so_van_ban).strip()
        self.so_van_ban = self.so_van_ban[self.so_van_ban.find(':') + 1:].strip().replace(' ', '')
        return self.so_van_ban, self.noi_ban_hanh

    def detect_noi_ban_hanh(self, doan_dau_vb):
        self.pages[0] = self.pages[0].replace(doan_dau_vb, '')
        doan_dau_vb = doan_dau_vb.replace('_', '')
        pattern = r'[\w\s]+'
        nbh = re.findall(pattern, doan_dau_vb)
        if len(nbh) > 0:
            nbh = nbh[0]
        else:
            nbh = ''
        return nbh.strip()

    def detect_place_date(self):
        pattern = r'(?:Th\w{1,2}nh *ph\w{1,2} *)?[A-Z][^A-Z\W]+(?:\s[A-Z][^A-Z\W]+)*, *ng\w{2,4} *\d+ *th\w{1,2}ng *\d+ *n\w{1,2}m *\d+'
        _temp = re.findall(pattern, self.pages[0])
        if len(_temp) == 0:
            return "", ""
        else:
            self.place_date = _temp[0]
        self.pages[0] = self.pages[0].replace(self.place_date, '')
        self.place_date = re.sub(r'\s{2,}', ' ', self.place_date)
        index = self.place_date.find(',')
        self.dia_diem = self.place_date[:index]
        temp = self.place_date[index:]
        num = re.findall(r'\d+', temp)
        self.thoi_gian = '/'.join([item for item in num])
        return self.dia_diem, self.thoi_gian

    def detect_tieu_de(self):
        # # xoa so trang o dau (neu co)
        # temp_d = re.search(r'\d', self.pages[0])
        # temp_w = re.search(r'[^0-9\s\-\–]', self.pages[0])
        # if temp_d.start() < temp_w.start():
        #     self.pages[0] = re.subn(r'\d', '', self.pages[0], 1)[0]
        temp = re.search(r'[^0-9a-z\_\W]', self.pages[0])
        self.pages[0] = self.pages[0][temp.start():]
        pattern_lvb = r'[^a-z\W][^a-z\W]+(?: [^a-z\W][^a-z\W]+)*\s*\n'
        self.loai_van_ban = re.findall(pattern_lvb, self.pages[0])
        self.loai_van_ban = self.loai_van_ban[0].strip()
        self.pages[0] = self.pages[0].replace(self.loai_van_ban, '')
        pattern_ty_nd = r'[\w][\w\s\&\,\.\\\/\-\–\'\"\“\”]+Căn'
        self.trich_yeu_nd = re.findall(pattern_ty_nd, self.pages[0])[0]
        self.trich_yeu_nd = re.sub(r'[-–]{3,}', '', self.trich_yeu_nd)
        index = self.trich_yeu_nd.rfind('Căn')
        self.trich_yeu_nd = self.trich_yeu_nd[:index - 1].strip()
        self.pages[0] = self.pages[0].replace(self.trich_yeu_nd, '')
        self.trich_yeu_nd = re.sub(r'\s{2,}', ' ', self.trich_yeu_nd)
        ch = re.search(r'\w', self.pages[0])
        self.pages[0] = self.pages[0][ch.start():]
        return self.loai_van_ban, self.trich_yeu_nd

    def detect_can_cu(self):
        pattern_doan_dau = r'(?:\.|\:|,)\s+(?:PHẦN|CHƯƠNG|Chương|Mục|Điều)+'
        temp = re.search(pattern_doan_dau, self.pages[0])
        doan_dau_vb = self.pages[0][:temp.start()]
        pattern = r'Căn *cứ[\w\s\&\/\\\.\,\-\–\'\"\“\”]+\;|Luật *[\w\s\&\/\\\.\,\-\–\'\"\“\”]+\;'
        can_cu_temp = re.findall(pattern, doan_dau_vb)
        self.can_cu = []
        for item in can_cu_temp:
            self.pages[0] = self.pages[0].replace(item, '')
            can_cu = re.sub(r'Căn *cứ *', '', item)
            can_cu = re.sub(r'\n', ' ', can_cu)
            can_cu = re.sub(r' {2,}', ' ', can_cu)
            pattern_temp = r'[sS]ố\s+(?:[\w\-\–]+\/)+[\w\-\–]+'
            chuoi_so = re.findall(pattern_temp, can_cu)
            for obj in chuoi_so:
                xau = re.sub(r'[sS]ố\s+', '', obj)
                can_cu = can_cu.replace(xau, "*" + xau + "#")
            self.can_cu.append(can_cu)
        return self.can_cu

    def detect_yeu_cau(self):
        pattern = r'(?:\.|\:|,)\s+(?:PHẦN|CHƯƠNG|Chương|Mục|Điều)+'
        temp = re.search(pattern, self.pages[0])
        self.yeu_cau = self.pages[0][:temp.start()]
        self.pages[0] = self.pages[0].replace(self.yeu_cau, '')
        self.yeu_cau = re.sub(r'\s{2,}', ' ', self.yeu_cau.strip())
        return self.yeu_cau

    def detect_phu_luc(self):
        # # old code
        # self.text = '\n'.join(self.pages)
        # index = self.text.find('PHỤ LỤC')
        # if index == -1:
        #     index = self.text.find('DANH MỤC')
        #     if index == -1:
        #         return ''
        #     else:
        #         self.phu_luc = self.text[index:]
        #         self.text = self.text.replace(self.phu_luc, '')
        #         return self.phu_luc.strip()
        # else:
        #     self.phu_luc = self.text[index:]
        #     self.text = self.text.replace(self.phu_luc, '')
        #     return self.phu_luc.strip()

        # new code
        for idx, page in enumerate(self.pages):
            index = page.find('PHỤ LỤC')
            if index == -1:
                index = page.find('DANH MỤC')
                if index == -1:
                    if idx == len(self.pages) - 1:
                        return ''
                else:
                    self.phu_luc = '\n'.join([page[index:]] + self.pages[idx + 1:])
                    self.pages = self.pages[:idx] + [page[:index]]
                    return self.phu_luc.strip()
            else:
                self.phu_luc = '\n'.join([page[index:]] + self.pages[idx + 1:])
                self.pages = self.pages[:idx] + [page[:index]]
                return self.phu_luc.strip()

    def detect_quy_che(self):
        # # old code
        # pattern = r'\n *QUY CHẾ *\n'
        # temp = re.search(pattern, self.text)
        # if temp is None:
        #     return ''
        # self.quy_che = self.text[temp.start():].strip()
        # self.text = self.text[:temp.start()]
        # return self.quy_che

        # new code
        pattern = r'\n *QUY CHẾ *\n'
        for idx, page in enumerate(self.pages):
            temp = re.search(pattern, page)
            if temp is None:
                if idx == len(self.pages) - 1:
                    return ''
            else:
                self.quy_che = '\n'.join([[page[temp.start():]] + self.pages[idx + 1:]])
                self.pages = self.pages[:idx] + [page[:temp.start()]]
                return self.quy_che

    def detect_noi_nhan(self):
        # # old code
        # if self.loai_van_ban == "LUẬT":
        #     return ""
        # index = self.text.rfind('Nơi nhận:')
        # doan_cuoi_vb = self.text[index:]
        # self.text = self.text.replace(doan_cuoi_vb, '')
        # doan_cuoi_vb = doan_cuoi_vb.replace('(đã ký)', '')
        # doan_cuoi_vb = doan_cuoi_vb.replace('(Đã ký)', '')
        # # index = doan_cuoi_vb.rfind('.')
        # # doan_cuoi_vb = doan_cuoi_vb[:index] + doan_cuoi_vb[index:].replace('.', ';')
        # pattern = r'[-–]\s*[\w\,\.\-\:\(\) \n]+\;'
        # noi_nhan_tmp = re.findall(pattern, doan_cuoi_vb)
        # if len(noi_nhan_tmp) > 0 and noi_nhan_tmp[-1].find('Lưu') > -1:
        #     noi_nhan_tmp = noi_nhan_tmp[:-1]
        # self.noi_nhan = []
        # for item in noi_nhan_tmp:
        #     # doan_cuoi_vb = doan_cuoi_vb.replace(item, '')
        #     self.noi_nhan.append(
        #         re.sub(r'\ {2,}', ' ', re.sub(r'\n+', ' ', re.sub(r'[-–]\s*', '', item))).replace(';', ''))
        # pattern_Luu = r'Lưu\: *[\w\,\&\.\-\–\:\;\(\) ]+(?:\n| {2,})'
        # temp = re.findall(pattern_Luu, doan_cuoi_vb)[0].strip()
        # self.noi_nhan.append(re.split(r'\s{2,}', temp, 1)[0])
        # return self.noi_nhan

        # new code
        if self.loai_van_ban == "LUẬT":
            return ""
        for i in range(len(self.pages) - 1, -1, -1):
            index = self.pages[i].rfind('Nơi nhận:')
            if index == -1:
                continue
            try:
                doan_cuoi_vb = '\n'.join([self.pages[i][index:]] + self.pages[i + 1:])
            except IndexError:
                doan_cuoi_vb = self.pages[-1][index:]
            self.pages = self.pages[:i] + [self.pages[i][:index]]
            break
        doan_cuoi_vb = doan_cuoi_vb.replace('(đã ký)', '').replace('(Đã ký)', '')
        pattern = r'[-–]\s*[\w\,\.\-\:\(\) \n]+\;'
        noi_nhan_tmp = re.findall(pattern, doan_cuoi_vb)
        if len(noi_nhan_tmp) > 0 and noi_nhan_tmp[-1].find('Lưu') > -1:
            noi_nhan_tmp = noi_nhan_tmp[:-1]
        self.noi_nhan = []
        for item in noi_nhan_tmp:
            # doan_cuoi_vb = doan_cuoi_vb.replace(item, '')
            self.noi_nhan.append(
                re.sub(r'\ {2,}', ' ', re.sub(r'\n+', ' ', re.sub(r'[-–]\s*', '', item))).replace(';', ''))
        pattern_Luu = r'Lưu\: *[\w\,\&\.\-\–\:\;\(\) ]+(?:\n| {2,})'
        temp = re.findall(pattern_Luu, doan_cuoi_vb)[0].strip()
        self.noi_nhan.append(re.split(r'\s{2,}', temp, 1)[0])
        return self.noi_nhan

    def remove_chu_ki(self):
        # # old code
        # if self.loai_van_ban == "LUẬT":
        #     pattern = r'Luật +này +đã +được'
        #     index = re.search(pattern, self.text).start()
        #     temp = self.text[index:]
        #     self.text = self.text[:index]
        #     index = temp.find('CHỦ TỊCH QUỐC HỘI')
        #     self.thoi_gian_ban_hanh = re.sub(r'\s{2}', ' ', temp[:index].strip())
        #     return self.thoi_gian_ban_hanh
        # else:
        #     index = self.text.rfind('KT. BỘ TRƯỞNG')
        #     self.text = self.text[:index - 1]
        #     return ''

        # new code
        if self.loai_van_ban == "LUẬT":
            pattern = r'Luật +này +đã +được'
            for i in range(len(self.pages) - 1, -1, -1):
                temp = re.search(pattern, self.pages[i])
                if temp is None:
                    continue
                index = temp.start()
                self.pages = self.pages[:i] + [self.pages[i][:index]]
                temp = self.pages[i][index:]
                index = temp.find('CHỦ TỊCH QUỐC HỘI')
                self.thoi_gian_ban_hanh = re.sub(r'\s{2}', ' ', temp[:index].strip())
                return self.thoi_gian_ban_hanh
        else:
            for i in range(len(self.pages) - 1, -1, -1):
                index = self.pages[i].rfind('KT. BỘ TRƯỞNG')
                if index == -1:
                    continue
                self.pages = self.pages[:i] + [self.pages[i][:index]]
                return ''

    def detect_noi_dung(self):
        # open('output/text', 'w', encoding='utf-8').write(self.text)
        self.text = '\n'.join(self.pages)
        print('------------------------')
        print('Start extracting data')
        # self.data = Item(self.text)
        self.data = Item(self.pages, 0)

        # noidung.print()
        return self.data

    def remove_line(self):
        self.pages = [re.sub('\-{5,}', '\n', page) for page in self.pages]

    def detect_footer(self):
        pass


all_pattern = [
    (r'Chương *[IVX]+', "Chương"),  # Chương
    (r'Mục *\d+', "Mục"),  # Mục
    (r'\n *Điều *\d+[\.\:]', "Điều"),  # Điều
    (r'\n *\d{1,2}\. ', "Khoản"),  # Khoản
    (r'\n *[a-z]\) ', "Điểm"),  # Điểm
    (r'\n *[a-z]\.\d+\) ', "Hạ Điểm"),  # Hạ điểm
    # (r'[\.\;\:\?]{1} *\n+ *[-–]{1} *', "Hạ điểm"),
]

'''
class Item:
    def __init__(self, content, item_type=0, stt='', type='Text'):
        self.stt = stt.strip()
        self.item_type = item_type
        self.type = type
        self.content = content.strip()
        self.title = ""
        self.children = []

        if item_type < len(all_pattern) and len(self.content) > 1:
            print('analysis', self.stt)
            self.pattern = all_pattern[item_type][0]
            # self.type = all_pattern[item_type][1]
            self.analysis_content()
            self.has_data = True
        else:
            self.has_data = False
        self.tokens = process_text(self.content)

    def analysis_content(self):
        pattern_title = r'[^\n]+'
        if self.stt != '' and self.item_type < 4:
            self.title = re.search(pattern_title, self.content).group().strip()
            self.content = re.sub(pattern_title, '', self.content, count=1)
        for i in range(self.item_type, len(all_pattern)):
            stt_children = re.findall(all_pattern[i][0], self.content)
            if len(stt_children) > 0:
                print('found', stt_children)
                children_type = all_pattern[i][1]
                children = re.split(all_pattern[i][0], self.content)
                self.content = children[0]
                children = children[1:]
                for stt, text in zip(stt_children, children):
                    # if text.strip()!='' or stt.strip()!='':
                    self.children.append(Item(text, i + 1, stt, children_type))
                break

    def print(self, pad_current='', pad=' ', print_content=True, display=True):
        text = '{0}{1}: {2}'.format(pad_current, self.stt.strip().rstrip(':.,)'), self.title.strip())
        if display:
            print(text)
        if print_content:
            content = '{0}{1}{2}'.format(pad_current, pad, self.content.strip())
            if display:
                print(content)
            text += '\n' + content
        for children in self.children:
            child_content = children.print(pad_current + pad, pad, print_content)
            text += '\n' + child_content
        return text

    def get_content(self, tokenized=False):
        if tokenized:
            content = self.tokens.strip()
        else:
            content = self.content.strip()
        for children in self.children:
            child_content = children.get_content(tokenized)
            content += ' ' + child_content
        return content

    def to_json(self):
        return {
            'stt': self.stt.strip(),
            'title': self.title.strip(),
            'type': self.type.strip(),
            'content': self.content.strip(),
            'children': [children.to_json() for children in self.children]
        }

    def to_database(self, database=None, parent=None, table='content', parent_ref='', title_ref=''):
        if database == None:
            database = DataBase()
        reference = '{0}/{1}'.format(parent_ref.strip().rstrip(':.,)/\\'), self.stt.strip().rstrip(':.,)'))
        if len(self.title.strip()) > 0:
            if len(title_ref.strip()) > 0:
                title = '{0} | {1}'.format(title_ref.strip(), self.title.strip())
            else:
                title = self.title.strip()
        else:
            title = title_ref
        record = {
            'parent': parent,
            'stt': self.stt.strip(),
            'type': self.type,
            'title': title,
            'content': self.content.strip(),
            'reference': reference,
            'tokens': self.tokens
        }
        parent = database.insert(record, table=table)
        for children in self.children:
            children.to_database(database, parent, table=table, parent_ref=reference, title_ref=title)
        return database
'''


class Item:
    def __init__(self, pages, page_index, item_type=0, header='', type='Text'):
        self.content = '\n'.join(pages)
        self.header = header.strip()
        self.item_type = item_type
        self.type = type
        self.pages = pages
        self.title = ""
        self.children = []
        self.page_index = page_index

        if item_type < len(all_pattern) and len(self.pages) > 0:
            print('analysis', self.header)
            self.pattern = all_pattern[item_type][0]
            # self.type = all_pattern[item_type][1]
            self.analysis_content()
            self.has_data = True
        else:
            self.has_data = False
        self.tokens = process_text(self.content)

    def analysis_content(self):
        pattern_title = r'[^\n]+'
        if self.header != '' and self.item_type < 4:
            self.title = re.search(pattern_title, self.pages[0]).group().strip()
            self.pages[0] = re.sub(pattern_title, '', self.pages[0], count=1)
        for i in range(self.item_type, len(all_pattern)):
            children_header = []
            for idx, page in enumerate(self.pages):
                children_match = re.findall(all_pattern[i][0], '\n' + page)
                if len(children_match) > 0:
                    print('found', children_match)
                    for child in children_match:
                        children_header.append((child, self.page_index + idx, idx))
            if not children_header:
                continue
            children_type = all_pattern[i][1]
            content = '\n'.join(self.pages)
            children_data = re.split(all_pattern[i][0], content)
            self.content = children_data[0]
            children_data = children_data[1:]
            for j in range(len(children_header)):
                if j < len(children_header) - 1:
                    first_page_idx = children_header[j][2]
                    last_page_idx = children_header[j + 1][2]
                    if first_page_idx == last_page_idx:
                        pages = [children_data[j]]
                    else:
                        first_page = '\n' + self.pages[first_page_idx]
                        first_page_data = first_page[first_page.find(children_header[j][0]) +
                                                     len(children_header[j][0]):]
                        last_page = '\n' + self.pages[last_page_idx]
                        last_page_data = last_page[:last_page.find(children_header[j + 1][0])]
                        pages = [first_page_data] + self.pages[first_page_idx + 1:last_page_idx] + [last_page_data]
                        if last_page_data == "":
                            pages = pages[:-1]
                else:
                    first_page_idx = children_header[j][2]
                    if first_page_idx == len(self.pages) - 1:
                        pages = [children_data[-1]]
                    else:
                        first_page = '\n' + self.pages[first_page_idx]
                        first_page_data = first_page[first_page.find(children_header[j][0]) +
                                                     len(children_header[j][0]):]
                        pages = [first_page_data] + self.pages[first_page_idx + 1:]
                page_index = children_header[j][1]
                child_header = children_header[j][0]
                self.children.append(Item(pages, page_index, i + 1, child_header, children_type))
            break

    def print(self, pad_current='', pad=' ', print_content=True, display=True):
        text = 'p{0} - {1}{2}: {3}'.format(self.page_index + 1, pad_current,
                                           self.header.strip().rstrip(':.,)'), self.title.strip())
        if display:
            print(text)
        if print_content:
            content = '{0}{1}{2}'.format(pad_current, pad, self.content.strip())
            if display:
                print(content)
            text += '\n' + content
        for children in self.children:
            child_content = children.print(pad_current + pad, pad, print_content)
            text += '\n' + child_content
        return text

    def get_content(self, tokenized=False):
        if tokenized:
            content = self.tokens.strip()
        else:
            content = self.content.strip()
        for children in self.children:
            child_content = children.get_content(tokenized)
            content += ' ' + child_content
        return content

    def to_json(self):
        return {
            'stt': self.header.strip(),
            'title': self.title.strip(),
            'type': self.type.strip(),
            'page': self.page_index,
            'content': self.content.strip(),
            'children': [children.to_json() for children in self.children]
        }

    def to_database(self, database=None, parent=None, table='content', parent_ref='', title_ref=''):
        if database == None:
            database = DataBase()
        reference = '{0}/{1}'.format(parent_ref.strip().rstrip(':.,)/\\'), self.header.strip().rstrip(':.,)'))
        if len(self.title.strip()) > 0:
            if len(title_ref.strip()) > 0:
                title = '{0} | {1}'.format(title_ref.strip(), self.title.strip())
            else:
                title = self.title.strip()
        else:
            title = title_ref
        record = {
            'parent': parent,
            'stt': self.header.strip(),
            'type': self.type,
            'title': title,
            'page': self.page_index,
            'content': self.content.strip(),
            'reference': reference,
            'tokens': self.tokens
        }
        parent = database.insert(record, table=table)
        for children in self.children:
            children.to_database(database, parent, table=table, parent_ref=reference, title_ref=title)
        return database
