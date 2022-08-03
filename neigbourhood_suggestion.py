import psycopg2

from connection import connection_to_db

conn = connection_to_db()


def search_by_input(user_input):
    try:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT DISTINCT neighbourhood
            FROM listing
            WHERE neighbourhood LIKE %s || '%%';
            """, (user_input,))
            result = [r[0] for r in cur.fetchall()]
            if result:
                print(result)
            else:
                print("Invalid input")
    except (Exception, psycopg2.Error) as error:
        conn.rollback()
        print(error)


if __name__ == "__main__":
    search_by_input(input("Enter part of neighbourhood: "))
