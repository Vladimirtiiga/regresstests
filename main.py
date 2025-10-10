from openpyxl import load_workbook
from startgen import test_get_request
from getisightstatus import get_status
from reportcompare import*
import time
import os
import json  # Для парсинга вложенных фрагментов, если нужно
from cromeget2 import getupdate
getupdate()
token = os.getenv('tokendev')


# Открываем файл
wb = load_workbook(filename='autoregress.xlsx', data_only=True)
ws = wb.active  # Предполагаем, что данные на активном листе

# Получаем количество строк
N = ws.max_row

# Столбцы от B до I
columns = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

# Цикл по строкам 2 до N — для каждой строки создаем отдельный payload и отправляем запрос
for i in range(2, N + 1):
    row_dict = {}  # Отдельный dict для текущей строки
    for col in columns:
        # Читаем значения как текст
        val1 = ws[col + '1'].value or ''  # Ключ из header (row 1)
        vali = ws[col + str(i)].value or ''  # Значение из текущей строки

        # Парсим ключ: убираем двоеточие, кавычки и пробелы
        key_str = str(val1).strip().rstrip(':').strip().strip('"\'')  # Пример: '"method": ' -> 'method'
        if not key_str:  # Пропускаем пустые ключи
            continue

        # Значение: оставляем как есть, но можно привести тип
        value_str = str(vali).strip().strip('"\'')  # Убираем внешние кавычки, если они есть

        # Пытаемся определить тип значения (для чисел, булевых)
        try:
            if value_str.lower() in ('true', 'false'):
                value = value_str.lower() == 'true'
            elif value_str.isdigit() or (value_str.startswith('-') and value_str[1:].isdigit()):
                value = int(value_str)
            elif '.' in value_str and value_str.replace('.', '').replace('-', '').isdigit():
                value = float(value_str)
            else:
                # Для строковых значений сначала пробуем парсинг JSON (массивы или объекты)
                if ('{' in value_str or '[' in value_str) and ('}' in value_str or ']' in value_str):
                    try:
                        # Пробуем парсить как JSON напрямую
                        value = json.loads(value_str)
                    except json.JSONDecodeError:
                        # Если не парсится, оставляем строкой
                        value = value_str
                else:
                    value = value_str  # Строка по умолчанию
        except ValueError:
            value = value_str

        # Добавляем в dict для текущей строки
        row_dict[key_str] = value

    # Теперь row_dict — это payload для текущей строки (НЕ update, а отдельно!)
    payload = row_dict

    # Выводим для отладки (теперь каждый раз свой, если данные отличаются)
    #print(f"Payload для строки {i}: {payload}")

    print(payload)

    #print(params)

    valiurl = ws['A' + str(i)].value or ''  # Если None, используем пустую строку
    urlstart = 'https://dev2-api.smartanalytics.io/api/insights/' +str(valiurl) + '/start/'   # Соединяем текст без пробела
    print(urlstart)
    report_id = test_get_request(urlstart, payload, token)
    print(report_id)
    ws['K' + str(i)].value = "https://dev2-cloud.smartanalytics.io/ru/#!/index/39/reports/14/"+str(report_id)
    time.sleep(5)
    while get_status(str(report_id), token)==False:
        time.sleep(5)
    comparestatus = compare(ws['J' + str(i)].value, ws['K' + str(i)].value)
    ws['L' + str(i)].value = "совпадение "+str(comparestatus)+"%)."





wb.save('output.xlsx')