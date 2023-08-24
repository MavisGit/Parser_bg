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

cookie = {
    " Cookie": "INGRESSCOOKIE=1692189594.576.36.199859|c412cbc471bb20d180c4cb39c15e89b8"
}

# Function for obtaining a .json file with url-addresses (use once). 
def get_url_list():
    url_memb_list = []

    for i in range(0, 744, 12):

        sleep(2)

        main_url = f"https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&offset={i}"

        response = requests.get(main_url, headers=headers, cookies=cookie)

        soup = BeautifulSoup(response.text, "lxml")

        data = soup.find_all("div", class_="col-xs-4 col-sm-3 col-md-2 bt-slide")

        for g in data:

            url = g.find("a").get("href")
            url_memb_list.append(url)
            namber = data.index(g) + i + 1
            print(f"Адрес c номером |{namber}| был успешно записан!\n")

        list_namber = i/12 + 1
        print(f"Лист под номером {int(list_namber)} успешно обработан.\n" + "_"*72)

    with open("data/list_members.json", "w") as f:
        json.dump(url_memb_list, f, indent=4, ensure_ascii=False)


with open("data/list_members.json", 'r', encoding="utf-8") as file:
    url_list = json.load(file)

clear_create = False
if clear_create == True:
    with open("data/members.csv", mode="w", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow([
            "Имя",
            "Партия",
            "Должность",
            "Профили в интернете",
            ])

count = 0
no_contact = 0
for url in url_list:
    member_info = {}
    contact_list = []
    # With love for the site :)
    sleep(3)

    respons = requests.get(url, headers=headers, cookies=cookie)

    soup = BeautifulSoup(respons.text, "lxml")

    data = soup.find("div", class_="col-xs-8 col-md-9 bt-biografie-name")

    name_consign = data.find("h3").text.split(",")

    member_info["Name"] = name_consign[0].strip()
    member_info["Consign"] = name_consign[1].strip()
    member_info["Position"] = data.find("div", class_="bt-biografie-beruf").text.strip()

    data_info = soup.find("div", class_="bt-standard-content bt-profil-kontakt collapse col-xs-12 col-sm-8 col-md-9")

    data_contact = data_info.find("ul", class_="bt-linkliste")
    if data_contact is None:
        contact_list.append("None")
        member_info["Platform"] = "None"
        print(f"У {member_info['Name']} нет контактов")
        no_contact += 1

    else:
        list_contact = data_contact.find_all("a", class_="bt-link-extern")

        for contact in list_contact:
            platform_name = contact.get("title")
            contact_url = contact.get("href")
            # Sorry Ilon Musk, not today ;)
            if platform_name == "X":
                platform_name = "Twitter"

            member_info[platform_name] = contact_url
            contact_list.append(f"{platform_name} : {contact_url} \n")

    # Adjust the name for the file
    name = member_info["Name"].replace(" ", "_")

    with open(f"data/person_cards/{name}.json", mode="w", encoding="utf-8") as file:
        json.dump(member_info, file, indent=4, ensure_ascii=False)

    print("Индивидуальная карта создана")
    contacr_str = "".join(contact_list)

    with open("data/members.csv", mode="a", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow([
            member_info["Name"],
            member_info["Consign"],
            member_info["Position"],
            contacr_str,
        ])
    count += 1

    print(f"Таблица была обновлена. \nВсего членов парламента занесено: {count}.\nОсталось: {len(url_list)-count}")
    print("-"*72)
    if count == len(url_list):
        print("Конец записи")
        print(f"Членов парламента без контактов {no_contact}")
