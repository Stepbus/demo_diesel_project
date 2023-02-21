import asyncio
import json
import logging

import aiohttp
import requests

from config import url_pilot, headers, payload_pilot, proxies, url_pilot_fuel_price
from dao_mongo import DAOMongo
from proxy_service.proxy_manager import ScraperProxyManager

database_worker = DAOMongo()
successful_records = 0
proxy_manager = ScraperProxyManager()


async def get_all_stores_in_page(session, page_num):
    payload_pilot['PageNumber'] = page_num
    proxy = proxy_manager.get_proxy_for_async_request()
    async with session.post(url_pilot, data=json.dumps(payload_pilot),
                            proxy=proxy) as response:
        logging.warning(f'{response.status}, "page_pilot"')
        stores_in_page = await response.json()
        await collect_info_store(session, stores_in_page)


async def get_fuel_info(session, store):
    id_ = store.get('name')
    url = url_pilot_fuel_price.format(id_)
    for attempt in range(3):
        global successful_records
        proxy = proxy_manager.get_proxy_for_async_request()
        async with session.get(url, proxy=proxy) as response:
            if response.status != 200:
                logging.warning(f"{response.status}, {store}")
                await asyncio.sleep(3)
                continue
            else:
                fuel = await response.json()
                if fuel:
                    for fuel_type in fuel:
                        if 'diesel' in fuel_type.get('description').lower():
                            store["diesel"].append({fuel_type.get('description'): fuel_type.get('price')})
                else:
                    store["diesel"].append({})
                database_worker.recording_data(store, 'pilot')
                successful_records += 1
                return
    logging.error(f"ERROR! {store}")


async def collect_info_store(session, stores_in_page):
    tasks = []
    for store in stores_in_page.get('Locations'):
        store_dict = {'name': store.get('Id'),
                      'store_name': store.get('StoreName'),
                      'phone': store.get('PhoneNumber'),
                      'state': store.get('State'),
                      'city': store.get('City'),
                      'address': store.get('StreetAddress'),
                      'diesel': []
                      }
        task = asyncio.create_task(get_fuel_info(session, store_dict))
        tasks.append(task)
    await asyncio.gather(*tasks)


async def main(quantity):
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for page_num in range(1, quantity):
            task = asyncio.create_task(get_all_stores_in_page(session, page_num))
            tasks.append(task)
        await asyncio.gather(*tasks)


def get_quantity_page():
    url = "https://com/umbraco/surface/storelocations"
    payload = payload_pilot
    payload["PageNumber"] = 1
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload), proxies=proxies[1])
    quantity_stores = response.json().get('TotalItems')
    return response.json().get('TotalPages') + 1, quantity_stores


def handler_pilot():
    quantity_page, quantity_stores = get_quantity_page()
    logging.warning('get quantity_page pilot...')
    asyncio.run(main(quantity=quantity_page))
    logging.warning(f"pilot finished. All stores {quantity_stores}, successful_records {successful_records}")
