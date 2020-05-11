# -*- coding: UTF-8 -*-

import urllib.request
import FlvParser
filePath = 'D:\\tmp-data\\orign\\temp.flv'
token1 = ''
token2 = ''
url1 = 'http://127.0.0.1:8000/live?port=1935&app=flv_live&stream=fly'
url3 = 'http://192.168.203.132:8083/live/live_33948091_1.flv?token=eyJrZXkiOjEwNCwic2lnbiI6ImhhdFhwVHh0UjI5eXV5NWpuNnBoaGJueVB1NVVzX09udXNoaTFmM2xma3lWaUFNNGgzb0VjN1FYZm1DYlN0YmgwcE5YOHBzcEozNnhOWmgzWU1BX21SWXhKSWhQbWpsdEdEZG1NdUNRRXIwVGNMeEtROE1JcjhsczdkQzVfQV9abXRQMkY1Z3ZiYklFX1ZhaWxxZExWOTRWbmRIMWtrN1NjSFQ2aFJpd0o4dyJ9'
url2 = 'http://111.45.122.1:8700/live/live_10_5.flv'
url2 += '?token=eyJrZXkiOjEsInNpZ24iOiItcTVkQWZfeW04RkNrNjJtajBEcjZXMko5UGl6ekVWanlYOEZ3Wnc4bFV1OVdUMUFneXVnZEFFYTRkTVd3cklRdVdueW04Y0pGbXJqVEExR3FaTVFkU3phSjRiR3FmQ242RkFkQXBwemVuNWJBUUxXZXE2RldxNTZhNURwYUFGTWN1ZmNOT3Z2RDJuWUFBQU4zZjBVOUEifQ'
# request = urllib.request.Request("")
# request.add_header("api-key", "")
size = 1024 * 4
data = {"token": "eyJrZXkiOjEsInNpZ24iOiJsRkNraXVNbkJTdHRDbVRoTXlWRW11dG9TN1pheDhYenJQVkRPemNjck5xTEdlQmlDV3lFelVZNl8yelF3TDliVEZ2YUpFbjVUaUQ3Rjh3TUhrb2RfdjN5bTdUQTlSVWNGWmdoTks5aXFXUmlmQkVNdG9OX2lnand4eUlRb25TbFBJSGh3Um14bUNzU2lmNkpaNXhfZFEifQ"}
resp = urllib.request.urlopen(url3)
file = open(filePath, 'wb')
parser = FlvParser.FlvParse()
for num in range(1, 100):
    data = resp.read(size)
    parser.parse(data)
    file.write(data)
resp.close()
file.close()
print('Down')
