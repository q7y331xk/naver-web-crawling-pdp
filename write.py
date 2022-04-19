from config import STARTS_AT, DAYS, NEW_TABLE, SILENCE
from scrapping import get_article_ids, get_pdp_dicts, set_cookies
from rds import write_db, conn_db, create_table_if_exists_drop
from push_periods import push_periods
from naver_login import naver_login

# change id and pw

def write(NEW_TABLE):
    periods = push_periods(starts_at = STARTS_AT, days = DAYS)
    period_max = periods[len(periods) - 1]
    print("crawling options")
    print(f"date from {periods[0]} to {period_max}")
    if NEW_TABLE:
        print('crawl into new table')
        create_table_if_exists_drop()
    else:
        print('crawl into exist table')
    if SILENCE:
        print('without opening browser')
    login = naver_login(SILENCE)
    driver = login['driver']
    cookies = login['cookies']
    req_session = set_cookies(cookies)
        
    for period in periods:
        article_ids = get_article_ids(period, req_session)
        pdp_dicts = get_pdp_dicts(driver, article_ids)
        write_db(pdp_dicts)
        print(f"{period}/{period_max}...")
    print("done")

write(NEW_TABLE)