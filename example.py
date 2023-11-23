import HttpAntiDebug

req = HttpAntiDebug.get('https://jsonip.com')
print(req.status_code)
print(req.text)
print(req.headers)

session = HttpAntiDebug.SessionServer('https://jsonip.com', '172.64.163.16')
req = session.get('/')
print(req.status_code)
print(req.text)
print(req.headers)