from config import STARTS_AT, DAYS, NEW_TABLE
from scrapping import get_article_ids, get_pdp_dicts, set_cookies
from rds import write_db, conn_db, create_table_if_exists_drop
from push_periods import push_periods
from naver_login import naver_login

# change id and pw

def write(NEW_TABLE):
    periods = push_periods(starts_at = STARTS_AT, days = DAYS)
    login = naver_login()
    driver = login['driver']
    cookies = login['cookies']
    req_session = set_cookies(cookies)
    article_ids = get_article_ids(periods, req_session)
    pdp_dicts = get_pdp_dicts(driver, article_ids)
    conn = conn_db()
    if NEW_TABLE:
        create_table_if_exists_drop(conn)
    write_db(conn, pdp_dicts)

write(NEW_TABLE)