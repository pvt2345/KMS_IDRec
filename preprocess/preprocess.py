import re
from underthesea import word_tokenize
from underthesea.word_tokenize.regex_tokenize import tokenize
import string
import os

path = os.path.dirname(__file__)

vietnamese_stopwords = open(os.path.join(path, 'vietnamese-stopwords.txt'), encoding='utf8').read().split('\n')


def clean_doc(doc):
    punc_remove = set(string.punctuation)
    doc = re.sub(r'[\w\W]*\d\[\w\W]*', ' ', doc)
    stop_free = " ".join([i for i in doc.split() if i not in vietnamese_stopwords])
    punc_free = ''.join(ch for ch in stop_free if ch not in punc_remove)
    punc_free = punc_free.lower()
    return punc_free


def tokenizer(doc):
    return word_tokenize(doc, format='text')


def process_text(doc):
    doc = clean_doc(doc)
    docs = tokenize(doc)
    text = ' . '.join([word_tokenize(doc, format='text') for doc in docs])
    return text


if __name__ == '__main__':
    t = process_text("Điều 1. Phạm vi và đối tượng áp dụng "
                     "Thông tư này hướng dẫn một số nội dung về thuế giá trị gia tăng (GTGT) đối với dịch vụ viễn "
                     "thông của cơ sở kinh doanh dịch vụ viễn thông. "
                     " Điều 2. Dịch vụ viễn thông thuộc đối tượng không chịu thuế GTGT "
                     " Các dịch vụ viễn thông dưới đây thuộc đối tượng không chịu thuế GTGT: "
                     " 1. Dịch vụ viễn thông công ích theo quy định của Luật Viễn thông.  "
                     " Danh mục dịch vụ viễn thông công ích, chất lượng, giá cước, đối tượng và phạm vi cung cấp "
                     " dịch vụ viễn thông công ích thực hiện theo quy định của Bộ Thông tin và Truyền thông. "
                     " 2. Dịch vụ viễn thông từ nước ngoài vào Việt Nam (chiều đến).  "
                     " Điều 3. Giải thích từ ngữ "
                     " 1. Các từ ngữ dưới đây sử dụng trong Thông tư này được hiểu theo quy định của Luật Viễn  "
                     "thông, cụ thể: ")
    print(t)
