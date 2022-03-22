import pandas as pd
import random
import datetime
from faker import Faker
from faker.providers import BaseProvider
from faker.providers import DynamicProvider
from collections import defaultdict
from sqlalchemy import create_engine

fake = Faker()

# Create function to randomize outcome with weights
# Might want to somehow refactor this depending on what use cases end up being
def weighted_random(weight1,weight2,lower1,upper1,lower2,upper2,lower3,upper3):

    x = random.randint(1,100)

    if x <= weight1:
        num = random.randrange(lower1,upper1)
        return num
    elif x > weight1 and x <= weight2:
        num = random.randrange(lower2,upper2)
        return num
    else:
        num = random.randrange(lower3,upper3)
        return num

# new dynamic providers to generate specific info

# Movie Name provider
movie_name_provider = DynamicProvider(
    provider_name = "movie_name",
    elements=["Battle", "Mage", "New York", "Alien", "Cowboy", "Space", "Pirate",
    "Showdown", "Magic", "Dog", "Office", "Robot", "Party", "Night", "Day", "Tree",
    "Sasquatch", "Water", "Fire", "Earth", "Air", "Tree", "Park"]
)

fake.add_provider(movie_name_provider)

# Special features providers
special_features_provider = DynamicProvider(
provider_name = "special_features",
elements=["Deleted Scenes", "Director's Cut", "Director Commentary", "Interviews",
"Behind The Scenes"]
)

fake.add_provider(special_features_provider)

# -----------------------------------------------------------------------------

# Actors
# has first name, last name
actor_data = defaultdict(list)

# Use methods in faker to generate data in list
# Because defaultdict(list) was used, whenever a key is accessed
# that hasn't been created, it'll automatically be added w/ empty
# list as value

for i in range(20):
    actor_data["actor_id"].append(i + 1)
    actor_data["first_name"].append(fake.first_name())
    actor_data["last_name"].append(fake.last_name())

df_actor_data = pd.DataFrame(actor_data)
# -----------------------------------------------------------------------------

# Category
# has Name
category_data = defaultdict(list)

category_names = ["Action", "Animation", "Children", "Classics", "Comedy", "Documentary",
"Drama", "Games", "Horror", "Musical", "Sci-Fi", "Sports", "Thriller"]

for i in range(len(category_names)):
    category_data["category_id"].append(i+1)
    category_data["category_name"].append((category_names)[i])

df_category_data = pd.DataFrame(category_data)
# -----------------------------------------------------------------------------

# City
# has City (name)
city_data = defaultdict(list)

city_names = ["Seattle", "Portland", "Los Angeles", "New York", "Boulder", "Austin",
"Atlanta", "Chicago"]

for i in range(len(city_names)):
    city_data["city_id"].append(i + 1)
    city_data["city_name"].append((city_names)[i])

df_city_data = pd.DataFrame(city_data)
# -----------------------------------------------------------------------------

# Customer
# has store ID, first and last name, City ID, create date
customer_data = defaultdict(list)

for i in range(500):
    customer_data["customer_id"].append(i+1)
    customer_data["first_name"].append(fake.first_name())
    customer_data["last_name"].append(fake.last_name())

    opening_date = datetime.date(1990,6,23)
    current_date = datetime.date(2007,3,9)
    customer_data["joined_on"].append(fake.date_between_dates(opening_date, current_date))
    customer_data["city_id"].append(random.randrange(1, len(city_names)))

df_customer_data = pd.DataFrame(customer_data)
# -----------------------------------------------------------------------------

# Film
# has Title (two word combo), release year, language ID, rental_duration, category
# rental price, length in minutes, replacement_costs, rating, special features

film_data = defaultdict(list)

