# from pdf2image import convert_from_path
# import cv2
# import numpy as np
import shutil
import os
try:
    import comtypes.client
except:
    pass
# from wand.image import Image
def doc_to_pdf(doc_path,pdf_path):
    pdf_path = os.path._getfullpathname(pdf_path)
    doc_path = os.path._getfullpathname(doc_path)
    # print(pdf_path)
    # print(doc_path)
    wdFormatPDF = 17
    try:
        if doc_path.endswith('.pdf'):
            shutil.copy(doc_path,pdf_path)
            return pdf_path

        # shutil.copy(doc_path,tmp_path)
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = False
        # time.sleep(2)
        # print(word)
        doc = word.Documents.Open(doc_path)
        doc.SaveAs(pdf_path, FileFormat=wdFormatPDF)
        doc.Close()
        word.Quit()
        print('convert done.')
        return pdf_path
    except Exception as e:
        print("ERROR: ", e)
        return None

def process(path,dir_output):
    file_name = os.path.basename(path).rsplit('.',1)[0]
    file_ext = os.path.splitext(path)[-1].lower()
    pdf_path = os.path.join(dir_output, "{0}.pdf".format(file_name))
    if file_ext in ['.doc','.docx']:
        doc_to_pdf(path,pdf_path)
    else:
        shutil.copy(path,pdf_path)

    # text = pdf_reader.extract_text([pdf_path])
    dir_image = os.path.join(dir_output, file_name)
    # if not os.path.exists(dir_image):
    #     # os.removedirs(dir_image)
    #     os.makedirs(dir_image)
    #
    # try:
    #     with Image(filename=pdf_path, resolution=300) as img:
    #         # img.compression_quality =100
    #         # keep good quality
    #         for i,page_wand_image_seq in enumerate(img.sequence):
    #             print(i)
    #             page_wand_image = Image(page_wand_image_seq)
    #             # page_wand_image.make_blob(format='jpg')
    #             page_jpg_bytes = page_wand_image.make_blob(format="jpeg")
    #             open(os.path.join(dir_image, "{0}.jpg".format(i)),'wb').write(page_jpg_bytes)
    # except:
    #     images = convert_from_path(pdf_path)
    #     print(len(images))
    #     for i, image in enumerate(images):
    #         print(image)
    #         img = np.array(image)
    #         print(img.shape)
    #         cv2.imwrite(os.path.join(dir_image, "{0}.jpg".format(str(i))), img)
    return pdf_path,dir_image

def to_pdf(paths,dir_output='output'):
    if isinstance(paths,str):
        file_paths = [paths]
    else:
        file_paths = paths.copy()
    pdf_paths = []
    wdFormatPDF = 17
    word = None
    for path in file_paths:
        file_name = os.path.basename(path).rsplit('.',1)[0]
        file_ext = os.path.splitext(path)[-1].lower()
        pdf_path = os.path.join(dir_output, "{0}.pdf".format(file_name))
        if file_ext in ['.doc','.docx']:
            # doc_to_pdf(path,pdf_path)
            if word==None:
                word = comtypes.client.CreateObject('Word.Application')
                word.Visible = False
            pdf_path = os.path._getfullpathname(pdf_path)

            doc_path = os.path._getfullpathname(path)
            doc = word.Documents.Open(doc_path)
            doc.SaveAs(pdf_path, FileFormat=wdFormatPDF)
            doc.Close()
        elif file_ext in ['.pdf']:
            # pdf_path = os.path._getfullpathname(path)
            pdf_path = os.path.abspath(path)
            # shutil.copy(path,pdf_path)
        else:
            pdf_path = None
        if pdf_path!= None:
            pdf_paths.append(pdf_path)
    if word!=None:
        word.Quit()
    if isinstance(paths,str):
        return pdf_paths[0]
    return pdf_paths

