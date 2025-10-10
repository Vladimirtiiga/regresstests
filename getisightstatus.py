from operator import truediv

import requests
def get_status(report,token):
    url = "https://new-dev2-api-stat.smartanalytics.io/api/insight_log/?"
    #url = "http://dev2-api.smartanalytics.io/api/insights/get_time_cases_by_date/"
    headers = {
        "Authorization": "Token "+token,  # Если требуется токен
        "Content-Type": "application/json"
    }
    params = {
        "profile_id":"39"
    }

    response = requests.get(url, headers=headers, params=params)

    # Проверка статуса ответа
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

        # Выводим результат
        if statuses:
            print(f"Statuses для report_id '{target_report_id}': {statuses}")
            # Или, если нужен только последний status (для текущей стадии):
            # print(f"Последний status: {statuses[-1]}")
            if k==2:
                print(f"кэширование завершено", k)
                return True
            else:
                print(f"кэширование НЕ завершено", k)
                return False

        else:
            print(f"Report_id '{target_report_id}' не найден в списке")
            return False

    else:
        print(f"Ошибка: {response.status_code}")
        print("Текст ошибки:", response.text)
