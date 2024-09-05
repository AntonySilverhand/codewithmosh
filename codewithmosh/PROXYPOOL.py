import requests
import base64
import re
from faker import Faker


"""
https://sky.moluo.ltd/api/v1/client/subscribe?token=4cb0b8d617014f9807398f61e6cc70ca
"""

class proxy_pool:
    def __init__(self):

        header = Faker().user_agent()
        self.headers = {
            "User-Agent": header
        }

        self.proxies = {}

    def get_proxy(self, url):

        response = requests.get(url, headers=self.headers)
        return response.text

    def parse(self, param):

        lines = base64.b64decode(param).decode('utf-8').strip().split('\n')[3:]
        pattern = re.compile(r'ss.*?@(.*?:\d+)#')
        i = 0
        for line in lines:
            self.proxies[pattern.search(line).group(1)] = 100

        return self.proxies





    def get_pool(self, url):
        text = self.get_proxy(url)
        result = self.parse(text)
        return result



# pp = proxy_pool()
# pp.get_pool('https://sky.moluo.ltd/api/v1/client/subscribe?token=4cb0b8d617014f9807398f61e6cc70ca')
# print(pp.proxies)
