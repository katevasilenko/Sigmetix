import psycopg2


DB_HOST = "localhost"
DB_NAME = "madrid_airbnb_data_db"
DB_USER = "postgres"
DB_PASSWORD = "secretpass"
PORT = "5432"


def connection_to_db():
    conn = None
    try:
        conn = psycopg2.connect(host=DB_HOST,
                                database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASSWORD,
                                port=PORT)
        print("Success connection!")
    except (Exception, psycopg2.DatabaseError) as error_:
        print("Error while connection to PostgreSQL", error_)
    return conn


def main(conn):
    cursor1 = conn.cursor()
    cursor1.execute("drop table if exists listing cascade;")
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
    print("Listing table created!")

    cursor2 = conn.cursor()
    cursor2.execute("drop table if exists review_detailed cascade;")
    cursor2.execute("""
        CREATE TABLE review_detailed(
            listing_id integer REFERENCES listing (id),
            id integer PRIMARY KEY,
            date date,
            reviewer_id integer,
            reviewer_name varchar,
            comments text
        )
    """)
    conn.commit()
    print("Review detailed table created!")

    listing_file = open("csv_files/listings.csv")
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
    print("Listing table filled!")

    reviews_detailed_file = open("csv_files/reviews_detailed.csv")
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
    print("Review detailed table filled!")

    conn.close()
    print("Connection closed!")


if __name__ == "__main__":
    main(connection_to_db())
