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
