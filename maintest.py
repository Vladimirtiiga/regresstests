from openpyxl import load_workbook
from startgen import test_get_request
from getisightstatus import get_status
import time
import os
token = os.getenv('tokendev')



params = {"method":"Искать проблемные зоны","top_dimensions_number":10,"max_depth":4,"metric":"conversion_rate","set_name":"Веб-аналитика 📈","time_case":{"TMPM":"Этот месяц VS предыдущий"},"how_start":"В реальном времени","run_tests":False}
#print(params)


url = "https://dev2-api.smartanalytics.io/api/insights/1603/start/"


report_id = test_get_request(url, params, token)
print(report_id)

time.sleep(5)
while get_status(str(report_id), token)==False:
    time.sleep(5)





