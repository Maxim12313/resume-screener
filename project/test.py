import psycopg
from config import Shared, db_name, db_user, db_password, db_host, db_port 

with psycopg.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
) as conn:
    with conn.cursor() as cur:
        cur.execute("")


