import asyncio
import json
import logging
import re
from datetime import datetime

import aiohttp
import requests

from config import headers, url_loves, payload_loves, proxies
from dao_mongo import DAOMongo
from proxy_service.proxy_manager import ScraperProxyManager

database_worker = DAOMongo()
successful_records = 0
proxy_manager = ScraperProxyManager()


async def get_all_stores_in_page(session, page_num):
    url = url_loves.format(page_num)
    proxy = proxy_manager.get_proxy_for_async_request()
    async with session.post(url, data=json.dumps(payload_loves),
                            proxy=proxy) as response:
        logging.warning(f'{response.status}, "page_loves"')
        stores_in_page = await response.json()
        await collect_info_store(stores_in_page)


async def collect_info_store(stores_in_page):
    for store in stores_in_page:
        global successful_records
        store_dict = {'name': store.get('SiteName'),
                      'phone': store.get('MainPhone'),
                      'state': store.get('State'),
                      'city': store.get('City'),
                      'address': store.get('Address'),
                      'diesel': []
                      }
        for fuel_type in store['FuelPrices']:
            if 'diesel' in fuel_type.get("DisplayName").lower():
                seconds_since_epoch_1 = re.search(r'\d{10}', fuel_type.get('LastPriceChangeDateTime')).group()
                seconds_since_epoch_2 = re.search(r'\d{10}', fuel_type.get('LastCheckInDateTime')).group()
                store_dict['diesel'].append({
                        "display_name": fuel_type.get('DisplayName'),
                        "product_name": fuel_type.get('ProductName'),
                        "fuel_type": fuel_type.get('FuelType'),
                        "cash_price": fuel_type.get('CashPrice'),
                        "credit_price": fuel_type.get('CreditPrice'),
                        "last_price_change_datetime": datetime.utcfromtimestamp(int(seconds_since_epoch_1)),
                        "last_check_in_datetime": datetime.utcfromtimestamp(int(seconds_since_epoch_2))
                    })
        database_worker.recording_data(store_dict, 'loves')
        successful_records += 1


async def main(quantity):
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for page_num in range(quantity):
            task = asyncio.create_task(get_all_stores_in_page(session, page_num))
            tasks.append(task)
        await asyncio.gather(*tasks)


def get_quantity_page():
    url = "https://www..com/api/StoreSearch/"
    response = requests.request("POST", url, headers=headers, data=payload_loves, proxies=proxies[1])
    quantity_stores = len(response.json()[0].get('Points'))
    return int(quantity_stores / 50) + 1, quantity_stores


def handler_loves():
    quantity_page, quantity_stores = get_quantity_page()
    logging.warning('get quantity_page loves...')
    asyncio.run(main(quantity=quantity_page))
    logging.warning(f"loves finished. All stores {quantity_stores}, successful_records {successful_records}")


if __name__ == '__main__':
    handler_loves()
