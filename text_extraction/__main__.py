from text_extraction import parse_pdf, extract_all_names,\
    CountryInfoExtract, search_techniques, extract_file_names, extract_providers,\
    extract_hashes, extract_domain_names, extract_ip_addresses,\
    extract_languages_from_images, get_languages, extract_companies_software,\
    extract_protocols, train

file_name = 'test.pdf'
temp_directory_name, text = parse_pdf(file_name)
names = extract_all_names(text)
extractor = CountryInfoExtract(names)
print('Countries')
countries = extractor.extract_countries()
print(countries)
print()
print('Cities')
cities = extractor.extract_cities()
print(cities)
print()
print('Country regions')
country_regions = extractor.extract_country_regions()
print(country_regions)
print()
print('Global regions')
global_regions = extractor.deeply_extract_global_region()
print(global_regions)
print()
print('MITRE ATT&CK techniques')
print(search_techniques(text))
files, extensions = extract_file_names(text)
print()
print('File names')
print(files)
print()
print('File extensions')
print(extensions)
hashes = extract_hashes(text)
print()
print('Hashes')
print(hashes)
domain_names = extract_domain_names(text)
print()
print('Domain names')
print(domain_names)
ip_addresses = extract_ip_addresses(text)
print()
print('Ip addresses')
print(ip_addresses)
providers = extract_providers(text)
print()
print('Providers')
print(providers)
protocols = extract_protocols(text)
print()
print('Protocols')
print(protocols)
images_text = extract_languages_from_images(temp_directory_name)
languages = get_languages(images_text)
print()
print('Program languages')
print(languages)
companies, software = extract_companies_software(names - cities - countries - country_regions)
print()
print('Companies')
print(companies)
print()
print('Software')
print(software)