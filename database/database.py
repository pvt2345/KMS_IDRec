import json
import os
import re
from search_engine import SearchEngine
class TextMiningDB:
    path = os.path.dirname(__file__)
    path = os.path.join(path,'data','db.json')
    def __init__(self):
        if os.path.exists(self.path):

            self.__dict__ = json.load(open(self.path,encoding='utf-8'))
        else:
            self.data = {}
            self.header = {}

    def create_table(self,table,columns=None):
        if table not in self.data:
            self.data[table]=[]
            self.header[table]=columns

    def insert(self,record,table='content'):
        if table not in self.data:
            self.data[table]=[]
            self.header[table]=None
        id = len(self.data[table])
        record = record.copy()
        record['id']=id
        self.data[table].append(record)
        return id

    def select(self,table):
        if table in self.data:
            return self.data[table].copy()
        else:
            return []

    def search(self,key_search):
        data = self.select('content')
        searcher = SearchEngine(key_search)
        result = []

        for d in data:
            content = d.get('content', ' ')
            if len(content.strip()) < 4:
                continue
            if len(re.findall('|'.join(key_search.lower().split()), content.lower())) == 0:
                continue

            titles = d.get('tieu_de', ' ').split('|')
            score = 0
            try:
                ok = True
                for i, title in enumerate(titles):
                    score_tieu_de, _ = searcher.LCS4Sentence(u'' + title)
                    score += (i + 1) / len(titles) * score_tieu_de * 2

                sentences = content.split('.')
                score_content = 0
                n_content = 0
                for sentence in sentences:
                    s_content, index = searcher.LCS4Sentence(u'' + sentence)
                    # score_content += s_content
                    # if s_content > 0:
                    #     n_content += 1
                    if s_content>score_content:
                        score_content=s_content
                score_content = 2 * score_content / (n_content + 1)
                _, index = searcher.LCS4Sentence(u'' + content)
                score += score_content
                if score < 0.3:
                    continue
                index = ';'.join(['{0}-{1}'.format(s, e) for s, e in index])
                reference = d.get('reference')  # d['stt']

                result.append({
                    'reference': reference,
                    'title': title.split('|')[-1],
                    'content': content,
                    'score': score,
                    'index': index
                })
            except Exception as e:
                print(e)
                ok = False
                # from text_mining.search_engine.search_engine import SearchEngine
                searcher = SearchEngine(key_search)

            if not ok:
                print('error')
                # print(searcher.LCS4Sentence('haha'))
        result = [r for r in result if r['score'] > 0.05]
        result = sorted(result, key=lambda r: r['score'], reverse=True)
        result = result[:20]
        return result

    def save(self):
        # if path!=None:
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        json.dump(self.__dict__,open(self.path,'w',encoding='utf-8'),ensure_ascii=False)