for i in range(25):
    film_data["film_id"].append(i + 1)

    two_word_title = fake.movie_name() + " " + fake.movie_name()
    film_data["title"].append(two_word_title)

    # Weight movie releases to favor more recent (but not brand-new) releases
    release_year = weighted_random(5,90,1970,1980,1981,2005,2006,2007)
    film_data["release_year"].append(release_year)

    # Weight language id
    x = random.randint(1,100)
    if x <= 8:
        language_id = 2
    elif x > 8 and x <= 90:
        language_id = 1
    else:
        language_id = random.randrange(3,7)

    film_data["language_id"].append(language_id)

    duration = random.randrange(3,7,1)
    film_data["rental_duration"].append(duration)

    category_id = random.randrange(len(category_data))
    film_data["category_id"].append("category_id")

    rental_price = random.randrange(3,8,2) # Rentals are either 3,5 or 7
    film_data["rental_price"].append(rental_price)

    film_data["length"].append(random.randrange(90,180))

    replacement_price = round(random.uniform(10,25), 2)
    film_data["replacement_price"].append(replacement_price)

    # Weight rating id
    x = random.randint(1,100)
    if x <= 5:
        rating_id = 1
    elif x > 5 and x <= 15:
        rating_id = 2
    elif x > 15 and x <= 85:
        rating_id = 3
    elif x > 85 and x <= 95:
        rating_id = 4
    else:
        rating_id = 5

    film_data["rating_id"].append(rating_id)

    # Adds list of 1-3 special features
    features_list = []
    features_number = random.randrange(1,3)

    for j in range(features_number):
        features_list.append(fake.special_features())

    final_list = list(set(features_list)) # Removes any duplicates
    film_data["special_features"].append(final_list)

df_film_data = pd.DataFrame(film_data)
# -----------------------------------------------------------------------------
# Film_actor bridges film and actor tables.
# Every film needs at least 2 actors, up to like 10
film_actors_data = defaultdict(list)

for i in range(25): #TODO rm magic number
    total_actors = random.randrange(2,10)
    for j in range(total_actors):
        actor_id = random.randrange(1,20) #Grab random actor id
        actor_full_name = actor_data.get("first_name")[actor_id] + " " + actor_data.get("last_name")[actor_id]
        film_actors_data["film_id"].append(actor_full_name)

df_film_actors_data = pd.DataFrame(film_actors_data)
# -----------------------------------------------------------------------------

# Film text is a generated description of a movie in format:
# " A ?adj ?film_type of a ?noun who ?action a ?noun in ?location"
film_text_data = defaultdict(list)

adj_list = ["striking", "lovely", "exciting", "sorrowful", "poignant",
"hilarious", "uninspired", "original", "inspirational", "adventurous"]

film_type_list = ["tale", "epic", "story", "account", "saga", "documentary",
"drama", "portrayal", "adventure", "film"]

noun_list = ["a firefighter", "a witch", "an explorer", "a monkey",
"a dog", "a teacher", "a programmer", "an olympic athlete", "a superhero", "an alien"]

action_list = ["fights", "deceives", "saves", "builds", "fixes", "destroys",
"encourages", "races", "fights", "deceives", "befriends", "helps"]

location_list = ["space", "the desert", "New York", "Seattle", "the ocean",
"an abandoned power plant", "a haunted house", "area 51", "a park", "a new planet",
"a small town", "a cruise ship", "a school", "the forest", "a cabin in the woods",
"a cafe"]

for i in range(len(film_data)):
    film_text_data["film_id"].append(i + 1)

    # Allows for any size of list of words
    description_adj = adj_list[random.randrange(0,len(adj_list))]
    description_type = film_type_list[random.randrange(0,len(film_type_list))]
    description_noun = noun_list[random.randrange(0,len(noun_list))]
    description_action = action_list[random.randrange(0,len(action_list))]
    description_noun_2 = noun_list[random.randrange(0,len(noun_list))]
    description_location = location_list[random.randrange(0,len(location_list))]

    film_description =  "A " + description_adj + " " + description_type + " of " + description_noun + " who " + description_action + " " + description_noun_2 + " in " + description_location + "."

    film_text_data["film_description"].append(film_description)

df_film_text_data = pd.DataFrame(film_text_data)
# -----------------------------------------------------------------------------
# Inventory
# has film ID, store ID, and purchase date

# This one might need to just do auto-incrementing ID
# OR a second loop that adds ID based on len of list

inventory_data = defaultdict(list)

for i in range(25): #Rm the magique number (number of films)
    for j in range(100): #Rm the magic-tastic number (number of stores)
        num_of_copies = random.randint(1,4) # Between 1 and 4 copies of each movie per store
        for k in range(num_of_copies):
            inventory_data["film_id"].append(i + 1)
            inventory_data["store_id"].append(j + 1)

            opening_date = datetime.date(1990,6,23)
            current_date = datetime.date(2007,3,9)
            inventory_data["purchase_date"].append(fake.date_between_dates(opening_date, current_date))

df_inventory_data = pd.DataFrame(inventory_data)
# -----------------------------------------------------------------------------

