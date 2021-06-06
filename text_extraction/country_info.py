from text_extraction import models


class CountryInfoExtract:
    def __init__(self, names):
        self.names = names

    def extract_cities(self):
        cities = models.Cities.select(models.Cities.name)\
            .where(models.Cities.name << self.names)
        return set(map(lambda x: x.name, cities))

    def extract_countries(self):
        countries = models.Country.select(models.Country.name)\
            .where(models.Country.name << self.names)
        return set(map(lambda x: x.name, countries))

    def extract_country_regions(self):
        country_regions = models.CountryRegion.select(models.CountryRegion.name)\
            .where(models.CountryRegion.name << self.names)
        return set(map(lambda x: x.name, country_regions))

    def extract_global_regions(self):
        global_regions = models.GlobalRegion.select(models.GlobalRegion.name)\
            .where(models.GlobalRegion.name << self.names)
        return set(map(lambda x: x.name, global_regions))

    def deeply_extract_global_region(self):
        global_regions = models.GlobalRegion.select(models.GlobalRegion.name) \
            .join(models.Country, on=(models.Country.global_region == models.GlobalRegion.id)) \
            .join(models.Cities, on=(models.Country.id == models.Cities.country))\
            .join(models.CountryRegion, on=(models.Country.id == models.CountryRegion.country))\
            .where((models.Country.name << self.names)
                   | (models.Cities.name << self.names)
                   | (models.CountryRegion.name << self.names)
                   | (models.GlobalRegion.name << self.names))\
            .distinct()
        return set(map(lambda x: x.name, global_regions))

