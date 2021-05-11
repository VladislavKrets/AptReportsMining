import PyPDF4
import geograpy
import nltk
from nltk import pos_tag, ne_chunk
import re
import wikipedia
import pytesseract
from guesslang import Guess
from PIL import Image, ImageOps
import os
import json

# if not downloaded
#nltk.download()


def extract_entities(text):
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'node'):
                print(chunk.node, ' '.join(c[0] for c in chunk.leaves()))


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


def extract_hashes(source_file_contents):
    regex_list = {

        'wordpress_md5': '\$P\$[\w\d./]+',
        'phpBB3_md5': '\$H\$[\w\d./]+',
        'sha1': '(?<!\w)[a-f\d]{40}(?!\w)',
        'md5': '(?<!\w)[a-f\d]{32}(?!\w)',
        'sha256': '(?<!\w)[a-f\d]{64}(?!\w)',
        'sha512': '(?<!\w)[a-f\d]{128}(?!\w)',
        'mysql': '(?<!\w)[a-f\d]{16}(?!\w)',
        'mysql5': '\*[A-F\d]{40}'

    }

    result = {}

    for format in regex_list.keys():
        hashes = []
        regex = re.compile(regex_list[format])
        hashes = regex.findall(source_file_contents)
        if hashes:
            result[format] = hashes

    return result


def extract_languages_from_images(temp_directory_name):
    full_path = os.path.abspath(temp_directory_name)
    all_imgs = os.listdir(temp_directory_name)
    images_text = []
    languages = []
    guess = Guess()
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
        text = pytesseract.image_to_string(file)
        images_text.append(text)
        language = guess.language_name(text)
        languages.append(language)
    return images_text, set(filter(lambda x: x and x.lower() in ('c', 'c++', 'java'), languages))


def parse_pdf(pdf_file_name):
    pdf_file = open(pdf_file_name, 'rb')
    read_pdf = PyPDF4.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    temp_directory_name = '.'.join(pdf_file_name.split('.')[:-1])
    raw = ''
    if not os.path.exists(temp_directory_name):
        os.mkdir(temp_directory_name)
    for i in range(0, number_of_pages):
        page = read_pdf.getPage(i)
        raw += (page.extractText() + " ")
        get_images_from_page(temp_directory_name, page)
    return temp_directory_name, raw


def extract_all_names(raw):
    toks = nltk.word_tokenize(raw)
    pos = pos_tag(toks)
    chunked_nes = ne_chunk(pos)
    return set([' '.join(map(lambda x: x[0], ne.leaves())) for ne in chunked_nes if isinstance(ne, nltk.tree.Tree)])


def extract_domain_names(raw):
    return re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', raw)


def extract_ip_addresses(raw):
    return re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', raw)


def extract_exploitation_techiques(raw):
    exploitation_techniques = open('files/techniques', 'r')
    exploitation_techniques = exploitation_techniques.readline()
    exploitation_techniques = json.loads(exploitation_techniques)

    techniques = set()
    raw_lower = raw.lower()
    for technique in exploitation_techniques:
        if technique.lower() in raw_lower:
            techniques.add(technique)
    return exploitation_techniques, techniques


def extract_providers(raw):
    raw_lower = raw.lower()
    text_providers = set()
    providers = open('files/providers', 'r')
    providers = providers.readline()
    providers = json.loads(providers)
    for provider in providers:
        if provider.lower() in raw_lower:
            text_providers.add(provider)
    return providers, text_providers


def extract_companies_protocols_software(nes, providers, exploitation_techniques):
    excluded = set(map(lambda x: x.lower(), nes)) \
               - set(map(lambda x: x.lower(), providers)) \
               - set(map(lambda x: x.lower(), exploitation_techniques))
    companies = set()
    protocols = set()
    software = set()
    for data in excluded:
        try:
            page = wikipedia.page(data)
            categories = page.categories
            for category in categories:
                category_lower = category.lower()
                if 'software' in category_lower or 'program' in category_lower:
                    software.add(data)
                elif 'protocol' in category_lower:
                    protocols.add(data)
                elif 'company' in category_lower or 'companies' in category_lower:
                    companies.add(data)
        except wikipedia.DisambiguationError:
            pass
        except wikipedia.PageError:
            pass
        except KeyError: # sometimes page.contents throws
            pass
    return companies, protocols, software


pdf_file_name = input('Enter file name:') #change to input
directory_name, text_data = parse_pdf(pdf_file_name)
images_text, languages = extract_languages_from_images(directory_name)

print('Program languages found:')
print(', '.join(languages)) #programm languages from images
print()

places = geograpy.get_place_context(text=text_data).countries #get places
print('Countries found:')
print(', '.join(places))
print()

nes = extract_all_names(text_data)

domain_names = extract_domain_names(text_data)
print('Domain names found:')
print(', '.join(set(domain_names))) #domain names
print()

ip_addresses = extract_ip_addresses(text_data)
print('IP addresses found:')
print(', '.join(set(ip_addresses))) #ip addresses
print()

hashes = extract_hashes(text_data)
print('Hashes found:')
for key, value in hashes.items():
    print(key, 'hash')
    print(', '.join(set(value)))
print()

exploitation_techniques, techniques = extract_exploitation_techiques(text_data)
print('Exploitation techniques found:')
print(', '.join(techniques)) #exploitation techniques
print()

providers, extracted_providers = extract_providers(text_data)
print('Providers found:')
print(', '.join(extracted_providers)) #providers
print()

companies, protocols, software = extract_companies_protocols_software(nes, providers, exploitation_techniques)
print('Companies found:')
print(', '.join(companies)) #companies
print(', '.join(protocols)) #protocols
print(', '.join(software)) #software
