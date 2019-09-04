from sqlalchemy.ext.declarative import declarative_base
import re
import time
from . import config
import pymysql
from search_engine.search_tfidf import searchtfidf
from search_engine import search_engine
Base = declarative_base()


pymysql.install_as_MySQLdb()

class DataAccess:
    def __init__(self):
        self.connect()

    def connect(self):
        self.connection = pymysql.connect(host=config.DATABASE_CONFIG['host'],
                                     db=config.DATABASE_CONFIG['dbname'],
                                     user=config.DATABASE_CONFIG['user'],
                                     password=config.DATABASE_CONFIG['password'],
                                     port=config.DATABASE_CONFIG['port'],
                                     charset='utf8mb4',
                                     cursorclass = pymysql.cursors.DictCursor)

    def GetData(self, query ):
        if(self.connection._closed):
            self.connect()
        cursor = self.connection.cursor()
        try:
            # connection.open()
            cursor.execute(query)
            data = cursor.fetchall()
            return data
        # except:
        #     return -1
        finally:
            self.connection.close()


    def ExecuteCommand(self, query : str):
        if(self.connection._closed):
            self.connect()
        cursor = self.connection.cursor()
        try:
            # connection.open()
            cursor.execute(query)
            self.connection.commit()
        finally:
            self.connection.close()

    def insert(self, item, table='content'):
        index_table = {
            'content':'document_dtl',
            'info':'document'
        }
        table = index_table[table]
        if (table == 'document'):
            try:
                loai_van_ban = item['Loại văn bản']
                noi_ban_hanh = item['Nơi ban hành']
                so_van_ban = item['Số văn bản']
                dia_diem = item['Địa điểm']
                thoi_gian = item['Thời gian']
                can_cu = ' '.join(item['Căn cứ'])
                trich_yeu_noi_dung = item['Trích yếu nội dung']
                noi_nhan = ' '.join(item['Nơi nhận'])
                phu_luc = item['Phụ lục']
                yeu_cau = item['Yêu cầu']
                path = item.get('path')
                title = item.get('title')
                subtitle = item.get('subtitle')
                content = item.get('content')
                _data = self.GetData("SELECT so_van_ban FROM document WHERE so_van_ban = '{}'".format(so_van_ban.strip()))

                if (len(_data) == 0):
                    self.ExecuteCommand(
                        'INSERT INTO {} (can_cu, loai_van_ban, noi_ban_hanh, noi_nhan, so_van_ban, phu_luc, thoi_gian, trich_yeu, yeu_cau, dia_diem, path, title, subtitle, content) '.format(
                            table) +
                        "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}')".format(can_cu,
                                                                                                               loai_van_ban,
                                                                                                               noi_ban_hanh,
                                                                                                               noi_nhan,
                                                                                                               so_van_ban,
                                                                                                               phu_luc,
                                                                                                               thoi_gian,
                                                                                                               trich_yeu_noi_dung,
                                                                                                               yeu_cau,
                                                                                                               dia_diem,
                                                                                                               path,
                                                                                                               title,
                                                                                                               subtitle,
                                                                                                               content))
                    pattern = r"\*[\w+/–-]*#"
                    s = []
                    for _item in item['Căn cứ']:
                        s.append(re.findall(pattern, _item))

                    _s = []
                    for _item in s:
                        for __item in _item:
                            _s.append(__item)
                    _s = [_item[1:-1] for _item in _s]
                    # _s = ', '.join(_item for _item in _s)
                    # print(_s)
                    _s = list(set(_s))
                    for _item in _s:
                        self.ExecuteCommand("INSERT INTO lien_ket_vb VALUES('{0}', '{1}', 1)".format(so_van_ban, _item))

                    data = self.GetData('SELECT MAX(id) FROM document')
                    return data[0]['MAX(id)']

                else:
                    return -1
            except Exception as e:
                print(e)
                return -1

        elif (table == 'document_dtl'):
            try:
                type = item['type']
                stt = item['stt']
                title = item['title']
                content = item['content']
                parent = item['parent']
                reference = item.get('reference')
                # page = item['page']
                page = item.get('page')
                tokens = item.get('tokens')
                if (isinstance(parent, int)):
                    self.ExecuteCommand('INSERT INTO {} (parent, type, stt, tieu_de, content,reference, tokens, page) VALUES '.format(table) +
                                        "({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(parent, type, stt, title, content,reference,tokens, page))
                else:
                    self.ExecuteCommand('INSERT INTO {} (parent, type, stt, tieu_de, content,reference, tokens, page) VALUES '.format(table) +
                                        "('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(parent, type, stt, title,
                                                                                     content,reference, tokens, page))
                data = self.GetData('SELECT MAX(id) as id from `document_dtl`')
                return data[0]['id']
            except Exception as e:
                print(e)
                return -1


    def GetDataLienKet(self):
        return self.GetData('SELECT * FROM lien_ket')

    def GetTokens(self):
        documents = self.GetData('SELECT id,tieu_de,reference,tokens,content FROM document_dtl')
        return documents
    def get_documents(self):
        return self.GetData('SELECT so_van_ban,trich_yeu,content,title,subtitle FROM document')
    def search(self, keyword):
        if len(keyword)>30:
            print('search tfidf')
            result = searchtfidf.search(keyword,self.GetTokens())
            result = sorted(result, key=lambda r: r['score'], reverse=True)
            result = result[:20]
            return result
        data =  self.GetData("SELECT `id`, `parent`, `type`, `tieu_de`,`reference`, `content`, MATCH (tieu_de, content) AGAINST " +
                             "('{} '".format(keyword)  +
                             "IN NATURAL LANGUAGE MODE) AS `score`" +
                             "FROM `document_dtl` WHERE MATCH (tieu_de, content) AGAINST " +
                             "('{} '".format(keyword) +
                            "IN NATURAL LANGUAGE MODE) ")
        print(data)
        start = time.time()
        result = search_engine.multi_search(keyword,data,top=20)
        print('search done in', time.time() - start)
        return result

    def save(self):
        pass
