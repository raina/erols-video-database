import pandas as pd
import random
import datetime
from faker import Faker
from faker.providers import BaseProvider
from faker.providers import DynamicProvider
from collections import defaultdict
from sqlalchemy import create_engine

fake = Faker()

# Constants - set these to determine how many records are generated
number_of_films = 200
number_of_actors = 300
number_of_customers = 1000
number_of_staff = 100
number_of_stores = 20
number_of_transactions = 3000

# Minimums and maximums for various options
min_rental_price = 3
max_rental_price = 7
rental_price_increment = 2 # How many dollars between rental prices
min_rental_duration = 3
max_rental_duration = 7
min_replacement_cost = 10.00
max_replacement_cost = 25.00
max_inventory_copies = 4
max_actors_in_film = 10
max_special_features = 3

# Opening date of the first store, and date the records were taken (latest possible)
opening_date = datetime.date(1990,6,23)
current_date = datetime.date(2007,3,9)

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

# New Dynamic providers to generate specific info
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

# Example of accessing specific value in list
# actor_full_name = actor_data.get("first_name")[actor_id] + " " + actor_data.get("last_name")[actor_id]

# -----------------------------------------------------------------------------
# Actors: ID, first name, last name
actor_data = defaultdict(list)

for i in range(number_of_actors):
    actor_data["actor_id"].append(i + 1)
    actor_data["first_name"].append(fake.first_name())
    actor_data["last_name"].append(fake.last_name())

df_actor_data = pd.DataFrame(actor_data)
# -----------------------------------------------------------------------------
# Category: ID, Name
category_data = defaultdict(list)

category_names = ["Action", "Animation", "Children", "Classics", "Comedy", "Documentary",
"Drama", "Games", "Horror", "Musical", "Sci-Fi", "Sports", "Thriller"]

for i in range(len(category_names)):
    category_data["category_id"].append(i+1)
    category_data["category_name"].append((category_names)[i])

df_category_data = pd.DataFrame(category_data)
# -----------------------------------------------------------------------------
# City: ID, name
city_data = defaultdict(list)

city_names = ["Seattle", "Portland", "Los Angeles", "New York", "Boulder", "Austin",
"Atlanta", "Chicago"]

for i in range(len(city_names)):
    city_data["city_id"].append(i + 1)
    city_data["city_name"].append((city_names)[i])

df_city_data = pd.DataFrame(city_data)

# -----------------------------------------------------------------------------
# Film: Title, release year, language ID, rental duration, category, rental price,
#       length in minutes, replacement cost, rating, special features

film_data = defaultdict(list)

for i in range(number_of_films):
    film_data["film_id"].append(i + 1)

    two_word_title = fake.movie_name() + " " + fake.movie_name()
    film_data["title"].append(two_word_title)

    # Weight movie releases to favor more recent (but not brand-new) releases
    release_year = weighted_random(5,90,1970,1980,1981,2005,2006,2007)
    film_data["release_year"].append(release_year)

    # Weight language id - mainly English, some Japanese, rest other
    x = random.randint(1,100)
    if x <= 8:
        language_id = 2
    elif x > 8 and x <= 90:
        language_id = 1
    else:
        language_id = random.randrange(3,7)

    film_data["language_id"].append(language_id)

    duration = random.randrange(min_rental_duration,max_rental_duration + 1) #Adding one to make correct max
    film_data["rental_duration"].append(duration)

    category_id = random.randrange(len(category_data))
    film_data["category_id"].append("category_id")

    rental_price = random.randrange(min_rental_price,max_rental_price+1,rental_price_increment) #Adding one to make correct max
    film_data["rental_price"].append(rental_price)

    film_data["length"].append(random.randrange(90,180)) # Length in minutes

    replacement_price = round(random.uniform(min_replacement_cost, max_replacement_cost), 2)
    formatted_price = format(replacement_price, '.2f')
    film_data["replacement_price"].append(formatted_price)

    # Weight mpa rating - loosely follows real-life distribution
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

    # Create list of special features
    features_list = set()
    features_number = random.randint(1,3)

    for j in range(features_number):
        features_list.add(fake.special_features())

    features_string = ', '.join(features_list)

    film_data["special_features"].append(features_string)

df_film_data = pd.DataFrame(film_data)
# -----------------------------------------------------------------------------
# Film_actor: bridges film and actor tables
film_actors_data = defaultdict(list)

for i in range(number_of_films):
    total_actors = random.randrange(2,10)
    actor_set = set()

    for j in range(total_actors):
        actor_set.add(random.randrange(1,number_of_actors))

    for actor in actor_set:
        film_actors_data["film_id"].append(i+1)
        film_actors_data["actor_id"].append(actor)

df_film_actors_data = pd.DataFrame(film_actors_data)
# -----------------------------------------------------------------------------
# Film text: is a generated description of a film
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

for i in range(number_of_films):
    film_text_data["film_id"].append(i + 1)

    # Builds words for description, madlibs style
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
# Inventory: film ID, store ID, and purchase date

inventory_data = defaultdict(list)

