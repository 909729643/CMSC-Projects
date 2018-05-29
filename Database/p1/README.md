## Project 1: SQL Assignment, CMSC424-0201, Fall 2017

*The assignment is to be done by yourself.*

The following assumes you cloned `p1` as `git clone https://gitlab.cs.umd.edu/keleher/p1.git`.

1. README.md: This file.
1. small.sql: The SQL script for creating the data.
1. queries.py: The file where to enter your answer; this is the file to be submitted
1. answers.py: The answers to the queries on the small dataset.
1. SQLTesting.py: File to be used for testing your submission -- see below.
1. Vagrantfile: A Vagrantfile that creates the 'flights' database and populates it using `small.sql` file.

**Note:** The testing will be done on a different, larger dataset. 

### Schema 
The dataset contains synthetic air flight data. Specifically it contains the following tables:

1. airports: airportid, city, name, total2011, total2012
1. customers: customerid, name, birthdate, frequentflieron
1. airlines: airlineid, name, hub
1. flights: flightid, source, dest, airlineid, local_departing_time, local_arrival_time
1. flewon: flightid, customerid, flightdate

See the provided SQL file for the table definitions.

The dataset was generated synthetically: the airport ids and the cities were chosen from the biggest airports in the US, but the rest of the data is populated randomly. The data will not make sense. For example, two different flights between the same cities may have very different flight durations. The flight times between the cities may not correspond to geographical distances that you know. Some other information about the data:
- **The dates in the *large* database might be different than in the *small*.**
- Each customer may at most take one flight every day.
- The flight times were chosen between 30 minutes to 5 hours randomly.
- All flights are daily (start and end on a single day), and none are overnight. 
- For every flight from city A to city B, there is corresponding return flight from B to A.
- The "flewon" table only contains the flight date -- the flight times must be extracted from the flights table.

In many cases (especially for complex queries or queries involving 
`max` or `min`), you will find it easier to create temporary tables
using the `with` construct. This also allows you to break down the full
query and makes it easier to debug.

You don't have to use the "hints" if you don't want to; there might 
be simpler ways to solve the questions.

### Testing and submitting using SQLTesting.py
Your answers (i.e., SQL queries) should be added to the `queries.py` file. A simple query is provided for the first answer to show you how it works.
You are also provided with a Python file `SQLTesting.py` for testing your answers.

- We recommend that you use `psql` to design your queries, and then paste the queries to the `queries.py` file, and confirm it works.

- SQLTesting takes quite a few options: use `python3 SQLTesting.py -h` to see the options.

- To get started with SQLTesting, do: `python3 SQLTesting.py -v -i` -- that will run each of the queries and show you your answer and correct answer.

- If you want to test your answer to Question 1, use: `python3 SQLTesting.py -q 1`. The program compares the result of running your query against the provided answer (in the `answers.py` file).

- The `-v` flag will print out more information, including the correct and submitted answers etc.

- If you want to test your answers to all questions (this is what we will do), use: `python3 SQLTesting.py` and look at the final total score.

- `-i` flag to SQLTesting will run all the queries, one at a time (waiting for you to press Enter after each query).

- **Note that**: We will basically run this same program on your submitted `queries.py` file, but with the larger dataset; your score on the assignment will 
be score output by the program. The program tries to do partial credits (as you can see in the code). It is very unlikely that your score on the larger, hidden 
dataset will be higher than your score on the provided dataset.  

### Submission Instructions
Submit the `queries.py` file using ELMS  [here](https://myelms.umd.edu/courses/1227917/assignments/4492249). **Due September 17.**
      
### Assignment Questions
See `queries.py` file.
