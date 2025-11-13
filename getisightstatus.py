from operator import truediv

import requests
def get_status(report,token, url):
    #url = "https://new-dev2-api-stat.smartanalytics.io/api/insight_log/?"

    headers = {
        "Authorization": "Token "+token,  # Если требуется токен
        "Content-Type": "application/json"
    }
    params = {
        "profile_id":"39"
    }

    while True:
        print("запрос статуса")
        try:
            response = requests.get(url, headers=headers, params=params, timeout=5)
            break
        except requests.exceptions.Timeout:
            print("Запрос завис, таймаут!")
        print("ПРобуем запрос еще раз")
    #response = requests.get(url, headers=headers, params=params)

    # Проверка статуса ответа
    print("Проверка статуса ответа")
    if response.status_code == 200:
        data = response.json()
        #print(f"результат: {response.json()}")
        #report_id = response.json()['report_id']

        target_report_id = report  # <-  сюда  report_id

        # Находим все status для этого report_id
        statuses = []
        for item in data:
            if item.get('report_id') == target_report_id:

                status = item.get('stage_name', '')
                statuses.append(status)
        k=0
        for item in statuses:
            if item == 'Кэширование запроса':

                k=k+1
        statuses2 = []
        for item in data:
            if item.get('report_id') == target_report_id:
                status2 = item.get('status', '')
                statuses2.append(status2)

        print(f"Statuses для report_id '{target_report_id}': {statuses2}")
        statuses3 = []
        for item in data:
            if item.get('report_id') == target_report_id:
                status3 = item.get('description', '')

                statuses3.append(status3)
                if status3=='Error':
                    return 'Error'

        print(f"description для report_id '{target_report_id}': {statuses3}")

        # Выводим результат
        if statuses:
            print(f"stage_name для report_id '{target_report_id}': {statuses}")
            # Или, если нужен только последний status (для текущей стадии):
            # print(f"Последний status: {statuses[-1]}")
            if k==2:
                print(f"кэширование завершено", k)
                return "True"
            else:
                print(f"кэширование НЕ завершено", k)
                return "False"

        else:
            print(f"Report_id '{target_report_id}' не найден в списке")
            return "False"

    else:
        print(f"Ошибка: {response.status_code}")
        print("Текст ошибки:", response.text)
