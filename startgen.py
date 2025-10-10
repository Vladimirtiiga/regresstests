import requests
from datetime import datetime, timedelta
import os
def test_get_request(url,params, token):
    #token = os.getenv('tokendev')
    #url = "https://dev2-api.smartanalytics.io/api/insights/1471/start/"

    headers = {
        #"Authorization": "Token "+token,  # Если требуется токен
        "Authorization": "Token "+token,  # Если требуется токен
        "Content-Type": "application/json"
    }


    response = requests.post(url, headers=headers, json=params)

    # Проверка статуса ответа
    if response.status_code == 202:

        print(f"результат: {response.json()}")
        report_id = response.json()['report_id']
        print(f"Report ID: {report_id}")
        return report_id

    else:
        print(f"Ошибка: {response.status_code}")
        print("Текст ошибки:", response.text)
        return response.text



#test_get_request()
