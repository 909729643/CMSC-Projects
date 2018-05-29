select c.customerid, c.name, count(f.customerid)
from customers c left outer join flewon f on (c.customerid = f.customerid)
where c.name like 'William%'
group by c.customerid, c.name
order by c.customerid;

#First Query: Since some users'names contain William but did not fly at all, the flewon table doesn't contain their customerid, 
#so the result will drop their id because the f.customerid is null.
#Second Query: left outer join will return all values of the left table so all customerid of customers will display
#and we should count f.customerid since some customer did not fly so their f.customerid is null, if we use count(*), the count
#will be 1 but the right count should be 0.