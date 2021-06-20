import wikipedia


def extract_companies_software(items):
    companies = set()
    software = set()
    for data in items:
        try:
            page = wikipedia.page(data)
            categories = page.categories
            for category in categories:
                category_lower = category.lower()
                if 'software' in category_lower or 'program' in category_lower:
                    software.add(data)
                elif 'company' in category_lower or 'companies' in category_lower:
                    companies.add(data)
        except wikipedia.DisambiguationError:
            pass
        except wikipedia.PageError:
            pass
        except KeyError: # sometimes page.contents throws
            pass
    return companies, software
