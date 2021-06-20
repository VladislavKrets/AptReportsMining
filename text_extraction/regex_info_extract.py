import json
import re


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


def extract_domain_names(raw):
    return re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', raw)


def extract_ip_addresses(raw):
    return re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', raw)


def extract_file_names(raw):
    file_extensions = open('files/file_extensions.txt', 'r')
    extensions = map(lambda x: re.escape(x).strip(), file_extensions.readlines())
    full_extensions = '|'.join(extensions)
    files = re.findall(f'\S+(?:{full_extensions})', raw, re.I)
    files = set(filter(lambda x: '://' not in x, files))
    extensions = set()
    for file in files:
        extensions.add('.'.join(file.split('.')[1:]).lower())
    return files, extensions


def check_word(w):
    w = re.escape(w)
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def extract_providers(raw):
    text_providers = set()
    providers = open('files/providers', 'r')
    providers = providers.readline()
    providers = json.loads(providers)
    for provider in providers:
        if check_word(provider)(raw) is not None:
            text_providers.add(provider)
    return text_providers


def extract_protocols(raw):
    text_protocols = set()
    protocols = open('files/protocols.json', 'r')
    protocols = protocols.readline()
    protocols = json.loads(protocols)
    for protocol in protocols:
        if check_word(protocol)(raw) is not None:
            text_protocols.add(protocol)
    return text_protocols
