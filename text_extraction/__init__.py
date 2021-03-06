from text_extraction.pdf_extract import parse_pdf, extract_languages_from_images
from text_extraction.country_info import CountryInfoExtract
from text_extraction.names_extract import extract_all_names, extract_special_words, clear_special_words
from text_extraction.regex_info_extract import extract_hashes, extract_providers,\
    extract_ip_addresses, extract_domain_names, extract_file_names,\
    extract_protocols, registry_keys_extract, clear_registry_keys, clear_hashes
from text_extraction.techniques_extract import search_techniques
from text_extraction.predict_program_language import get_languages, train
from text_extraction.wiki_extract import extract_companies_software

