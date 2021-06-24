import json
import re

registry_keys = [
        'HKEY_CURRENT_USER'.lower(),
        'HKCU'.lower(),
        'HKEY_USERS'.lower(),
        'HKU'.lower(),
        'HKEY_LOCAL_MACHINE'.lower(),
        'HKLM'.lower(),
        'HKEY_CLASSES_ROOT'.lower(),
        'HKCR'.lower(),
        'HKEY_CURRENT_CONFIG'.lower(),
        'HKEY_DYN_DATA'.lower()
]


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
    return re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', raw)


def extract_ip_addresses(raw):
    return re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', raw)


def extract_file_names(raw):
    files = re.findall(r'([\\/].*?\.[\w:]+)', raw, re.I)
    files = set(filter(lambda x: '://' not in x and not x.startswith('//'), files))
    extensions = set(map(lambda x: x.split('.')[-1], files))
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


def registry_keys_extract(special_words):
    registry_data = set()
    for word in special_words:
        if word.split('\\')[0] in registry_keys:
            registry_data.add(word)
    return registry_data


def clear_registry_keys(special_words):
    return [i for i in special_words if i.split('\\')[0] not in registry_keys]
