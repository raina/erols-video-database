# jackolantern-video-database
A fake movie rental database to practice using SQL queries

## History and Inspiration
I was inspired to create this database generator when I realized how few databases exist where people
who are new to SQL can practice writing queries. More importantly, it's really hard to find databases
where the information isn't randomly generated, so that users can practice asking questions of a database. Instead of needing to create an entire database by hand, I created a script that dynamically generates a database based on a few parameters. Across all the tables, I have tried to maintain logical consistency so that insights could be found and visualizations made - ex. movies cannot be in a store's inventory until after their release date. Ideas to expand the functionality of this tool are greatly appreciated!

The format of this database, a fake video store company, was inspired by [Oracle's Sakila Database](https://dev.mysql.com/doc/sakila/en/sakila-introduction.html).

Name inspired by Seattle's [Scarecrow Video](https://www.scarecrow.com/index.html). If you're in town,
go rent some videos!

## How to Use the Database
If you just want to have a sample database to practice queries and analysis with, download `SCRIPT NAME.sql` and open it in MySQL to generate the database.

If you want to make changes to any of the below assumptions or change the number of films, stores, etc., download the Python file `create_data_script.py` and change the variables at the top listed under "Constants" to reflect what you want the database to contain. Also, you will need to change the "engine" line to point to your own database - instructions for that are in the file. Run the script and all the data will be generated to the specified schema. The only manual step is creating the foreign keys in MySQL and marking ID's as primary keys (I'm hoping to add that functionality in a future version).

## Database Facts and Assumptions

#### Company
- The company opened June 23, 1990
- This database "snapshot" is from March 9, 2007 (latest possible date)

#### Movies
- Movies were released between 1970 and 2007
- Rentals are either $3, $5, or $7
- Movie release dates are weighted to favor recent movies, with only some new releases
- Languages are weighted to have primarily English films, a few Japanese, and a
small number of other languages
- Movie ratings loosely follow a real life distribution:

| G    | PG   | PG-13 | R    |NC-17 |
| :--- | :--- | :---  | :--- | :--- |
| 5%   | 10%  | 70%   | 10%  | 5%   |

- Movies have between 1-3 special features and 1-10 unique actors
- Movies are 90-180 minutes long
- Movies only release on January 1 of their release year

#### Stores and Inventory
- Each state only has one city with a store
- Each store has between 1-4 copies of each movie
- Transactions are broken down into individual movie rentals.
- Each rental tracks when a movie left the store and when it was returned. Rentals tend to be returned either a day early or on time, but are sometimes returned late.
- Movies only enter inventory after their release date
- Employees have an "active" status - 1 is a currently employed person, 0 is a former employee
(They treat their staff well, and thus has a very high retention rate)
- Customers cannot rent before they join a store, and they only rent from their "main" store
