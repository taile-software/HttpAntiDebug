# HttpAntiDebug #
https://github.com/taile-software/HttpAntiDebug

Hiện tại có rất nhiều đối tượng xấu đã sử sụng 1 thủ thuật là bắt traffic http để có response và fake 1 server localhost để fake server của 1 phần mềm, tools,...

**Thư viện này sẽ giúp bạn vá đi được phần nào đó của lỗ hổng này ( không thể an toàn tuyệt đối )**

* Vẫn hoạt động ổn định cho tới hiện tại
* Sử dụng Python >= 3.6

## **Installation** ##
```
pip install HttpAntiDebug
```
hoặc bạn có thể install từ github: 
```
pip install git+https://github.com/taile-software/HttpAntiDebug@master
```

## **Chi tiết** ##

Thư viện được xây dựng trên nền tảng socket để tránh bị ghi lại các traffic http

Được xây dựng sao cho tương đối giống với thư viện phổ biến trong Python hiện nay là ```requests```, lớp, method, function khá tương tự với ```requests```

```
req = HttpAntiDebug.get('https://jsonip.com')
print(req.status_code)
print(req.text)
print(req.headers)
```

**Về cơ bản cách dùng của ```HttpAntiDebug``` chỉ khác 1 chút không đáng kể tại lớp quản lý phiên ```Session```**

Trong ```requests``` Session được quản lí 1 theo hướng mở còn ```HttpAntiDebug``` chỉ quản lí giữa ***Client*** và ***Server*** cố định

## ***Trươc khi dùng*** ##

![Screenshot 2023-11-23 230206](https://github.com/taile-software/HttpAntiDebug/assets/151706988/38be65c5-8a4c-4c10-b012-8b58b0cb0e51)

## ***Sau khi dùng*** ##

![Screenshot 2023-11-23 230544](https://github.com/taile-software/HttpAntiDebug/assets/151706988/7df1f2cc-26cd-4134-bd72-f59fd97dbeae)

```
session = HttpAntiDebug.SessionServer('https://jsonip.com', '172.64.163.16')
req = session.get('/')
print(req.status_code)
print(req.text)
print(req.headers)
```

Sử dụng thủ thuật so sánh, khi bạn điền vào 1 baseIP ( IP Cố định ), thì thư viện sẽ ghi nhớ rằng đó là ip của hostting server

Nếu IP không hợp lệ sẽ báo lỗi

![image](https://github.com/taile-software/HttpAntiDebug/assets/151706988/df7037ce-403d-48ac-9d79-5772f358f249)

Ngoài ra thư viện cung cấp 1 khả năng nhẹ nữa chống chỉnh sửa file hosts, file hosts là file cấu hình dns, ip của domain người nào đó có thể sử dụng nó để trỏ domain server của bạn về localhost, lúc này thư viện sẽ từ chối quyền truy cập và thông báo lỗi

![Screenshot 2023-11-23 231222](https://github.com/taile-software/HttpAntiDebug/assets/151706988/aab2566c-2931-49b6-8f17-2d8867751004)


# **Usage** #

## Methode cơ bản ##

Về cơ bản bạn chỉ cần install và import thư viện
```
import HttpAntiDebug as hd
```

Và sau đó có thể gán cho 1 biến hoặc không rồi sử dụng tương tự ```requests```
> ### Method: GET ###

```
rq = hd.get('https://excample.com')
if rq.status_code == 200:
    print(rq.text)
```

> ### Method: POST ###

Trong post bạn có thêm form-data tương tự với ```requests```
```
payload = {'name1': 'value', 'name2': int}
rq = hd.get('https://excample.com', data = data)
if rq.status_code == 200:
    print(rq.text)
```

> ### Headers tùy chỉnh ###

Với trường hợp bạn có headers tùy chỉnh muốn dùng với http thì gán tương tự lun !

```
headers = {
    'accept': "*",
    'Host': "jsonip.com",
    'Content-Type': 'application/x-www-form-urlencoded'
}
rq = hd.get('https://example.com', headers = headers)
```

> ## SessionServer ##

Trong ***```HttpAntiDebug```*** có phương thức lớp ***```SessionServer```*** giống ***```Session```*** của ***```requests```***

Tuy nhiên không giống 100% mà trong ***```HttpAntiDebug```*** sẽ có sự thay đổi nhẹ của lớp này

Lớp ***```SessionServer```*** sẽ chỉ giữ kết nối duy nhất 2 đầu là ***Client*** và ***Server***, ngoài ra nếu bạn muốn thêm kết nối tới 1 host khác thì đồng nghĩa với việc bạn phải gọi Phương thức này 1 lần nữa

```
from AntiDebug import SessionServer as SV

sess = SV('https://jsonip.com')

```

Thay vì mỗi lần tạo giao thức phải điền cả 1 url vào thì với ***```HttpAntiDebug.SessionServer```*** chỉ cần điền tham số là ```path```

>PATH: Là đường dẫn địa chỉ dẫn tới mục tài nguyên được lưu trữ tại server

```
sess.get('/').text
sess.post('/auth/login', data = {'username': "example", 'password': "ExamplePassword123"}).json
```

# **Kết thúc** #

## Contact ##

Zalo: 0358768395

Telegram: @tlsoftware
