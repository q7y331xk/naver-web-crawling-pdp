import pymysql
import copy
import re
from config import RDS_HOST, RDS_USER_NAME, RDS_USER_PW, RDS_DB, RDS_TABLE



def check_cost_significant(cost_text):
    significant = True
    cost_int = int(cost_text)
    if cost_text.find('123') > -1:
        significant = False
    if cost_text.replace(cost_text[0],'') == '':
        significant = False
    if cost_int < 10000:
        significant = False
    if cost_int > 9000000:
        significant = False
    return significant

def main_find_cost(main_text):
    found_cost = 0
    won= r"[0-9]+원"
    man= r"[0-9]+만"
    find_num_won = re.search(won, main_text)
    find_num_man = re.search(man, main_text)
    if find_num_won:
        found_cost = int(find_num_won.group().replace('원',''))
    if find_num_man:
        found_cost = int(find_num_man.group().replace('만','')) * 10000
    return found_cost

def covert_data(pdp_dict):
    pdp_converted = copy.deepcopy(pdp_dict)
    pdp_converted['condition'] = ''
    pdp_converted['pay_methods'] = ''
    pdp_converted['delivery'] = ''
    pdp_converted['location'] = ''
    cost_text = pdp_dict['cost'].replace(',','').replace('원','')
    views_text = pdp_dict['views'].replace(',','')
    likes_text = pdp_dict['likes'].replace(',','')
    comments_cnt_text = pdp_dict['comments_cnt'].replace(',','')
    cost_significant = check_cost_significant(cost_text)
    if cost_significant:
        pdp_converted['cost'] = int(cost_text)
    else:
        pdp_converted['cost'] = main_find_cost(pdp_dict['main'])
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
    for_sell = pdp_converted['title'].find('삽') > -1 | pdp_converted['main'].find('삽') > -1 | pdp_converted['title'].find('구매') > -1 
    if for_sell:
        pdp_converted['status'] = '구매'
    for_exchange = pdp_converted['title'].find('교환') > -1
    if for_exchange:
        pdp_converted['status'] = '교환'
    return pdp_converted

def conn_db():
    conn = pymysql.connect(host=RDS_HOST, user=RDS_USER_NAME, password=RDS_USER_PW, charset='utf8', port=3306, db=RDS_DB)
    return conn

def create_table_if_exists_drop():
    conn = conn_db()
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
    conn.commit()



def write_db(pdp_dicts):
    conn = conn_db()
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

def read_db():
    conn = pymysql.connect(host=RDS_HOST, user=RDS_USER_NAME, password=RDS_USER_PW, charset='utf8', port=3306, db=RDS_DB)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {RDS_TABLE}")
    sellings = cursor.fetchall()
    conn.commit()
    return sellings