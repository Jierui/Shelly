# -*- coding: UTF-8 -*-

import urllib.request
filePath = 'D:\\tmp-data\\orign\\plat_c.flv'
token1 = ''
token2 = ''
url1 = 'http://192.168.200.214/live?port=1935&app=hls&stream=fly'
url2 = 'http://192.168.200.214:8083/live/live_25096185_1.flv'
url2 += '?token=eyJrZXkiOjEsInNpZ24iOiJsTzVhOUswZ3hQR3JqLWZUaEkyVjJrSXRxWnM5TVhpSzdfMk1pWTVaU0VDSmtTcDlncWtZT1dkZEl2YWhNd0lzVHlJcTVTWXdmZUN4dTNaYTFEUnVNM2lNR1VFaVNQbFFTZFExUjNHWXRwQmExbTZ3TF9oOXVHZlNjazdkMDRfeGx1ZFdVSUt3MHFyMG9IZFFSQ2tNM0EifQ'
# request = urllib.request.Request("")
# request.add_header("api-key", "")
size = 1024 * 1024
data = {"token": "eyJrZXkiOjEsInNpZ24iOiJsRkNraXVNbkJTdHRDbVRoTXlWRW11dG9TN1pheDhYenJQVkRPemNjck5xTEdlQmlDV3lFelVZNl8yelF3TDliVEZ2YUpFbjVUaUQ3Rjh3TUhrb2RfdjN5bTdUQTlSVWNGWmdoTks5aXFXUmlmQkVNdG9OX2lnand4eUlRb25TbFBJSGh3Um14bUNzU2lmNkpaNXhfZFEifQ"}
resp = urllib.request.urlopen(url2)
file = open(filePath, 'wb')
for num in range(1, 15):
    data = resp.read(size)
    file.write(data)
resp.close()
file.close()
print('Down')
