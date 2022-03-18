import pandas as pd
import random
import datetime
from faker import Faker
from faker.providers import BaseProvider
from collections import defaultdict
from sqlalchemy import create_engine

fake = Faker()

# Create new dynamic providers that generate specific info

# One list per table
# Actors have first name, last name
actor_data = defaultdict(list)

# Use methods in faker to generate data in list
# Because defaultdict(list) was used, whenever a key is accessed
# that hasn't been created, it'll automatically be added w/ empty
# list as value

for i in range(200):
    actor_data["first_name"].append(fake.first_name())
    actor_data["last_name"].append(fake.last_name())

# Category
# has Name
category_data = defaultdict(list)

category_names = ["Action", "Animation", "Children", "Classics", "Comedy", "Documentary",
"Drama", "Games", "Horror", "Musical", "Sci-Fi", "Sports", "Thriller"]

for i in range(len(category_names)):
    state_data["category_name"].append((category_names)[i])

# City
# has City (name)
city_data = defaultdict(list)

city_names = ["Seattle", "Portland", "Los Angeles", "New York", "Boulder", "Austin",
"Atlanta", "Chicago", "San Francisco", "San Diego"]

for i in range(len(city_names)):
    state_data["city_name"].append((city_names)[i])

# Customer
# has store ID, first and last name, City ID, create date, last rental?

customer_data = defaultdict(list)

for i in range(500):
    customer_data["first_name"].append(fake.first_name())
    customer_data["last_name"].append(fake.last_name())

# Film
# has Title (two word combo)
# release year, language ID, original language ID, rental_duration, category
# rental price, length in minutes, replacement_costs, rating, special features

film_data = defaultdict(list)


# Film_actor bridges film and actor tables.
# Every film needs at least 2 actors, up to like 10?

# Roll dice from 1 - 10
# TODO test all of this
for i in range(len(film_data)):
    total_actors = random.randrange(10)
    for j in range(total_actors):
        actor_id = random.randrange(len(actor_data))
        actor_full_name = actor_data.get("first_name")[actor_id]
        film_data["film_id"].append(actor_full_name)

# Film text is a generated description of a movie in format:
# " A ?adj ?film_type of a ?noun and a ?noun who ?action a ?noun in ?location"
film_text_data = defaultdict(list)


# Inventory has film ID, store ID, and an update (purchase?) update
# smthg like for i in film.id for j in store.id generate 1:10 copies

# Language has name - can probably just manually make this guy its only 8ish rows

# location
# Has city id and state id


# Line item
# Has ID, film ID, transaction ID, payment amount

# Rental
# Line item ID (not transaction), rental date, return date
# Return date being some kind of function of rental length?
# Like rand(rental_duration - 2):(rental_duration + 2)

# Staff first name, last name, email (same formula), store_id, active

staff_data = defaultdict(list)

for i in range(5):
    staff_data["first_name"].append(fake.first_name())
    staff_data["last_name"].append(fake.last_name())
    staff_email = staff_data.get("first_name")[i] + staff_data.get("last_name")[i] + "@company.com"
    staff_data["email"].append(staff_email)
    # Store ID
    # Active employee - weight towards Y

# State
# Has id, name
state_data = defaultdict(list)

state_names = ["Washington", "Oregon", "California", "New York", "Colorado", "Texas",
"Georgia", "Illinois"]

for i in range(len(state_names)):
    state_data["state_name"].append((state_names)[i])

# STORE
# has manager_staff_id, City id, opening date
store_data = defaultdict(list)

for i in range(100):
    random_city_id = random.randrange(1, len(city_names), 1)
    store_data["city_id"].append(random_city_id)

    random_employee_id = random.randrange(1, len(staff_data),1)
    store_data["city_id"].append(random_employee_id)

    opening_date = datetime.date(1990,6,23)
    current_date = datetime.date(2007,3,9)
    store_data["opening_date"].append(fake.date_between_dates(opening_date, current_date))

# transaction
# Has ID, staff id, customer id, store id (maybe?), total amount, rental date,
transaction_data = defaultdict(list)
