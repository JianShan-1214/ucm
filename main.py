import requests
from bs4 import BeautifulSoup
import urllib3
import csv
from secrets import url_class_curriculum

class_code = '16101'

urllib3.disable_warnings()
url = url_class_curriculum + class_code
r = requests.get(url,timeout=30,verify=False)
r.encoding='big5'
r.text
soup = BeautifulSoup(r.text, 'html5lib')
table = soup.find("table")

output_rows = []
for table_row in table.findAll('tr'):
    columns = table_row.findAll('td')
    
    output_row = []
    for column in columns:
        output_row.append(column.text)
    output_rows.append(output_row)

with open('output.csv', 'w+', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_rows)