import pymongo
import psycopg2

mongo_client = pymongo.MongoClient("mongodb+srv://takixor119:z7ShIivdUIQH26kD@peoplecluster.ssjfkzz.mongodb.net/?retryWrites=true&w=majority&appName=PeopleCluster")
mongo_db = mongo_client["forpeople"]
mongo_quotes_collection = mongo_db["quote"]
mongo_authors_collection = mongo_db["author"]

pg_conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="789456",
    host="localhost",
    port='5432'
)
pg_cur = pg_conn.cursor()

author_map = {}

for mg_author in mongo_authors_collection.find():
    fullname = mg_author['fullname']
    born_time = mg_author.get('born_date', '')
    born_loc = mg_author.get('born_location', '')
    descr = mg_author.get('description', '')

    pg_cur.execute(
        "INSERT INTO quoteapp_author (fullname, born_date, born_location, description) VALUES (%s, %s, %s, %s) RETURNING id",
        (fullname, born_time, born_loc, descr))

    pg_conn.commit()
    author_id = pg_cur.fetchone()
    print(author_id)

    author_map[mg_author['_id']] = author_id


for mg_quote in mongo_quotes_collection.find():
    quote_text = mg_quote['quote']
    quote_author_id = author_map[mg_quote['author']]
    print(quote_author_id)
    tags = ', '.join(mg_quote['tags'])
    user_id = 2
    pg_cur.execute("SELECT * FROM quoteapp_quote WHERE author_id = %s", (quote_author_id,))
    existing_row = pg_cur.fetchone()
    if existing_row is None:
        pg_cur.execute("INSERT INTO quoteapp_quote (quote, author_id, tags, user_id) VALUES (%s, %s, %s, %s)",
                       (quote_text, quote_author_id, tags, user_id))
        pg_conn.commit()
    else:
        print(f"Author ID {quote_author_id} already exists in quoteapp_quote.")

    # pg_cur.execute("INSERT INTO quoteapp_quote (quote,author_id, tags, user_id) VALUES (%s, %s,%s, %s)",
    #                (quote_text,quote_author_id, tags, user_id))

    pg_conn.commit()


mongo_client.close()
pg_cur.close()
pg_conn.close()

print("Migration completed successfully!")