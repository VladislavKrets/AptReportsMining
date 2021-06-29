import PyPDF4
import pytesseract
from PIL import Image, ImageOps
from googletrans import Translator
import os
from pdfminer import high_level
import shutil


def get_images_from_page(path, page):
    imgs = []
    if '/XObject' in page['/Resources']:
        xObject = page['/Resources']['/XObject'].getObject()

        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "P"
                if '/Filter' in xObject[obj]:
                    if xObject[obj]['/Filter'] == '/FlateDecode':
                        img = Image.frombytes(mode, size, data)
                        img.save(path + '/' + obj[1:] + ".png")
                    elif xObject[obj]['/Filter'] == '/DCTDecode':
                        img = open(path + '/' + obj[1:] + ".jpg", "wb")
                        img.write(data)
                        img.close()
                    elif xObject[obj]['/Filter'] == '/JPXDecode':
                        img = open(path + '/' + obj[1:] + ".jp2", "wb")
                        img.write(data)
                        img.close()
                    elif xObject[obj]['/Filter'] == '/CCITTFaxDecode':
                        img = open(path + '/' + obj[1:] + ".tiff", "wb")
                        img.write(data)
                        img.close()
                else:
                    img = Image.frombytes(mode, size, data)
                    img.save(path + '/' + obj[1:] + ".png")


def parse_pdf(pdf_file_name):
    pdf_file = open(pdf_file_name, 'rb')
    read_pdf = PyPDF4.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    temp_directory_name = '.'.join(pdf_file_name.split('.')[:-1])
    if not os.path.exists(temp_directory_name):
        os.mkdir(temp_directory_name)
    for i in range(0, number_of_pages):
        page = read_pdf.getPage(i)
        get_images_from_page(temp_directory_name, page)
    text = high_level.extract_text(pdf_file_name, "", [i for i in range(number_of_pages)])
    text = text.strip()
    translator = Translator()
    lang = translator.detect(text)
    if lang.lang != 'en':
        text = translator.translate(text).text
    return temp_directory_name, text


def extract_languages_from_images(temp_directory_name, remove=False):
    full_path = os.path.abspath(temp_directory_name)
    all_imgs = os.listdir(temp_directory_name)
    images_text = []
    for img in all_imgs:
        file = Image.open(os.path.join(full_path, img), 'r').convert('RGB')
        pixels = file.getdata()
        black_thresh = 50
        nblack = 0
        for pixel in pixels:
            if sum(pixel) < black_thresh:
                nblack += 1
        n = len(pixels)
        if nblack / float(n) > 0.5:
            file = ImageOps.invert(file)
        text = pytesseract.image_to_string(file).strip()
        if text and len(text) > 35:
            images_text.append(text)
    if remove:
        shutil.rmtree(temp_directory_name)
    return images_text
