import pandas as pd
def is_separator(_ch):
    if _ch in list(" ,;\t.\n:+-*/"):
        return True
    return False
class SearchEngine:


    def __init__(self,pattern,option='1111'):

        self.m_ParternAutomat = []
        self.m_ContentWordsInP = []
        self.m_LCSResult = []
        self.m_FuzzyThreshold = {}
        self.m_NumberWordInP = 0
        self.m_NumberWordInS = 0
        self.m_Pattern = ''
        self.m_tsDoXapXiTu = 0
        self.m_tsAnpha = 0
        self.m_tsDoLechTichLuy = 0
        self.m_tsTanSuatTichLuy = 0
        self.m_DicMangDau = {}
        self.m_DicMangVietHoa = {}


        print('search',pattern)
        self.init_mangdau()
        self.init_mangviethoa()
        self.init_option(option)

        self.m_Pattern = pattern
        i = 0
        j = 0
        _code = 0
        _ch = 0
        _token = 0
        _value = ""
        _beginIndex = 0
        _endIndex = 0
        _InitlistIndex = {}
        self.m_ParternAutomat.append(_InitlistIndex)
        self.m_Pattern += " "
        # self.m_FuzzyThreshold = {}
        self.m_FuzzyThreshold[1] = 1
        self.m_FuzzyThreshold[2] =1
        self.m_FuzzyThreshold[3]=0.3
        self.m_FuzzyThreshold[4]=0.3
        self.m_FuzzyThreshold[5]=0.4
        self.m_FuzzyThreshold[6]=0.4
        self.m_FuzzyThreshold[7]=0.4
        self.m_FuzzyThreshold[8]=0.4
        self.m_FuzzyThreshold[9]=0.3
        self.m_FuzzyThreshold[10]=0.3
        self.m_FuzzyThreshold[11] = 0.3
        self.m_FuzzyThreshold[12] = 0.3
        for l in range(12,50):
            self.m_FuzzyThreshold[i]=0.3
        while i< len(self.m_Pattern):
            _ch = self.m_Pattern[i]
            _ch = self.normalize_char(_ch)
            if is_separator(_ch):
                _word = ContentWord()
                _word.value = _value
                _word.start = _beginIndex
                _word.end = _endIndex

                self.m_ContentWordsInP.append(_word)

                _value = ''
                _endIndex+=1
                _beginIndex = _endIndex
                _token = _token+1
                _listIndex = {}
                self.m_ParternAutomat.append(_listIndex)
                i+=1
            else:
                _value += _ch
                _endIndex +=1

                _code = ord(_ch)
                _listIndex = self.m_ParternAutomat[_token]
                if _code not in _listIndex:
                    _lst = []
                    _listIndex[_code]=_lst
                    for k in range(i+1-_beginIndex):
                        _listIndex[_code].append(i+1-_beginIndex)
                j=i+1
                _index = 0
                _code_next = 0
                while _code!= _code_next and j <len(self.m_Pattern):
                    _ch_next = self.m_Pattern[j]
                    _ch_next = self.normalize_char(_ch_next)

                    _code_next = ord(_ch_next)

                    if _code == _code_next or j== len(self.m_Pattern)-1 or is_separator(_ch_next):
                        _index = j-i
                        for k in range(_index):
                            _listIndex[_code].append(j+1-_beginIndex)
                    if is_separator(_ch_next):
                        break
                    j+=1

                i+=1


        self.m_NumberWordInP = len(self.m_ContentWordsInP)
        # print(self.m_NumberWordInP)
        self.m_ParternAutomat.remove(self.m_ParternAutomat[self.m_NumberWordInP])

        # print(self.m_ContentWordsInP)
        # print(self.m_ParternAutomat)

    m_viethoathuong = True
    m_unicode = True
    m_codau = True
    m_colap = True

    def init_option(self,_option):
        self.m_viethoathuong,self.m_unicode,self.m_codau,self.m_colap = [False if i=='0' else True for i in _option]


    def init_mangdau(self):
        m_MangChuCai = u"A-Á-À-Ã-Ả-Ạ-Ă-Ắ-Ằ-Ẵ-Ẳ-Ặ-Â-Ấ-Ầ-Ẫ-Ẩ-Ậ"
        for i in range(0,len(m_MangChuCai),2):
            self.m_DicMangDau[m_MangChuCai[i]] = 'A'

        m_MangChuCai = u"a-á-à-ã-ả-ạ-ă-ắ-ằ-ẵ-ẳ-ặ-â-ấ-ầ-ẫ-ẩ-ậ"
        for i in range(0, len(m_MangChuCai), 2):
            self.m_DicMangDau[m_MangChuCai[i]] = 'a'

        m_MangChuCai = u"D-Đ"
        for i in range(0, len(m_MangChuCai), 2):
            self.m_DicMangDau[m_MangChuCai[i]] = 'D'

        m_MangChuCai = u"d-đ"
        for i in range(0, len(m_MangChuCai), 2):
            self.m_DicMangDau[m_MangChuCai[i]] = 'd'

        m_MangChuCai = u"E-É-È-Ẽ-Ẻ-Ẹ-Ê-Ế-Ề-Ễ-Ể-Ệ"
        for i in range(0, len(m_MangChuCai), 2):
            self.m_DicMangDau[m_MangChuCai[i]] = 'E'

        m_MangChuCai = u"e-é-è-ẽ-ẻ-ẹ-ê-ế-ề-ễ-ể-ệ"
        for i in range(0, len(m_MangChuCai), 2):
            self.m_DicMangDau[m_MangChuCai[i]] = 'e'

        m_MangChuCai = u"I-Í-Ì-Ĩ-Ỉ-Ị"
        for i in range(0, len(m_MangChuCai), 2):
            self.m_DicMangDau[m_MangChuCai[i]] = 'I'

        m_MangChuCai = u"i-í-ì-ĩ-ỉ-ị"
        for i in range(0, len(m_MangChuCai), 2):
            self.m_DicMangDau[m_MangChuCai[i]] = 'i'

        m_MangChuCai = u"O-Ó-Ò-Õ-Ỏ-Ọ-Ô-Ố-Ồ-Ỗ-Ổ-Ộ-Ơ-Ớ-Ờ-Ỡ-Ở-Ợ"
        for i in range(0, len(m_MangChuCai), 2):
            self.m_DicMangDau[m_MangChuCai[i]] = 'O'

        m_MangChuCai = u"o-ó-ò-õ-ỏ-ọ-ô-ố-ồ-ỗ-ổ-ộ-ơ-ớ-ờ-ỡ-ở-ợ"
        for i in range(0, len(m_MangChuCai), 2):
            self.m_DicMangDau[m_MangChuCai[i]] = 'o'

        m_MangChuCai = u"U-Ú-Ù-Ũ-Ủ-Ụ-Ư-Ứ-Ừ-Ữ-Ử-Ự"
        for i in range(0, len(m_MangChuCai), 2):
            self.m_DicMangDau[m_MangChuCai[i]] = 'U'

        m_MangChuCai = u"u-ú-ù-ũ-ủ-ụ-ư-ứ-ừ-ữ-ử-ự"
        for i in range(0, len(m_MangChuCai), 2):
            self.m_DicMangDau[m_MangChuCai[i]] = 'u'

        m_MangChuCai = u"Y-Ý-Ỳ-Ỹ-Ỷ-Ỵ"
        for i in range(0, len(m_MangChuCai), 2):
            self.m_DicMangDau[m_MangChuCai[i]] = 'Y'

        m_MangChuCai = u"y-ý-ỳ-ỹ-ỷ-ỵ"
        for i in range(0, len(m_MangChuCai), 2):
            self.m_DicMangDau[m_MangChuCai[i]] = 'y'
    def init_mangviethoa(self):
        m_MangChuCai = u"A-Á-À-Ã-Ả-Ạ-Ă-Ắ-Ằ-Ẵ-Ẳ-Ặ-Â-Ấ-Ầ-Ẫ-Ẩ-Ậ-"
        m_MangChuCai2 = u"a-á-à-ã-ả-ạ-ă-ắ-ằ-ẵ-ẳ-ặ-â-ấ-ầ-ẫ-ẩ-ậ-"

        m_MangChuCai += u"D-Đ-"
        m_MangChuCai2 += u"d-đ-"

        m_MangChuCai += u"E-É-È-Ẽ-Ẻ-Ẹ-Ê-Ế-Ề-Ễ-Ể-Ệ-"
        m_MangChuCai2 += u"e-é-è-ẽ-ẻ-ẹ-ê-ế-ề-ễ-ể-ệ-"

        m_MangChuCai += "I-Í-Ì-Ĩ-Ỉ-Ị-"
        m_MangChuCai2 += "i-í-ì-ĩ-ỉ-ị-"

        m_MangChuCai += "O-Ó-Ò-Õ-Ỏ-Ọ-Ô-Ố-Ồ-Ỗ-Ổ-Ộ-Ơ-Ớ-Ờ-Ỡ-Ở-Ợ-"
        m_MangChuCai2 += "o-ó-ò-õ-ỏ-ọ-ô-ố-ồ-ỗ-ổ-ộ-ơ-ớ-ờ-ỡ-ở-ợ-"

        m_MangChuCai += "U-Ú-Ù-Ũ-Ủ-Ụ-Ư-Ứ-Ừ-Ữ-Ử-Ự-"
        m_MangChuCai2 += "u-ú-ù-ũ-ủ-ụ-ư-ứ-ừ-ữ-ử-ự-"

        m_MangChuCai += "Y-Ý-Ỳ-Ỹ-Ỷ-Ỵ-"
        m_MangChuCai2 += "y-ý-ỳ-ỹ-ỷ-ỵ-"
        for i in range(0,len(m_MangChuCai),2):
            self.m_DicMangVietHoa[m_MangChuCai[i]] = m_MangChuCai2[i]

    def normalize_char(self,_ch):
        if not self.m_viethoathuong:
            if _ch in self.m_DicMangVietHoa:
                _ch = self.m_DicMangVietHoa[_ch]
            else:
                if _ch.isupper():
                    _ch = _ch.lower()
        if not self.m_codau:
            if _ch in self.m_DicMangDau:
                _ch = self.m_DicMangDau[_ch]

        return _ch

    def LCS4Char(self,_ch):
        _ch = self.normalize_char(_ch)
        _code = ord(_ch)
        for _order in range(len(self.m_ContentWordsInP)):
            _content_word = self.m_ContentWordsInP[_order]
            _result = [] #[0]*(len(_content_word['value'])+1)
            if len(self.m_LCSResult)>_order and self.m_LCSResult[_order]!=None:
                _result = self.m_LCSResult[_order]
            else:
                self.m_LCSResult.append(_result)

            _lst = self.m_ParternAutomat[_order]
            if _code in _lst:
                _arr = _lst[_code]
                if len(_arr)== len(_content_word)+1:
                    _arr.append(len(_content_word)+1)

                if len(_result) == 0:
                    _result.extend(_arr)
                else:
                    S=0
                    T = _arr[S]
                    while T <= len(_content_word):
                        if _result[S] < T and T <_result[_result[S]]:
                            _result[T] = _result[_result[S]]
                            _result[_result[S]] = T

                            S=T
                            T = _arr[_result[T]]
                        else:
                            S= _result[S]
                            T = _arr[S]

    def LCS4Sentence(self,str_source,_doxapxitu=0.8,_alpha=0.5):
        _token = 1
        _beginIndex = 0
        _endIndex = 0
        _modifiedOrder = 0
        _word = ''
        _ch = 0
        _isStart = False

        self.m_tsDoXapXiTu = _doxapxitu
        self.m_tsAlpha = _alpha
        _tansuat=0
        _dolech = 0
        _lstDoLechTichLuy = []
        for i in range(len(self.m_ContentWordsInP)):
            self.m_ContentWordsInP[i].searchedwords = None
            _lstDoLechTichLuy.append(10000)

        self.m_LCSResult = []
        str_source+=' '
        for i in range(len(str_source)):
            _ch = str_source[i]
            # print(_ch)
            if not is_separator(_ch):
                _word +=_ch
                _endIndex+=1
                self.LCS4Char(_ch)
            else:
                # Cập nhật curWord trong S
                _curWord = ContentWord()
                _curWord.value=_word
                _curWord.start = _beginIndex
                _curWord.end = _endIndex

                _word = ''
                _endIndex+=1
                _beginIndex=_endIndex
                _token +=1

                # Tổng họp kết quả
                # print(_curWord)
                # print(self.m_NumberWordInP)
                for _order in range(self.m_NumberWordInP):
                    _wordInP = self.m_ContentWordsInP[_order]
                    # print(_wordInP)
                    k=0
                    _count = 0
                    if len(self.m_LCSResult)>0:
                        while k <len(_wordInP):
                            _lst = self.m_LCSResult[_order]
                            if len(_lst)>0:
                                k = _lst[k]
                                if k<len(_wordInP)+1:
                                    _count+=1
                            else:
                                break
                    if _wordInP.searchedwords == None:
                        _wordInP.searchedwords = []
                    _LCS = _count/max(len(_wordInP),len(_curWord),1)
                    # print(_wordInP.searchedwords)
                    if _LCS >= self.m_tsDoXapXiTu and _LCS >= self.m_FuzzyThreshold.get(len(_wordInP),0.2):
                        # Tính theo tần suất cô lập và độ đảo từ
                        if self.m_colap:
                            _tansuat +=1
                            _wordInP.searchedwords.append(_curWord)
                            # print(_wordInP.value)
                            if _isStart:
                                _lstDoLechTichLuy[_order] = min(_lstDoLechTichLuy[_order],abs(_order-_modifiedOrder))

                            if _order==0:
                                _isStart = True
                            _modifiedOrder +=1
                        else:
                            if not _wordInP.isrepeated:
                                _tansuat +=1
                                _wordInP.searchedwords.append(_curWord)

                                if _isStart:
                                    _lstDoLechTichLuy[_order]=min(_lstDoLechTichLuy[_order],abs(_order-_modifiedOrder))

                                if _order == 0:
                                    _isStart = True

                                _modifiedOrder +=1
                                _wordInP.isrepeated=True
                self.m_LCSResult = []
            self.m_NumberWordInS = _token-1


        ######################### Tổng hợp kết quả #####################################

        N = 0
        if self.m_colap:
            _N = max(self.m_NumberWordInS,self.m_NumberWordInP)
        else:
            _N = self.m_NumberWordInP

        # Tính độ tích lũy
        for k in range(len(_lstDoLechTichLuy)):
            if _lstDoLechTichLuy[k]!= 10000:
                _dolech += _lstDoLechTichLuy[k]
        _dolechtichluy = _dolech

        _tansuattichluy = _tansuat
        _doxapxitonghop = (_dolech*(-self.m_tsAlpha)/(_N+1)+_tansuat)/_N
        _maskstring = ""
        index = set()
        for i in range(len(self.m_ContentWordsInP)):
            for var in self.m_ContentWordsInP[i].searchedwords:
                index.add((var.start,var.end))
                _maskstring += str(var)+';'
            _maskstring += '|'
        return _doxapxitonghop,sorted(list(index),key=lambda x:x[0])

