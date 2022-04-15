from rds import read_db
from excel import write_excel

sellings = read_db()
write_excel(sellings)