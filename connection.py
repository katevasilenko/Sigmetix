import psycopg2


HOST = "localhost"
DBNAME = "madrid_airbnb_data_db"
USER = "postgres"
PASSWORD = "secretpass"
PORT = "5432"

try:
    conn = psycopg2.connect(database=DBNAME,
                            user=USER,
                            host=HOST,
                            password=PASSWORD,
                            port=PORT)
except (Exception, psycopg2.DatabaseError) as error_:
    print("Error while connection to PostgreSQL", error_)

cursor1 = conn.cursor()
cursor1.execute("drop table if exists listing;")
cursor1.execute("""
    CREATE TABLE listing(
        id integer PRIMARY KEY,
        name varchar,
        host_id integer,
        host_name varchar,
        neighbourhood_group varchar,
        neighbourhood varchar,
        latitude float,
        longitude float,
        room_type varchar,
        price integer,
        minimum_nights integer,
        number_of_reviews integer,
        last_review date,
        reviews_per_month float,
        calculated_host_listings_count integer,
        availability_365 integer
    )
""")
conn.commit()

cursor2 = conn.cursor()
cursor2.execute("drop table if exists review_detailed;")
cursor2.execute("""
    CREATE TABLE review_detailed(
        listing_id integer,
        id integer PRIMARY KEY,
        date date,
        reviewer_id integer,
        reviewer_name varchar,
        comments text
    )
""")

listing_file = open("listings.csv")
sql_statement = """
    COPY listing
    FROM STDIN WITH
    CSV
    HEADER
    DELIMITER AS ',';
"""

cursor1.copy_expert(sql=sql_statement, file=listing_file)

conn.commit()
cursor1.close()

reviews_detailed_file = open("reviews_detailed.csv")
sql_statement = """
    COPY review_detailed
    FROM STDIN WITH
    CSV
    HEADER
    DELIMITER AS ',';
"""

cursor2.copy_expert(sql=sql_statement, file=reviews_detailed_file)

conn.commit()
cursor2.close()


conn.close()
