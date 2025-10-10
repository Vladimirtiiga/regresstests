import requests
from datetime import datetime, timedelta
import os
def test_get_request():
    token = os.getenv('tokendev')
    url = "https://dev2-api.smartanalytics.io/api/insights/1603/start/"

    headers = {

        "Authorization": "Token "+token,  #
        "Content-Type": "application/json"
    }
    params = {"method": "Искать проблемные зоны", "top_dimensions_number": 10, "max_depth": 4,
              "metric": "conversion_rate", "set_name": "Веб-аналитика 📈",
              "time_case": {"TMPM": "Этот месяц VS предыдущий"}, "how_start": "В реальном времени", "run_tests": False}
    # print(params)

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
        return 'response.text'



test_get_request()
