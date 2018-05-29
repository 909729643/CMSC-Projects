## Project 2: Advanced SQL, Python DB app, ORMs, CMSC424-0201, Fall 2017
### Due Oct. 1, 2017, 11:59PM

*The assignment is to be done by yourself.*

### Setup

As before we have created a VagrantFile for you. The main differences here are that we have loaded a skewed database (`flightsskewed`), and also installed Java. Start by doing `vagrant up` and `vagrant ssh` as usual.

However, this repository is hosted through *gitlab.cs.umd.edu*, not github, so the command
to clone it is:

    git clone https://gitlab.cs.umd.edu/keleher/p2.git

Ensure that the Vagrantfile has loaded
the `flightsskewed` database, together with tables populated from  `large-skewed.sql`. Use
`flightsskewed` for all parts of this assignment.

### Assignment Questions

**Question 1 (.5 pt)**: Consider the following query which finds the number of flights
  taken by users whose name starts with 'William'.

```
select c.customerid, c.name, count(*)
from customers c join flewon f on (c.customerid = f.customerid and c.name like 'William%')
group by c.customerid, c.name
order by c.customerid;
```

The result however does not contain the users whose name contains 'William' but who did
not fly at all (e.g., `cust731`). So we may consider
modifying this query to use a left outer join instead, so we get those users as well:

```
select c.customerid, c.name, count(*)
from customers c left outer join flewon f on (c.customerid = f.customerid and c.name like 'William%')
group by c.customerid, c.name
order by c.customerid;
```

Briefly explain why this query does not return the expected answer (as below), and rewrite the query so that it does.

The final answer should look like this:
```
	customerid |              name              | count
	------------+--------------------------------+-------
	cust727    | William Harris                 |     4
	cust728    | William Hill                   |     6
	cust729    | William Jackson                |     6
	cust730    | William Johnson                |     5
	cust731    | William Lee                    |     0
	cust732    | William Lopez                  |     6
	cust733    | William Martinez               |     0
	cust734    | William Mitchell               |     6
	cust735    | William Moore                  |     5
	cust736    | William Parker                 |     4
	cust737    | William Roberts                |     8
	cust738    | William Robinson               |     7
	cust739    | William Rodriguez              |     5
	cust740    | William Wright                 |     8
	cust741    | William Young                  |     5
	(15 rows)
```

Save your query in a file called `william.sql`.
Include your explanation as a comment in this file.

---
**Question 2 (1.5 pt)**: [Trigger]
Let's create a table `NumberOfFlightsTaken(customerid, customername, numflights)` to keep track of the total number of flights taken by each customer. Since this is a derived table (and not a view), it will not be kept up-to-date by the database system.  Use the following command for doing this:
```
create table NumberOfFlightsTaken as
select c.customerid, c.name as customername, count(*) as numflights
from customers c join flewon fo on c.customerid = fo.customerid
group by c.customerid, c.name;
```

Write a `trigger` to keep this new table updated when a new entry is inserted into or a row is deleted from the `flewon` table. Remember the customerid corresponding to the new flewon update may not exist in the `NumberOfFlightsTaken` table at that time and it should be added to the table with a count of 1, in that case. Similarly, if a deletion of a row in `flewon` results in a user not having any flights, then the corresponding tuple for that user in `NumberOfFlightsTaken` should be deleted.

The trigger code should be submitted in `trigger.sql` file, as straight SQL. Running `psql
-f trigger.sql flightsskewed` should generate the trigger without errors.

The trigger
file you are given contains some (incorrect) code already, but must be corrected and expanded.

---
**Question 3 (2 pt)**:  One of more prominent ways to use a database system is using an
external client, using APIs such as ODBC and JDBC, or the
Python DB-API 2.0 specification.

