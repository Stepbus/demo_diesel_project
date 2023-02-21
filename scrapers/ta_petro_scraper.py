import logging
import re

import requests

from config import url_ta_petro_get_all, headers, proxies
from dao_mongo import DAOMongo


database_worker = DAOMongo()
successful_records = 0


def handler_ta_petro(successful):
    response = requests.request("POST", url_ta_petro_get_all, headers=headers, proxies=proxies[2])
    logging.warning(f'{response.status_code}, "page_ta_petro"')
    all_stores = response.json()
    quantity_stores = len(all_stores)
    for store in all_stores:
        store_dict = {'name': store.get('Name'),
                      'phone': store.get('Phone'),
                      'state': store.get('State'),
                      'city': store.get('City'),
                      'address': store.get('Street'),
                      'diesel': []}
        for fuel_type in store['FuelPrices']:
            if 'diesel' in fuel_type.get('Description').lower():
                price = re.search(r'\$(.+)', fuel_type.get('Price')).group(1)
                store_dict['diesel'].append({fuel_type.get('Description'): float(price)})
        database_worker.recording_data(store_dict, 'petro')
        successful += 1
    logging.warning(f"petro finished. All stores {quantity_stores}, successful_records {successful}")
