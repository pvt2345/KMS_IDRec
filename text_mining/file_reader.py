from .utils import file_convert,pdf_reader,image_reader
import os
#
# def inside(box1,box2):
#     if box1['x0']>box2['x1'] or box1['y0']>box2['y1'] or box1['x1']<box2['x0'] or box1['y1']<box2['y0']:
#         return False
#     else:
#         left = max(box1['x0'],box2['x0'])
#         right = min(box1['x1'],box2['x1'])
#         top = max(box1['y0'],box2['y0'])
#         down = min(box1['y1'],box2['y1'])
#         if (right-left)*(down-top)>0.6*(box1['x1']-box1['x0'])*(box1['y1']-box1['y0']):
#             return True
#         else:
#             return False
def extract_text(path,tmp_path='output'):
    pdf_path = file_convert.to_pdf(path,tmp_path)
    pdf = pdf_reader.PDFAnalyzer(pdf_path)
    pages = []
    for i,page in enumerate(pdf.pages):
        # print(len(page['textlines']))
        # if len(page['textlines'])==0:
        #     image_page = image_reader.image_to_textbox(os.path.join(dir_image,"{0}.jpg".format(i)),ocr=True)
        # else:
        #     image_page = image_reader.image_to_textbox(os.path.join(dir_image,"{0}.jpg".format(i)),ocr=False,debug=True)
        #     scale_x = image_page['width']/page['width']
        #     scale_y = image_page['height']/page['height']
        #     # textlines = []
        #     for textline in page['textlines']:
        #         textline['x0']*=scale_x
        #         textline['x1']*=scale_x
        #         textline['y0']*=scale_y
        #         textline['y1']*=scale_y
        #
        #     for box in image_page['textboxes']:
        #         textlines = [textline for textline in page['textlines'] if inside(textline,box)]
        #         textlines = sorted(textlines,key=lambda k:(k['y0'],k['x0']))
        #         box['text'] = ''.join([textline['text'] for textline in textlines])
                # print(box['text'])
        text = ' '.join([textline['text'] for textline in page['textlines']])
        pages.append(text)

    # for page in pages:
    #     print(page)
    return pages
