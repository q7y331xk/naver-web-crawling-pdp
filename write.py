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

    if NEW_TABLE:
        create_table_if_exists_drop()

    period_max = periods[len(periods) - 1]
    for period in periods:
        article_ids = get_article_ids(period, period_max, req_session)
        pdp_dicts = get_pdp_dicts(driver, article_ids)
        write_db(pdp_dicts)
        print(f"{period}/{period_max} done")

write(NEW_TABLE)