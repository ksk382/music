import requests

url = 'http://www.ticketfly.com/api/events/list.json?orgId=1&location=geo:41.8755546,-87.6244212&distance=20mi&fromDate=2018-06-10&&thruDate=2018-08-09&fields=venue.city,startDate,venue.name,headlinersName,supportsName&pageNum=1'
print ('\n', url, '\n')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
resp = requests.get(url, headers=headers)
data = resp.json()
print (data)