import pytesseract
from PIL import Image
import os
import cv2
import numpy as np


def extract_text(image_path,output_path=''):
    text = pytesseract.image_to_string(Image.open(image_path), lang="vi+eng")
    if output_path != '' and os.path.exists(output_path):
        writer = open(output_path,'w',encoding='utf-8')
        writer.write(text)
    return text


def image_to_textbox(imagepath,debug=False,tmp_path='output/debug',ocr=False):
    print('ocr pharse',imagepath)
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    img = cv2.imread(imagepath, 0)
    height,width = img.shape
    kernel = np.ones((10, 10), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=10)


    ret, thresh = cv2.threshold(erosion, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(img, contours, -1, (0,255,0), 3)
    # del contours[0]  # xóa khung viền
    boundingRect = []
    i = 0

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w>0.9*width and h>0.95*height:
            # bỏ qua khung viền
            continue
        if y>0.85*height and w<0.05*width:
            # bỏ qua số trang
            continue
        if (h > 0.01*height):
            boundingRect.append(np.zeros((4), np.uint8))
            boundingRect[i] = [x, y, w, h]
            i = i + 1

    # boundingRect = boundingRect[::-1]  # bounding rect chứa các phần text
    # del boundingRect[-1]  # xóa số trang
    textboxes = []
    for x,y,w,h in boundingRect:
        cv2.rectangle(erosion,(x,y),(x+w,y+h),(0,0,255),thickness=3)
        if ocr:
            text = pytesseract.image_to_string(img[y:y+h,x:x+w],lang='vie')
        else:
            text = ''
        textboxes.append({
            'text':text,
            'x0':x,
            'y0':y,
            'x1':x+w,
            'y1':y+h
        })
    if debug:
        cv2.imwrite('{0}/erosion.jpg'.format(tmp_path), erosion)
        cv2.imwrite('{0}/original.jpg'.format(tmp_path), img)
    print('done.')
    textboxes = sorted(textboxes,key=lambda k:(k['y0'],k['x0']))
    return {'textboxes':textboxes,'width':width,'height':height}

def detect_footer(page):
    textboxes = page['textboxes']
    left =  [box for box in textboxes if box['x0']<0.3*page['width']]
    left = sorted(left,key=lambda b:b['y0'])
    address = left[-1]
    signature = [box for box in textboxes if box['x1']>0.7*page['width'] and box['y1']>address['y0']]
    signature = sorted(signature,key=lambda box:box['y0'])
    return address,signature

def detect_header(page):
    textboxes = page['textboxes']
    top = [box for box in textboxes if box['y0'] < 0.25 * page['height']]
    left = [box for box in top if box['x0']<0.4*page['width']]
    right = [box for box in top if box['x1'] > 0.6 * page['width']]
    left = sorted(left,key=lambda b:b['y0'])
    right = sorted(right, key=lambda b: b['y0'])
    return left,right
