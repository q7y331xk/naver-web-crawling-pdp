from config import STARTS_AT, DAYS
from scrapping import search_each_period
from rds import write_db
from push_periods import push_periods
from get_naver_cookies import get_naver_cookies
from pdp import pdp

# change id and pw

periods = push_periods(starts_at = STARTS_AT, days = DAYS)
driver = get_naver_cookies()
# pdp = pdp(driver)


# sellings = search_each_period(periods, cookies)
# write_db(sellings)