queries = ["" for i in range(0, 11)]

### 0. List all airport codes and their cities. Order by the city name in the increasing order. 
### Output column order: airportid, city

queries[0] = """
select airportid, city 
from airports
order by city;
"""

### 1. Write a query to find the names of the customers whose names are at least 15 characters long, and the second letter in the  name is "l".
### Order by name.
queries[1] = """
select customers.name
from customers
where name like '_l%'and length(name)>=15
order by name;
"""


### 2. Write a query to find any customers who flew on their birthday.  Hint: Use "extract" function that operates on the dates. 
### Order output by Customer Name.
### Output columns: all columns from customers
queries[2] = """
select customers.*
from customers natural join flewon
where extract(month from birthdate)=extract(month from flightdate) and extract(day from birthdate)=extract(day from flightdate)
order by name;
"""

### 3. Write a query to generate a list: (source_city, source_airport_code, dest_city, dest_airport_code, number_of_flights) for all source-dest pairs with at least 3 flights. 
### Order first by number_of_flights in decreasing order, then source_city in the increasing order, and then dest_city in the increasing order.
### Note: You must generate the source and destination cities along with the airport codes.
queries[3] = """
select s.city, source, d.city, dest, count(*) as number_of_flights
from flights, airports as s, airports as d
where flights.source = s.airportid and flights.dest = d.airportid
group by s.city, source, d.city, dest
having count(*) >=3
order by number_of_flights desc, s.city asc, d.city asc;
"""

### 4. Find the name of the airline with the maximum number of customers registered as frequent fliers.
### Output only the name of the airline. If multiple answers, order by name.
queries[4] = """
with max as(
	select frequentflieron as airlineid, count(*) as num
	from customers
	group by frequentflieron
	)
select name
from max natural join airlines
where num=(select max(num) from max)
order by name;
"""

### 5. For all flights from OAK to IAD, list the flight id, airline name, and the 
### duration in hours and minutes. So the output will have 4 fields: flightid, airline name,
### hours, minutes. Order by flightid.
queries[5] = """
with dur as(
	select flightid,name,(local_arrival_time-local_departing_time) as duration
	from flights natural join airlines
	where source='OAK' and dest='IAD'
	)
select flightid, name, extract(hours from duration) hours, extract(minutes from duration) minutes
from dur
order by flightid;
"""

### 6. Write a query to find all the empty flights (if any); recall that all the flights listed
### in the flights table are daily, and that flewon contains information for a period of 10
### days from Jan 1 to Jan 10, 2010. For each such flight, list the flightid and the date.
### Order by flight id in increasing order, and then by date in increasing order.
queries[6] = """
with distin as (
    select distinct flightdate
    from flewon
	) 
select flightid, flightdate
from flights, distin
except
select flightid, flightdate
from flewon
order by flightid asc, flightdate asc;
"""

### 7. Write a query to generate a list of customers who don't list Southwest as their frequent flier airline, but
### actually flew the most (by number of flights) on that airline.
### Output columns: customerid, customer_name
### Order by: customerid
queries[7] = """
with count_num as(
	select customerid, airlineid, count(*) as num
	from flights natural join flewon
	group by customerid, airlineid
	),
max_SW as(
	select customerid
	from count_num as c1
	where num=(select max(num) from count_num as c2 where c1.customerid=c2.customerid) and airlineid='SW'
	)
select customers.customerid,name
from customers,max_SW
where customers.customerid=max_SW.customerid and customers.frequentflieron!='SW'
order by customerid;
"""

# fall17
### 8. Write a query to generate a list of customers where the interval between first and last flight is 5 days.
### Order by the customer name. 
queries[8] = """
with first as(
	select customerid,min(flightdate) as min_f
	from flewon
	group by customerid
	),
last as(
	select customerid,max(flightdate) as max_f
	from flewon
	group by customerid
	)
select distinct c.name
from customers as c natural join first natural join last
where extract(year from max_f)=extract(year from min_f) and extract(month from max_f)=extract(month from min_f) 
and abs(extract (day from max_f)-extract(day from min_f))=5
order by c.name;
"""


# fall17
### 9. Name of customer whose max interval between any two consecutive flights is 4 days.
### The output should be simply a list of names
### Order by the customer name. 
queries[9] = """
with first as(
	select row_number() over (order by customerid,flightdate) as id, customerid,flightdate as f1 from flewon
	),
second as(
	select row_number() over (order by customerid,flightdate)+1 as id, customerid,flightdate as f2 from flewon
	),
together as(
	select name,f1,f2 from first natural join second natural join customers
	),
final as(
	select name,max(f1-f2) as num
	from together
	group by name)
select name from final where num=4 order by name;
"""

### 10. Write a query that outputs a list: (AirportID, Airport-rank), where we rank the airports 
### by the total number of flights that depart that airport. So the airport with the maximum number
### of flights departing gets rank 1, and so on. If two airports tie, then they should 
### both get the same rank, and the next rank should be skipped.
### Order the output in the increasing order by rank.

queries[10] = """
with count_num as(
	select source as id, count(*) as num
	from flights
	group by source
	)
select id,(
	select count(*)
	from count_num as c2
	where c2.num>c1.num)+1 as rank
from count_num as c1
order by rank,id;
"""

