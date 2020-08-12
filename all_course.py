import requests
from bs4 import BeautifulSoup
import urllib3
import csv
import secrets
import os
from school_code import department_code
import organize_course

def General_Education(campus):

    urllib3.disable_warnings()
    url = secrets.url_course + 'query_4_1.asp'
    r = requests.get(url,data={"sch":campus},timeout=30,verify=False)
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

    for i in output_rows:
        print (i)

    # if not os.path.exists("General_Education"):
    #     os.mkdir("General_Education")
    # with open('General_Education/'+ str(campus)+'.csv', 'w+', encoding='utf-8') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerows(output_rows)



def Elective(dept,yr):
    
    urllib3.disable_warnings()
    url = secrets.url_course + "query_3_1.asp"
    r = requests.get(url,data={"dept":dept,"yr":yr},timeout=30,verify=False)
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
    if not os.path.exists("Elective"):
        os.mkdir("Elective")
        
    if not os.path.exists("Elective/"+str(dept)):
        os.mkdir("Elective/"+str(dept))
    
    with open('Elective/'+str(dept)+'/'+str(yr)+'.csv', 'w+', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)
    organize_course.organize_course('Elective/'+str(dept)+'/'+str(yr)+'.csv')






def generate_all_Elective():
    for code in department_code:
        for yr in range(1,6):
            # print (str(code) + ' ' + str(yr))
            try:
                Elective(str(code),str(yr))
            except:
                print(str(code)+' '+str(yr)+' err')


def generate_all_General_Education():
    for campus in range(1,4):
        General_Education(campus)


generate_all_Elective()


