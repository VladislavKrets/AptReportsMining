import peewee

conn = peewee.SqliteDatabase('data.sqlite')
cursor = conn.cursor()


class BaseModel(peewee.Model):
    class Meta:
        database = conn


class GlobalRegion(BaseModel):
    name = peewee.TextField(column_name='name')


class Country(BaseModel):
    name = peewee.TextField()
    global_region = peewee.ForeignKeyField(model=GlobalRegion, backref='countries')


class CountryRegion(BaseModel):
    name = peewee.TextField()
    country = peewee.ForeignKeyField(model=Country, backref='country_regions')


class Cities(BaseModel):
    name = peewee.TextField()
    country = peewee.ForeignKeyField(model=Country, backref='cities')


class Technique(BaseModel):
    name = peewee.TextField()
    description = peewee.TextField()


conn.create_tables([GlobalRegion, Country, CountryRegion, Cities, Technique])