We will be using the [psycopg](http://initd.org/psycopg/) instantiation of the Python DB spec to access the
database. There are many good tutorials, such as this
[Postgres/psycopg Tutorial](http://www.postgresqltutorial.com/postgresql-python),
the [default documentation](http://initd.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries) is quite good,
and you can also
get see a working example of queries in *SQLTesting.py* from Project 1.

For those new to Python, I recommend the
[Python Tutorial](https://docs.python.org/3/tutorial/index.html).

Your task to write a Python program that will take in JSON updates and insert appropriate
data into the database.

1. You program is called with a single parameter: `python3 psy.py <inputfile>`.
1. Each line in the input file will consist of a single JSON object in one of the following three formats:


- New customer, where information about a customer is provided in the following format
  (though our example file has each input in a single line). You can assume that the
  frequent flier airline name matches exactly what is there in the 'airlines' table.

```
{ "newcustomer": {
    "customerid": "cust1000",
    "name": "XYZ",
    "birthdate": "1991-12-06",
    "frequentflieron": "Southwest Airlines"
    }
}
```

- Flight information, where information about the passengers in a flight is
  provided. Create new rows in `flewon` for each customer, as well as the `customers`
  table if the `customerid` does not already exist.
  - In some cases the `customer_id` provided may not be present in the database (cust1000 as seen below). In this case, first update the `customers` table (all the info is guaranteed to be
  there), and then add tuples to the `flewon` table.

```
{ "flightinfo": {
    "flightid": "DL119",
    "flightdate": "2015-09-25",
    "customers": [
        {"customer_id": "cust94"},
        {"customer_id": "cust102"},
        {"customer_id": "cust1000", "name": "XYZ", "birthdate": "1991-12-06", "frequentflieron": "DL"}
        ]
    }
}
```



- Airlines (a query), where you print airline names, together with a count of how many customers list each as their `frequentflieron`. Order by the count, and then airline name. Print a maximum of
  `howmany` lines. The number of spaces between name and count is not important.
```
{ "airlines": {
    "howmany": 3,
    }
}
```

For example, in response to the above you should print:

    JetBlue              95
    United Airlines      92
    Delta Airlines       88



Notes:

1. In the case of either of the following errors, you should just print "Error424" and then exit. You do not need to handle any other errors.
  - If the `customerid` for a `newcustomer` update is already present, or
  - if the `frequentflieron` does not have a match in the airlines table
2. Be sure to *commit()* and then *close()* the database connection at the end. Without
the commit, no data will be modified.
3. `example.json` is an example input file.  
4. There are many Python JSON parsing libraries, but the simplest to use is the
[json module](https://docs.python.org/3/library/json.html) from the
[Python standard library](https://docs.python.org/3/library/).
5. `./clean-example.py` will remove the tuples added from `example.py`
6. `./test-example.py pys.py` will run your code and print the results


---
**Question 4 (2 pt)**:  Another way to use a database is through an
  object-relational-mapping (ORM), which maps table rows onto objects that are visible in a
  programming language. The result is that you can write a database application without
  using SQL at all.

We will re-write the previous program with exactly the same semantics, but using an object
model approach instead. Notes:
1. There are many python ORMs, including [Django](https://www.djangoproject.com/), but we
will use the simpler [peewee](https://github.com/coleifer/peewee).
1. Peewee's distribution includes a tool called `pwiz`, which uses database
   *introspection* to create python classes mirroring an existing postgres schema. You
   should use this as follows:

		pwiz.py -e postgresql -u ubuntu -P flightsskewed > orm.py

   The password is `ubuntu`. This will create the scaffolding of your ORM program in `orm.py`.

1. Test this code by:
- add the following to the top of `orm.py`: `from datetime import date`
- Eliminate blank lines before "    class Meta:" lines, i.e. get rid of any blank lines
   within class definitions (or ensure that proper indentation is maintained by adding spaces).
- Add the following lines to the end of the file:

```
bob = Customers(name="bob", customerid='cust1010', birthdate='1960-01-15', frequentflieron='SW')
bob.save(force_insert=True)

bwi = Airports(airportid='PET', city='Takoma', name='Pete', total2011=2, total2012=4)
bwi.save(force_insert=True)

for port in Airports.select().order_by(Airports.name):
    print (port.name)
```

- Run by typing `python3 orm.py` from the shell. You should see a record added to each of
  *customers* and *airports*, followed by a listing of all airport names.

Remove the above lines and continue modifying `orm.py` to implement the same changes to
the database as in `psy.py` (read JSON strings, insert corresponding tuples into the
database), but do so entirely through the **Peewee** ORM interface.

Don't forget to `.save(force_insert=True)` new tuples or they will not be committed to the
database.

`clean-example.py` and `./test-example.py orm.py` work as in the last question.

## Submit Instructions
Submit `william.sql`, `trigger.sql`, `psy.py`, and  `orm.py` files by creating a single
tarball, *tar cvfz p2.tgz answers.docx trigger.sql psy.py orm.py*, and
uploading [here](https://myelms.umd.edu/courses/1218383/assignments/4378989).
