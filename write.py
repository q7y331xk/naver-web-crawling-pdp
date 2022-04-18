from config import STARTS_AT, DAYS
from scrapping import get_article_ids, convert_soup_to_dict, get_pdp_dicts, set_cookies
from rds import write_db
from push_periods import push_periods
from naver_login import naver_login
from pdp import pdp

# change id and pw

def write():
    periods = push_periods(starts_at = STARTS_AT, days = DAYS)
    login = naver_login()
    driver = login['driver']
    cookies = login['cookies']
    req_session = set_cookies(cookies)
    article_ids = get_article_ids(periods, req_session)
    pdp_dicts =  get_pdp_dicts(driver, article_ids)
    write_db(pdp_dicts)

write()