import json

jsonData = r'{"name": "jie", "desc": "你好\n杰哥"}'
data = json.loads(jsonData)
print(data["desc"])
