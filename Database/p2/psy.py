#!/usr/bin/python3
import psycopg2
import os
import sys
import datetime
import json
from types import *
import sys

if len(sys.argv) != 2:
    print("USAGE: {:s} <JSON file>".format(sys.argv[0]))
    exit()

conn = psycopg2.connect("dbname=flightsskewed user=ubuntu password=ubuntu")
curs = conn.cursor()

with open(sys.argv[1]) as f:
	data=[]
	for line in f:
		data.append(json.loads(line))
f.close()

def insert_customer(entry,title):
	cid=entry['customerid']
	airline=entry['frequentflieron']
	if(title == 'newcustomer'):
		curs.execute("select airlineid from airlines where name = %s",(airline,))
	elif(title == 'flightinfo'):
		curs.execute("select airlineid from airlines where airlineid = %s",(airline,))
	if curs.rowcount == 0:
		print('Error424')
		exit()
	aid=curs.fetchone()
	curs.execute("select * from customers where customerid = %s",(cid,))
	if curs.rowcount != 0:
		print('Error424')
		exit()
	name=entry['name']
	birthdate=entry['birthdate']
	curs.execute("insert into customers(customerid, name, birthdate, frequentflieron) \
	values (%s, %s, %s, %s)",(cid, name, birthdate, aid))
	return

for entry in data:
	if 'newcustomer' in entry:
		insert_customer(entry['newcustomer'],'newcustomer')
	if 'flightinfo' in entry:
		for cust in entry['flightinfo']['customers']:
			cid=cust['customerid']
			fid=entry['flightinfo']['flightid']
			fdate=entry['flightinfo']['flightdate']
			curs.execute("select customerid from customers where customerid = %s",(cid,))
			if(curs.rowcount == 0):
				insert_customer(cust,'flightinfo')
			curs.execute("insert into flewon(flightid, customerid, flightdate) \
			values (%s, %s, %s)",(fid,cid,fdate))
	if 'airlines' in entry:
		n=entry['airlines']['howmany']
		curs.execute("with temp (fid,num) as (\
			select frequentflieron, count(customerid)\
			from customers\
			group by frequentflieron)\
			select a.name, num from airlines a,temp\
			where a.airlineid=fid\
			order by num desc, a.name asc limit %s",(n,))
		result = curs.fetchall()
		for line in result:
			print(line[0],line[1],end='\n')
conn.commit()
curs.close()
conn.close()
