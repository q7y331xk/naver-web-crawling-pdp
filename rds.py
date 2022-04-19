import pymysql
from config import RDS_HOST, RDS_USER_NAME, RDS_USER_PW, RDS_DB, RDS_TABLE

def covert_data(pdp_dict):
    pdp_converted = pdp_dict
    pdp_converted['condition'] = ''
    pdp_converted['pay_methods'] = ''
    pdp_converted['delivery'] = ''
    pdp_converted['location'] = ''
    cost_text = pdp_dict['cost'].replace(',','').replace('원','')
    views_text = pdp_dict['views'].replace(',','')
    likes_text = pdp_dict['likes'].replace(',','')
    comments_cnt_text = pdp_dict['comments_cnt'].replace(',','')
    pdp_converted['cost'] = int(cost_text)
    pdp_converted['views'] = int(views_text)
    pdp_converted['likes'] = int(likes_text)
    pdp_converted['comments_cnt'] = int(comments_cnt_text)
    details = pdp_dict['details']
    for detail in details:
        for key, value in detail.items():
            if key == '상품 상태':
                pdp_converted['condition'] = value
            if key == '결제 방법':
                pdp_converted['pay_methods'] = value
            if key == '배송 방법':
                pdp_converted['delivery'] = value
            if key == '거래 지역':
                pdp_converted['location'] = value
    del(pdp_converted['details'])
    return pdp_converted

def conn_db():
    conn = pymysql.connect(host=RDS_HOST, user=RDS_USER_NAME, password=RDS_USER_PW, charset='utf8', port=3306, db=RDS_DB)
    return conn

def create_table_if_exists_drop(conn):
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {RDS_TABLE}")
    cursor.execute(f"CREATE TABLE {RDS_TABLE} (\
        id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        title TEXT,\
        cost INT,\
        nickname TEXT,\
        `status` TEXT,\
        `condition` TEXT,\
        pay_methods TEXT,\
        delivery TEXT,\
        location TEXT,\
        main TEXT,\
        views INT,\
        date TEXT,\
        likes TEXT,\
        comments_cnt INT,\
        comments TEXT\
    )")



def write_db(conn, pdp_dicts):
    cursor = conn.cursor()
    for pdp_dict in pdp_dicts:
        pdp_converted = covert_data(pdp_dict)
        cursor.execute(f"INSERT INTO {RDS_TABLE} VALUES(\
            \"{id}\",\
            \"{pdp_converted['title']}\",\
            \"{pdp_converted['cost']}\",\
            \"{pdp_converted['nickname']}\",\
            \"{pdp_converted['status']}\",\
            \"{pdp_converted['condition']}\",\
            \"{pdp_converted['pay_methods']}\",\
            \"{pdp_converted['delivery']}\",\
            \"{pdp_converted['location']}\",\
            \"{pdp_converted['main']}\",\
            \"{pdp_converted['views']}\",\
            \"{pdp_converted['date']}\",\
            \"{pdp_converted['likes']}\",\
            \"{pdp_converted['comments_cnt']}\",\
            \"{pdp_converted['comments']}\"\
        )")
    conn.commit()
    print("write db done")

def read_db():
    conn = pymysql.connect(host=RDS_HOST, user=RDS_USER_NAME, password=RDS_USER_PW, charset='utf8', port=3306, db=RDS_DB)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {RDS_TABLE}")
    sellings = cursor.fetchall()
    conn.commit()
    return sellings