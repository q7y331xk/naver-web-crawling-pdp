import pymysql
from config import RDS_HOST, RDS_USER_NAME, RDS_USER_PW, RDS_DB, RDS_TABLE

def write_db(sellings):
    print("write db...")
    conn = pymysql.connect(host=RDS_HOST, user=RDS_USER_NAME, password=RDS_USER_PW, charset='utf8', port=3306, db=RDS_DB)
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {RDS_TABLE}")
    cursor.execute(f"CREATE TABLE {RDS_TABLE} (\
        id int,\
        title text,\
        status text,\
        views text,\
        likes text,\
        comments text,\
        name text,\
        date text\
    )")
    for selling in sellings:
        cursor.execute(f"INSERT INTO {RDS_TABLE} VALUES({selling['id']},\"{selling['title']}\",\"{selling['status']}\",\"{selling['views']}\",\"{selling['likes']}\",\"{selling['comments']}\",\"{selling['name']}\",\"{selling['date']}\")")
    conn.commit()
    print("write db done")

def read_db():
    conn = pymysql.connect(host=RDS_HOST, user=RDS_USER_NAME, password=RDS_USER_PW, charset='utf8', port=3306, db=RDS_DB)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {RDS_TABLE}")
    sellings = cursor.fetchall()
    conn.commit()
    return sellings