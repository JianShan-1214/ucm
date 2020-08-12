import requests
import secrets
from bs4 import BeautifulSoup


#先撈全校有哪些系跟他們的代碼
department_res = requests.get(secrets.url_department)
department_res.encoding = 'big5-hkscs'
department_soup = BeautifulSoup(department_res.text, 'html.parser')

department_name =[] #系所名稱
department_code =[] #系所代碼

for name in department_soup.find_all('td',align="left"):
     department_name = department_name + [name.font.string.rstrip()]

for num in department_soup.find_all('td',align="center"):
    if num.font != None:
        department_code = department_code + [num.font.a.string.rstrip()]
        
department_dic = dict(zip(department_name,department_code))



#用系所代碼求所有班級代號
def search_department_all_class(department_name):   

    all_class_url = secrets.url_class_code +department_dic[department_name]+'&tdena=%B8%EA%B0T%A4u%B5{%BE%C7%A8t'

    res = requests.get(all_class_url)
    res.encoding = 'big5-hkscs'
    soup = BeautifulSoup(res.text, 'html.parser')


    department_class = [] #系所班級

    for num in soup.find_all('td'):
        str = num.text.rstrip()
        str = ''.join(str.split()) #移除中間空白
        department_class = department_class + [str]

    return department_class


def generate_all_class():
    dic = []
    for department_name,department_code in department_dic.items():
        for classcode in search_department_all_class(department_name):
            if(len(classcode) > 5): 
                dic += [classcode[0:5]]
    return dic

