import selenium
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from ics import Calendar, Event
from datetime import datetime, timedelta

from getpass import getpass

meneshu_nosaukumi = {
    "janvāris": "01",
    "februāris": "02",
    "marts": "03",
    "aprīlis": "04",
    "maijs": "05",
    "jūnijs": "06",
    "jūlijs": "07",
    "augusts": "08",
    "septembris": "09",
    "oktobris": "10",
    "novembris": "11",
    "decembris": "12"
}

password = getpass("Ievadi e-studiju vides paroli: ")

service = Service()
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=option)
wait = WebDriverWait(driver, 10)

# ielogojos estudijas.rtu sistēmā

url = "https://estudijas.rtu.lv"
driver.get(url)
wait.until(EC.presence_of_element_located((By.ID, "submit")))
find = driver.find_element(By.ID, "submit")
find.click()
time.sleep(1)

find = driver.find_element(By.ID, "IDToken1")
find.send_keys("daniels.sabanskis")

find = driver.find_element(By.ID, "IDToken2")
find.send_keys(password)
find.send_keys(Keys.RETURN)

# Iegūstu tuvojošos notikumu sarakstu
time.sleep(1)
assignment_blocks = driver.find_elements(By.CLASS_NAME, "event")
assignments = []

for i in range(len(assignment_blocks)):
    try:
        assignment_blocks = driver.find_elements(By.CSS_SELECTOR, 'a[data-type="event"]')
        # Atveru katru notikumu no saraksta ar .click(), lai varētu apskatīt katra notikuma detalizētu informāciju
        assignment_blocks[i].click()

        # atveras notikuma logs
        modal_title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-title")))

        # saglabāju notikuma nosaukumu mainīgajā title
        title_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h5.modal-title')))
        title = title_elem.text

        # mainu fokusu uz notikuma loga saturu, kurā atrodas datums un kursa nosaukums
        modal_body = driver.find_element(By.CSS_SELECTOR, 'div.modal-body')
        time.sleep(0.2)
        # iegūstu datus no notikuma loga satura
        date = modal_body.find_element(By.XPATH,'(//div[contains(@class, "col-11")])[1]').text
        time.sleep(0.2)
        course_name = modal_body.find_element(By.XPATH, '(//div[contains(@class, "col-11")])[last()]').text

        # pārveidoju datumu .ics kalendāram saprotamā formātā no latviešu valodas uz ciparu formātu
        parts = date.split(", ")
        day = parts[1].split(".")[0].strip()
        month = parts[1].split(".")[1].strip()
        month = meneshu_nosaukumi[month]
        daytime = parts[2]
        year = datetime.now().year
        dt = datetime.strptime(f"{year}-{month}-{day} {daytime}", "%Y-%m-%d %H:%M")
        dt = dt.strftime("%Y-%m-%d %H:%M")


        # Iegūstu linku uz notikumu
        activity_link = driver.find_element(By.CSS_SELECTOR, 'div.modal-footer a')
        link_href = activity_link.get_attribute("href")

        assignments.append({
            "Title": title,
            "Course": course_name,
            "due": dt,
            "link": link_href,
        })

        # Aizveru logu, lai varētu nākamajā for cikla iterācijā atvērt nākamo logu
        close_button = driver.find_element(By.CSS_SELECTOR, 'button[data-action="hide"]')
        close_button.click()
        time.sleep(0.5)
    except Exception as e:
        print("error", e)
        driver.quit()

for i in range(len(assignments)):
    print(assignments[i]["Title"])
    print(assignments[i]["Course"])
    print(assignments[i]["due"])
    print(assignments[i]["link"])
    print("-" * 60)

calendar = Calendar()

for i in range(len(assignments)):
    event = Event()
    event.name = assignments[i]["Title"]
    event.description = assignments[i]["Course"]
    dt = datetime.strptime(assignments[i]["due"], "%Y-%m-%d %H:%M")
    event.begin = dt
    event.end = dt + timedelta(hours=2)
    event.url = assignments[i]["link"]
    calendar.events.add(event)

with open('assignments.ics', 'w') as f:
    f.writelines(calendar)

print("SUCCESS!! iCalendar .ics fails izveidots. Nospied ENTER, lai aizvērtu programmu.")

input()
