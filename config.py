# OPTIONS
from datetime import datetime

STARTS_AT = datetime(2021,3,1)
DAYS = 31
NEW_TABLE = True
SILENCE = True
# 검색어는 korean euc-kr encode

# RDS
RDS_HOST = 'oden-second-hands-selling.ctj9mgachfi3.ap-northeast-2.rds.amazonaws.com'
RDS_USER_NAME = 'admin'
RDS_USER_PW = 'pLa5yfCbS^rCt^vh'
RDS_DB = 'chocam'
RDS_TABLE = 'recent_one_month'


# EXCEL
EXCEL_FILE_NAME = 'sellings'
EXCEL_SAVE_PATH = f"/Users/duckyounglee/Documents/{EXCEL_FILE_NAME}.xlsx"

# Naver Login
NAVER_ID = 'q7y331xk'
NAVER_PW = 'f7gh18Sh94#'