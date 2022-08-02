import psycopg2

from connection import connection_to_db

room_type_input = input("Enter room type you prefer: ")
price_input = int(input("Enter price expectation: "))
nights_input = int(input("Enter number of night: "))

conn = connection_to_db()


def search_by_input():
    try:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT neighbourhood
            FROM listing
            WHERE room_type = %s AND price = %s AND minimum_nights = %s;
            """, (room_type_input, price_input, nights_input))
            result = [r[0] for r in cur.fetchall()]
            print(result)
    except (Exception, psycopg2.Error) as error:
        conn.rollback()
        print(error)


print(search_by_input())
