import requests
key = "9539824b7075b630f3afb1d9c353d1b0"
address="南京"
url="https://restapi.amap.com/v3/geocode/geo?address="+address+"&key="+key
res=requests.post(url=url)
print(res.text)