# Language
# has ID and name
language_data = defaultdict(list)

language_names = ["English", "Japanese", "Spanish", "French", "Mandarin",
"Italian", "German"]

for i in range(len(language_names)):

    language_data["language_id"].append(i + 1)
    language_data["language_name"].append((language_names)[i])

df_language_data = pd.DataFrame(language_data)
# -----------------------------------------------------------------------------

# location
# Has city id and state id
# This only works because city and state name lists are manually typed in the right order.
location_data = defaultdict(list)

for i in range(len(city_names)):
    location_data["state_id"].append(i + 1)
    location_data["city_id"].append(i + 1)

df_location_data = pd.DataFrame(location_data)
# -----------------------------------------------------------------------------

# Line item
# Has ID, film ID, transaction ID, price
# -----------------------------------------------------------------------------

# mpa_rating
# has id, name
rating_data = defaultdict(list)

ratings = ["G", "PG", "PG-13", "R", "NC-17"]

for i in range(len(ratings)):

    rating_data["rating_id"].append(i + 1)
    rating_data["mpa_rating"].append((ratings)[i])

df_rating_data = pd.DataFrame(rating_data)
# -----------------------------------------------------------------------------

# Rental
# Line item ID (not transaction), rental date, return date
# Return date is a function of rental length
# Like rand(rental_duration - 2):(rental_duration + 2)
# -----------------------------------------------------------------------------

# Staff
# has first name, last name, email, store_id, active

staff_data = defaultdict(list)

for i in range(5):
    staff_data["staff_id"].append(i+1)
    staff_data["first_name"].append(fake.first_name())
    staff_data["last_name"].append(fake.last_name())
    staff_email = staff_data.get("first_name")[i] + staff_data.get("last_name")[i] + "@company.com"
    staff_data["email"].append(staff_email)
    # Store ID
    # Active employee - weight towards Y

df_staff_data = pd.DataFrame(staff_data)
# -----------------------------------------------------------------------------

# State
# Has id, name
state_data = defaultdict(list)

state_names = ["Washington", "Oregon", "California", "New York", "Colorado", "Texas",
"Georgia", "Illinois"]

for i in range(len(state_names)):
    state_data["state_id"].append(i+1)
    state_data["state_name"].append((state_names)[i])

df_state_data = pd.DataFrame(state_data)
# -----------------------------------------------------------------------------

# STORE
# has manager_staff_id, City id, opening date
store_data = defaultdict(list)

for i in range(10):
    random_city_id = random.randrange(1, len(city_names), 1)
    store_data["city_id"].append(random_city_id)

    random_employee_id = random.randrange(1, len(staff_data),1)
    store_data["city_id"].append(random_employee_id)

    opening_date = datetime.date(1990,6,23)
    current_date = datetime.date(2007,3,9)
    store_data["opening_date"].append(fake.date_between_dates(opening_date, current_date))

# df_store_data = pd.DataFrame(store_data)
# -----------------------------------------------------------------------------

# transaction
# consists of multiple line items
# Has ID, staff id, customer id, store id, total amount, rental date

# This should probably go Like
# Every customer has home store and at least one transaction
# Every store has certain employees who could do transaction
# Total amount is kinda tricky so maybe that's done in db?

transaction_data = defaultdict(list)

for i in range(10):
    transaction_data["transaction_id"].append(i + 1)
    transaction_data["total_paid"].append(15) #TODO rm, for testing only

df_transaction_data = pd.DataFrame(transaction_data)
# -----------------------------------------------------------------------------
# Add data to testdb schema
engine = create_engine('mysql://root:rootroot@localhost/testdb', echo=False)

# This can defs be a function
df_actor_data.to_sql('actor', con=engine, index=False)
df_category_data.to_sql('category', con=engine, index=False)
df_city_data.to_sql('city', con=engine, index=False)
df_customer_data.to_sql('customer', con=engine, index=False)
# df_film_data.to_sql('film', con=engine, index=False) errors exist, "operand should contain one column" - PROBABLY special features col
df_film_text_data.to_sql('film_text', con=engine, index=False)
df_language_data.to_sql('language', con=engine, index=False)
df_location_data.to_sql('location', con=engine, index=False)
df_rating_data.to_sql('mpa_rating', con=engine, index=False)
df_staff_data.to_sql('staff', con=engine, index=False)
df_transaction_data.to_sql('transactions', con=engine, index=False)

# -----------------------------------------------------------------------------
