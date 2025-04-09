import requests

# 测试api接口
# 常用requests请求方法
requests.get(url, params=None, **kwargs)
requests.post(url, data=None, json=None, **kwargs)
requests.put(url, data=None, **kwargs)
requests.delete(url, **kwargs)
requests.request(url, method, **kwargs)
requests.session()
