from peewee import *
import json
import sys

database = PostgresqlDatabase('flightsskewed', **{'user': 'ubuntu', 'password': 'ubuntu'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Airports(BaseModel):
    airportid = CharField(primary_key=True)
    city = CharField(null=True)
    name = CharField(null=True)
    total2011 = IntegerField(null=True)
    total2012 = IntegerField(null=True)

    class Meta:
        db_table = 'airports'

class Airlines(BaseModel):
    airlineid = CharField(primary_key=True)
    hub = ForeignKeyField(db_column='hub', null=True, rel_model=Airports, to_field='airportid')
    name = CharField(null=True)

    class Meta:
        db_table = 'airlines'

class Customers(BaseModel):
    birthdate = DateField(null=True)
    customerid = CharField(primary_key=True)
    frequentflieron = ForeignKeyField(db_column='frequentflieron', null=True, rel_model=Airlines, to_field='airlineid')
    name = CharField(null=True)

    class Meta:
        db_table = 'customers'

class Flights(BaseModel):
    airlineid = ForeignKeyField(db_column='airlineid', null=True, rel_model=Airlines, to_field='airlineid')
    dest = ForeignKeyField(db_column='dest', null=True, rel_model=Airports, to_field='airportid')
    flightid = CharField(primary_key=True)
    local_arrival_time = TimeField(null=True)
    local_departing_time = TimeField(null=True)
    source = ForeignKeyField(db_column='source', null=True, rel_model=Airports, related_name='airports_source_set', to_field='airportid')

    class Meta:
        db_table = 'flights'

class Flewon(BaseModel):
    customerid = ForeignKeyField(db_column='customerid', null=True, rel_model=Customers, to_field='customerid')
    flightdate = DateField(null=True)
    flightid = ForeignKeyField(db_column='flightid', null=True, rel_model=Flights, to_field='flightid')

    class Meta:
        db_table = 'flewon'

class Numberofflightstaken(BaseModel):
    customerid = CharField(null=True)
    customername = CharField(null=True)
    numflights = BigIntegerField(null=True)

    class Meta:
        db_table = 'numberofflightstaken'
        primary_key = False

with open(sys.argv[1]) as f:
	data=[]
	for line in f:
		data.append(json.loads(line))
f.close()

def insert_customer(entry,title):
	cid=entry['customerid']
	airline=entry['frequentflieron']
	if(title == 'newcustomer'):
		air=Airlines.select().where(Airlines.name == airline)
	elif(title == 'flightinfo'):
		air=Airlines.select().where(Airlines.airlineid == airline)
	if not air.exists():
		print('Error424')
		exit()
	aid=Airlines.get().airlineid
	customer=Customers.select().where(Customers.customerid == cid)
	if customer.exists():
		print('Error424')
		exit()
	cname=entry['name']
	cbirthdate=entry['birthdate']
	query=Customers(customerid = cid, name=cname,birthdate=cbirthdate,frequentflieron=aid)
	query.save(force_insert = True)
	return

for entry in data:
	if 'newcustomer' in entry:
		insert_customer(entry['newcustomer'],'newcustomer')
	if 'flightinfo' in entry:
		for cust in entry['flightinfo']['customers']:
			cid=cust['customerid']
			fid=entry['flightinfo']['flightid']
			fdate=entry['flightinfo']['flightdate']
			temp=Customers.select().where(Customers.customerid == cid)
			if not temp.exists():
				insert_customer(cust,'flightinfo')
			temp=Flewon(flightid=fid,customerid=cid,flightdate=fdate)
			temp.save(force_insert=True)
	if 'airlines' in entry:
		num=int(entry['airlines']['howmany'])
		result =(Airlines.select(Airlines.name, fn.count(Customers.customerid).alias('n'))
			.join(Customers,on=(Customers.frequentflieron==Airlines.airlineid))
			.group_by(Airlines.name)
			.order_by(fn.count(Customers.customerid).desc(),Airlines.name.asc())
			.limit(num))
		for line in result:
			print(line.name,line.n,end='\n')