class ContentWord:
    value = ''
    start = 0
    end = 0
    searchedwords = None
    isrepeated = False
    def __str__(self):
        return str(self.start)+'-'+str(self.end)
    def __len__(self):
        return len(self.value)

def similar(P,S,alpha,option='1111'):
    _searchengine = SearchEngine(P,option)
    # print(_searchengine.m_ContentWordsInP[0].searchedwords)
    _doxapxitonghop, _maskstring = _searchengine.LCS4Sentence(S,0.9,alpha)
    return _doxapxitonghop,_maskstring
def search(keys,data,top=10):
    searcher = SearchEngine(keys,'1111')
    scores = [(t,searcher.LCS4Sentence(t,0.9,0.5)[0]) for t in data]
    return sorted(scores,key=lambda x:x[1],reverse=True)[:top]

def load_data(path):
    df = pd.read_csv(path)
    return list(df['text'])

def rank_result(params):
    key_search,data,top = params
    searcher = SearchEngine(key_search)
    result = []

    for d in data:
        content = d.get('content', ' ')
        if len(content.strip()) < 4:
            continue

        titles = d.get('tieu_de', ' ').split('|')
        score = 0
        try:
            ok = True
            for i, title in enumerate(titles[-1:]):
                score_tieu_de, _ = searcher.LCS4Sentence(u'' + title)
                score += (i + 1) / len(titles) * score_tieu_de

            sentences = content.split('. ')
            score_content = 0
            n_content = 0
            for sentence in sentences:
                s_content, index = searcher.LCS4Sentence(u'' + sentence)
                # score_content += s_content
                # if s_content > 0:
                #     n_content += 1
                if s_content > score_content:
                    score_content = s_content
            # score_content = 2 * score_content / (n_content + 1)
            _, index = searcher.LCS4Sentence(u'' + content)
            score += score_content
            if score < 0.3:
                continue
            index = ';'.join(['{0}-{1}'.format(s, e) for s, e in index])
            reference = d.get('reference')  # d['stt']

            result.append({
                'reference': reference,
                'title': titles[-1],
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
    # result = [r for r in result if r['score'] > 0.05]
    result = sorted(result, key=lambda r: r['score'], reverse=True)
    result = result[:top]
    return result

import multiprocessing as mp
def multi_search(key_search,data,top=20):
    cpu_c = mp.cpu_count()
    p = mp.Pool(cpu_c)
    size = len(data)//cpu_c+1
    key_searchs = [key_search]*cpu_c
    parts = [data[i*size:(i+1)*size] for i in range(cpu_c)]
    tops = [top]*cpu_c
    scores = p.map(rank_result,zip(key_searchs,parts,tops))
    result = []
    for score in scores:
        result.extend(score)
    result = sorted(result, key=lambda r: r['score'], reverse=True)
    result = result[:top]
    p.close()
    return result

if __name__=='__main__':
    searcher = SearchEngine(u'thuế suất', '1111')

    print(searcher.LCS4Sentence(u'thuế suất giao dịch'))

    # print(searcher.LCS4Sentence(u'anh Linh học lớp anh'))
    # print(searcher.LCS4Sentence(u'lớp anh Linh học lớp anh 10'))








