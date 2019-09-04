from text_mining import file_reader
import cv2
import re
import os
import numpy as np

# page_text = file_reader.extract_text('D:/Documents/CMC/1_Dữ liệu Thuế/vanban/vbpq/thongtu/158578_TT_78_2010_BTC.doc', 'output')
def remove_quoc_ngu(text):
    quoc_ngu = []
    quoc_ngu.append(r'C\w{1,2}NG *HO\w{1,2} *X\w{1,2} *H\w{1,2}I *CH\w{1,2} *NGH\w{1,2}A *VI\w{1,2}T *NAM')
    quoc_ngu.append(r'\w{2,4}c *l\w{1,2}p *- *T\w{1,2} *do *- *H\w{1,2}nh *ph\w{1,2}c')
    pattern = '|'.join(quoc_ngu)
    return re.sub(pattern,'',text)

def detect_date_time(text):
    date_time = r'[\w+ +]{2,10}, *ng\w{1,2}y *\d+ *th\w{1,2}ng *\d+ *n\w{1,2}m *\d+'
    return re.findall(date_time, text)

def find_quoc_ngu(text):
    quoc_ngu = []
    quoc_ngu.append(r'C\w{1,2}NG *HO\w{1,2} *X\w{1,2} *H\w{1,2}I *CH\w{1,2} *NGH\w{1,2}A *VI\w{1,2}T *NAM')

    # return re.findall(r'C\w{1,2}NG *HO\w{1,2} *X\w{1,2} *H\w{1,2}I *CH\w{1,2} *NGH\w{1,2}A *VI\w{1,2}T *NAM',text)
    return re.findall(r'\w{2,4}c *l\w{1,2}p *- *T\w{1,2} *do *- *H\w{1,2}nh *ph\w{1,2}c',text)
def split(text):
    return re.split('\-{5,}',text)
def remove_line(text):
    return re.sub('\-{5,}','\n',text)

def main_test_image():
    from text_mining.utils import image_reader

    page_end = image_reader.image_to_textbox('output/1.jpg', ocr=True)
    address, signature = image_reader.detect_footer(page_end)
    print('address')
    print(address['text'])
    print('signature')
    for x in signature:
        print(x['text'])

    page_first = image_reader.image_to_textbox('output/0.jpg', ocr=True)
    left, right = image_reader.detect_header(page_first)
    print('left')
    for x in left:
        print(x['text'])

    print('right')
    for x in right:
        print(x['text'])

def main():
    from text_mining.text_mining import TextMining
    # textmining = TextMining('data/test.pdf')
    textmining = TextMining('data/2.pdf')
    textmining.extraction()
    result =  textmining.to_json()
    # result['content'] = textmining.data.to_json()
    import json
    json.dump(result,open('output/result.json','w',encoding='utf-8'),ensure_ascii=False)
    # print('nội dung:')
    # textmining.data.to_database().to_excel('output/data.xlsx')

    # textmining.print()

import json
def process_file(path_file):
    '''

    :param path_file: đường dẫn file pdf hoặc word
    :return: output là json
    '''
    json.load(open(path_file))
if __name__ == '__main__':
    main()





