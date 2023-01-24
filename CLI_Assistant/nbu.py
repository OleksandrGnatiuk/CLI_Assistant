import json
from datetime import datetime
from urllib import request


def get_currency(currencyname):
    today = datetime.now().strftime("%Y%m%d")
    URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=' + currencyname + '&date=' + today + '&json'
    content = request.urlopen(URL)
    rate = json.load(content)[0]['rate']
    return f"\n{str(datetime.now().date())}  {currencyname}: {rate}\n"

