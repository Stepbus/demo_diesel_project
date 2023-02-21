proxies = [
    {'http': 'http://name:psw@11.111.11.11:20000',
     },
]

headers = {
    'ADRUM': 'isAjax:true',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Cookie': 'Cookie',
    'Origin': 'https://.com',
    'Referer': 'https://.com/store-locations',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
}

url_pilot = "https://.com//su/search"
url_pilot_fuel_price = "https://FfuelPrices"

url_ta_petro_get_all = "https://www.com/api/locations/get"

url_loves = "https://www.com/api/sitecore/"

payload_pilot = {
    "PageNumber": 0,
    "PageSize": 100,
    "States": [],
    "Countries": [],
    "Concepts": []
}

payload_loves = "{\"StoreTypes\":[],\"Amenities\":[],\"Restaurants\":[],\"FoodConcepts\":[],\"State\":\"All\"}"
