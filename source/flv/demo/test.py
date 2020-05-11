import json
import urllib.request
import urllib.parse

jsonData = r'{"name": "jie", "desc": "你好\n杰哥"}'
data = json.loads(jsonData)
print(data["desc"])
print(urllib.parse.quote("33013046_1-1573489763713.ts"))
resp = urllib.request.urlopen("http://172.19.3.59:8302/33013046_1-1573489763713.ts")
print(resp)