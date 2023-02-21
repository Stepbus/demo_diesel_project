import random

import redis

from proxy_service.proxy_list import PROXY_LIST
REDIS_HOST = 'redis'
REDIS_PORT = 6379


class ProxyList:
    redis_set_name = 'PROXY_LIST'
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    @classmethod
    def proxy_list_exists(cls):
        if not cls.redis_client.smembers(cls.redis_set_name):
            return False
        else:
            return True

    @classmethod
    def add_proxy(cls, proxy):
        cls.redis_client.sadd(cls.redis_set_name, proxy)

    @classmethod
    def remove_proxy(cls, proxy):
        cls.redis_client.srem(cls.redis_set_name, proxy)

    @classmethod
    def get_all_proxies(cls):
        if not cls.proxy_list_exists():
            for proxy in PROXY_LIST:
                cls.add_proxy(proxy)
        return cls.redis_client.smembers(cls.redis_set_name)


class ScraperProxyManager:

    @property
    def available_proxies_list(self) -> set:
        return set([i.decode() for i in ProxyList.get_all_proxies()])

    def get_random_proxy_address(self) -> str:
        return random.choice(list(self.available_proxies_list))

    def get_proxy_for_sync_request(self) -> dict:
        proxy = self.get_random_proxy_address()
        self.__block_proxy(proxy)
        return {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}',
        }

    def get_proxy_for_async_request(self) -> str:
        proxy = self.get_random_proxy_address()
        self.__block_proxy(proxy)
        return f'http://{proxy}'

    def __block_proxy(self, proxy: str) -> None:
        ProxyList.remove_proxy(proxy)

    @staticmethod
    def _parse_proxy(proxy) -> str:
        if isinstance(proxy, dict):
            proxy_address = proxy['http'].split('://')[1]
        else:
            proxy_address = proxy.split('://')[1]
        return proxy_address

    def release_proxy(self, proxy) -> None:
        '''Adds proxy to the list of available proxies'''

        proxy_address = self._parse_proxy(proxy)

        if proxy_address not in self.available_proxies_list:
            ProxyList.add_proxy(proxy_address)