for i in range(number_of_films):

    for j in range(number_of_stores):
        num_of_copies = random.randint(1,max_inventory_copies)

        for k in range(num_of_copies):
            inventory_data["film_id"].append(i + 1)
            inventory_data["store_id"].append(j + 1)
            movie_release_year = film_data.get("release_year")[i]
            film_release_date = datetime.datetime(movie_release_year,1,1)
            inventory_data["purchase_date"].append(fake.date_between_dates(film_release_date, current_date))

df_inventory_data = pd.DataFrame(inventory_data)
# -----------------------------------------------------------------------------
# Language: ID and name
language_data = defaultdict(list)

language_names = ["English", "Japanese", "Spanish", "French", "Mandarin",
"Italian", "German"]

for i in range(len(language_names)):

    language_data["language_id"].append(i + 1)
    language_data["language_name"].append((language_names)[i])

df_language_data = pd.DataFrame(language_data)
# -----------------------------------------------------------------------------
# location: city id and state id
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
# mpa_rating: id, name
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
# State: id, name
state_data = defaultdict(list)

state_names = ["Washington", "Oregon", "California", "New York", "Colorado", "Texas",
"Georgia", "Illinois"]

for i in range(len(state_names)):
    state_data["state_id"].append(i+1)
    state_data["state_name"].append((state_names)[i])

df_state_data = pd.DataFrame(state_data)
# -----------------------------------------------------------------------------
# STORE: manager_staff_id, City id, opening date
# Depends on CITY table
store_data = defaultdict(list)

for i in range(number_of_stores):

    store_data["store_id"].append(i+1)

    random_city_id = random.randrange(1, len(city_names))
    store_data["city_id"].append(random_city_id)

    store_data["opening_date"].append(fake.date_between_dates(opening_date, current_date))

df_store_data = pd.DataFrame(store_data)
# -----------------------------------------------------------------------------
# transaction
# consists of multiple line items
# Has ID, staff id, customer id, store id, total amount, rental date

# This should probably go Like
# Every customer has home store and at least one transaction
# Every store has certain employees who could do transaction
# Total amount is kinda tricky so maybe that's done in db?

transaction_data = defaultdict(list)

for i in range(number_of_transactions):
    transaction_data["transaction_id"].append(i + 1)
    transaction_data["total_paid"].append(15) #TODO rm, for testing only

df_transaction_data = pd.DataFrame(transaction_data)
# -----------------------------------------------------------------------------
# CUSTOMER: ID, first name, last name, City ID, create date
# Depends on STORE and CITY table
customer_data = defaultdict(list)

for i in range(number_of_customers):
    customer_data["customer_id"].append(i+1)
    customer_data["first_name"].append(fake.first_name())
    customer_data["last_name"].append(fake.last_name())

    store_id = random.randrange(1, number_of_stores)
    customer_data["store_id"].append(store_id)

    store_opening_date = store_data.get("opening_date")[store_id-1]
    customer_data["joined_on"].append(fake.date_between_dates(store_opening_date, current_date))

    store_city_id = store_data["city_id"][store_id-1]
    customer_data["city_id"].append(store_city_id)

df_customer_data = pd.DataFrame(customer_data)
# -----------------------------------------------------------------------------
# STAFF: first name, last name, email, store_id, active
# Depends on STORE table
staff_data = defaultdict(list)

for i in range(number_of_staff):
    staff_data["staff_id"].append(i+1)
    staff_data["first_name"].append(fake.first_name())
    staff_data["last_name"].append(fake.last_name())

    staff_email = staff_data.get("first_name")[i] + staff_data.get("last_name")[i] + "@company.com"
    staff_data["email"].append(staff_email)

    staff_data["store_id"].append(random.randrange(1,number_of_stores))

    activity_dice = random.randint(1,100)
    if activity_dice < 5:
        staff_data["active_employee"].append(0)
    else:
        staff_data["active_employee"].append(1)

df_staff_data = pd.DataFrame(staff_data)
# -----------------------------------------------------------------------------
# Add manager to store
# Depends on STORE and STAFF tables

# Make list of index positions that store_id [i] appears at
#for i in range(number_of_stores):
#    store_id = i
#    city_list = store_data["city_id"]
#    indices = [j for j, x in enumerate(my_list) if x == store_id]

# -----------------------------------------------------------------------------
# Add data to testdb schema
engine = create_engine('mysql://root:rootroot@localhost/testdb', echo=False)

df_actor_data.to_sql('actor', con=engine, index=False)
df_category_data.to_sql('category', con=engine, index=False)
df_city_data.to_sql('city', con=engine, index=False)
df_customer_data.to_sql('customer', con=engine, index=False)
df_film_data.to_sql('film', con=engine, index=False)
df_film_actors_data.to_sql('film_actors', con=engine, index=False)
df_film_text_data.to_sql('film_text', con=engine, index=False)
df_inventory_data.to_sql('inventory', con=engine, index=False)
df_language_data.to_sql('language', con=engine, index=False)
df_location_data.to_sql('location', con=engine, index=False)
df_rating_data.to_sql('mpa_rating', con=engine, index=False)
df_staff_data.to_sql('staff', con=engine, index=False)
df_state_data.to_sql('state', con=engine, index=False)
df_store_data.to_sql('store', con=engine, index=False)
df_transaction_data.to_sql('transactions', con=engine, index=False)

# -----------------------------------------------------------------------------
