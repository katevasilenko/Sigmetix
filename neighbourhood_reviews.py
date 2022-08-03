import psycopg2

from connection import connection_to_db

conn = connection_to_db()


def get_neighbourhood_reviews(neighbourhood_name):
    try:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT DISTINCT name
            FROM listing
            INNER JOIN review_detailed rd on listing.id = rd.listing_id
            WHERE neighbourhood = %s AND rd.comments IS NOT NULL;
            """, (neighbourhood_name,))
            result = [r[0] for r in cur.fetchall()]
            print({neighbourhood_name: result})
    except (Exception, psycopg2.Error) as error:
        conn.rollback()
        print(error)


if __name__ == "__main__":
    get_neighbourhood_reviews("Aeropuerto")

