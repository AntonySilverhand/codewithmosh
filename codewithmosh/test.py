from PROXYPOOL import proxy_pool
import random


purl = "https://sky.moluo.ltd/api/v1/client/subscribe?token=4cb0b8d617014f9807398f61e6cc70ca"
proxies = proxy_pool().get_pool(purl)
# 获取字典的所有键值对
items = list(proxies.items())

# 从键值对中随机选择一个
random_key_value_pair = random.choice(items)

print(random_key_value_pair)
