import requests
from bs4 import BeautifulSoup
from time import sleep
from function_lib_3les import get_agent
import json
import csv

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "User-agent": get_agent()
}

coockie = {
    " Coockie": "INGRESSCOOKIE=1692189594.576.36.199859|c412cbc471bb20d180c4cb39c15e89b8"
}

# The following code is used once to get the required page addresses
"""
url_memb_list = []

for i in range(0, 744, 12):

    sleep(2)

    main_url = f"https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&offset={i}"

    response = requests.get(main_url, headers=headers, cookies=coockie)

    soup = BeautifulSoup(response.text, "lxml")

    data = soup.find_all("div", class_="col-xs-4 col-sm-3 col-md-2 bt-slide")

    for g in data:

        url = g.find("a").get("href")
        url_memb_list.append(url)
        namber = data.index(g) + i + 1
        print(f"Адрес c номером |{namber}| был успешно записан!\n")

    list_namber = i/12 + 1
    print(f"Лист под номером {int(list_namber)} успешно обработан.\n" + "_"*72)

"""
# with open("data/list_members.json", "w") as file:
#      json.dump(url_memb_list, file, indent=4, ensure_ascii=False)

with open("data/list_members.json", 'r', encoding="utf-8") as file:

    url_list = json.load(file)

for url in url_list:

    respons = requests.get(url, headers=headers, cookies=coockie)

    soup = BeautifulSoup(respons.text, "lxml")



