import socket
from .response import Response
import ssl, json
from urllib.parse import urlparse
import urllib.parse

__all__ = ['get', 'post', 'put', 'delete', 'options']
def _requests(method, url, headers=None, data=None):
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
    path = parsed_url.path
    if parsed_url.query:
        path += '?' + parsed_url.query
    if not path:
        path = '/'

    request_line = f"{method} {path} HTTP/1.1\r\n"
    headers_requests = {
        "User-Agent": "HttpAntiDebug/1.0",
        "Host": host,
        "Connection": "close",
    }
    if data:
        data_str = str(urllib.parse.urlencode(data))
        headers_requests["Content-Length"] = str(len(data_str))
        headers_requests['Content-Type'] = "application/x-www-form-urlencoded"
    else:
        data_str = ""
        
    if headers:
        headers_requests.update(headers)
    header_lines = "\r\n".join(f"{key}: {value}" for key, value in headers_requests.items())
    full_request = f"{request_line}{header_lines}\r\n\r\n{data_str}"
    return host, port, full_request.encode()

def _send_request(method, url, headers=None, data=None):
    host, port, request = _requests(method, url, headers, data)
    parsed_url = urlparse(url)
    secure = parsed_url.scheme == 'https'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if secure:
            context = ssl.create_default_context()
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                ssock.connect((host, port))
                ssock.sendall(request)
                response = b""
                while True:
                    recv = ssock.recv(4096)
                    if not recv:
                        break
                    response += recv
        else:
            sock.connect((host, port))
            sock.sendall(request)
            response = b""
            while True:
                recv = sock.recv(4096)
                if not recv:
                    break
                response += recv
    return Response(response.decode())

def get(url, headers=None):
    return _send_request("GET", url, headers)

def post(url, headers=None, data=None):
    # Tương tự như phương thức GET nhưng sử dụng "POST" và xử lý data
    return _send_request("POST", url, headers, data)

def put(url, headers=None, data=None):
    # Tương tự như phương thức POST nhưng sử dụng "PUT"
    return _send_request("PUT", url, headers, data)

def delete(url, headers=None):
    # Tương tự như phương thức GET nhưng sử dụng "DELETE"
    return _send_request("DELETE", url, headers)

def options(url, headers=None):
    # Tương tự như phương thức GET nhưng sử dụng "OPTIONS"
    return _send_request("OPTIONS", url, headers)

    # Logic để gửi request và nhận response giống như trong phương thức GET
# requester = SimpleHttpRequester()
# response = get("https://jsonip.com", {"Accept": "text/html"})
# print(response.json)
