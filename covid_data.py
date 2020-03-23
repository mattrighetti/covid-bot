import json
from requests import get
import threading, time
from datetime import datetime

region_data_url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json'
province_data_url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province-latest.json'
italy_data_url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale-latest.json'

def get_region_data():
    json_data = get(region_data_url)
    data = (json.loads(json_data.text))
    return data

def get_italy_data():
    json_data = get(italy_data_url)
    data = (json.loads(json_data.text))
    return data

def get_province_data():
    json_data = get(province_data_url)
    data = (json.loads(json_data.text))
    return data

def get_data():
    region_data_dict = {data['denominazione_regione'] : data for data in get_region_data()}
    province_data_dict = {data['denominazione_regione'] : data for data in get_province_data()}
    italy_data_dict = get_italy_data()
    
    return italy_data_dict[0], region_data_dict, province_data_dict