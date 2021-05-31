from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time
import re

category = "nations"
fname = f"{category}_word.txt"
f = open(f"C:/Users/ronal/PycharmProjects/definition/nlp/nlp_project_liars_game/{fname}", "r")

driver = webdriver.Chrome(executable_path="C:/Users/ronal/Downloads/chromedriver_win32/chromedriver.exe")
result = dict()

f.readline()
for line in f:
    word = line.strip()
    url = f"https://en.dict.naver.com/#/search?range=english&query={word}"
    driver.get(url)

    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    a = soup.find_all("li", class_="mean_item")[0].find_all("m")

    if len(a) == 0:
        a = soup.find_all("li", class_="mean_item")[0].find_all("p")

    if len(a) == 0:
        print(word)

    txt = ' '.join(sent.text for sent in a)
    result[word] = txt.strip()

data = result

for key in data.keys():
    temp = re.search(r'[a-zA-Z]', data[key], re.I)
    data[key] = data[key][temp.start():]

f = open("nations_definitions.json", "w")
json.dump(data, f, sort_keys=True, indent=4)
