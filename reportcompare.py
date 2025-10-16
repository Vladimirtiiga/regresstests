import os
import threading
import time
import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook
from string import ascii_letters, whitespace
from cromeget2 import getupdate
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from datetime import datetime, date, time as dt
import psutil

#manage_windows_proxy()
#getupdate()
def compare(urlopenget,urlopenget2):
    '''

    def get_current_time() -> datetime:
        delta = datetime.timedelta(hours=3, minutes=0)
        return datetime.now(datetime.timezone.utc) + delta
    '''
    disk = 'd'

    #urlopenget = 'https://dev2-cloud.smartanalytics.io/ru/#!/index/39/reports/14/18591'
    #urlopenget2 = 'https://dev2-cloud.smartanalytics.io/ru/#!/index/39/reports/14/18589'
    #prod = 'https://cloud.smartanalytics.io/new-vui-vux/#/ru/insights'


    good_chars = (ascii_letters + whitespace + '0123456798').encode()
    junk_chars = bytearray(set(range(0x100)) - set(good_chars))

    options = Options()
    options.add_argument("user-data-dir=" + disk + ":\\testinsigt\\test2")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)


    while True:
        time.sleep(1)
        try:
            print("пробуем загрузить первый отчет")
            driver.get(urlopenget)
            break
        except:
            time.sleep(1)
            print('пробую еще раз')
            continue
    time.sleep(15)

    try:
        print("пробуем открыть первый отчет")
        bodytable = driver.find_element(By.XPATH, '//tbody[@class="table-list__body"]')
    except:
        print("образец не открылся")
        return 0
    #print("первый отчет:")
    #print(bodytable.text)
    text1 = bodytable.text

    while True:
        time.sleep(1)
        try:
            print("пробуем загрузить второй отчет")
            driver.get(urlopenget2)
            break
        except:
            time.sleep(1)
            print('пробую еще раз')
            continue
    time.sleep(5)

    try:
        print("пробуем открыть второй отчет")
        bodytable2 = driver.find_element(By.XPATH, '//tbody[@class="table-list__body"]')
    except:
        print("тестируемый отчет не открылся")
        return 0
    text2 = bodytable2.text
    #print("второй отчет:")
    #print(bodytable2.text)
    text2 = bodytable2.text
    #if bodytable2==bodytable:
    #    print('отчеты совпадают')
    #else:
    #    print('отчеты не совпадают')



    # Разбиваем на строки и очищаем пустые
    lines1 = [line.strip() for line in text1.split('\n') if line.strip()]
    lines2 = [line.strip() for line in text2.split('\n') if line.strip()]

    # Общее количество строк (максимум из двух)
    total_lines = max(len(lines1), len(lines2))

    # Количество совпадающих строк по позиции
    matching_lines = sum(1 for i in range(min(len(lines1), len(lines2))) if lines1[i] == lines2[i])

    # Процент совпадения
    match_percentage = (matching_lines / total_lines) * 100 if total_lines > 0 else 0

    print(f"Процент совпадения: {match_percentage:.2f}%")
    print(f"Длина text1: {len(lines1)} строк, text2: {len(lines2)} строк")

    # Если разница небольшая (порог >95%, настройте под себя)
    if match_percentage > 95:
        print("Разница небольшая. Отличающиеся строки:")
        diff_lines = []
        for i in range(max(len(lines1), len(lines2))):
            if i < len(lines1) and i < len(lines2):
                if lines1[i] != lines2[i]:
                    diff_lines.append(f"Строка {i + 1}: text1='{lines1[i]}', text2='{lines2[i]}'")
            elif i < len(lines1):
                diff_lines.append(f"Строка {i + 1}: только в text1='{lines1[i]}'")
            else:
                diff_lines.append(f"Строка {i + 1}: только в text2='{lines2[i]}'")

        for diff in diff_lines:
            print(diff)
        return match_percentage
    else:
        print("Разница слишком большая (совпадение ",match_percentage,"%).")
        # Опционально: для детального diff
        #import difflib

        #diff = difflib.unified_diff(lines1, lines2, lineterm='')
        #print("\nПолный diff:")
        #for line in diff:
        #    print(line)
        return match_percentage