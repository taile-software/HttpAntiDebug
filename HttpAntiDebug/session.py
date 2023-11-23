import socket
import ssl
import urllib.parse
from urllib.parse import urlparse
from .exception import *
from .response import *
import platform
import os


ip_base_secret = ''
__all__ = [
    'SessionServer'
]



def check_base_ip(function):
    '''
    Hàm dùng để so sánh IP mặc định và ip host xem có giống nhau
    Nếu 2 IP không giống nhau rất có thể có 1 đối tượng nào đó đã chỉnh sửa file host nhằm gian lận
    '''
    def base_ip_access(obj, *args, **kwargs):
        global ip_base_secret
        os_desktop = platform.platform().lower()
        if os_desktop.startswith('windows'):
            file_host = os.path.join(os.environ['SYSTEMROOT'], 'System32', 'drivers', 'etc', 'hosts')
        else:
            file_host = '/etc/hosts'
        data_hosts = open(file_host, 'r', encoding='utf-8-sig').read()
        if obj.host in data_hosts: 
            raise PermissionDenied('', "Bạn không có quyền truy cập")
        if ip_base_secret:
            ip_host = socket.gethostbyname(obj.host)
            if ip_host != ip_base_secret:
                raise BaseIpError("IP của host hiện tại không hợp lệ !", str(ip_host), ip_base_secret)
        return function(obj, *args, **kwargs)
    return base_ip_access


class SessionServer:
    """
    Class sử dụng để connect cố định giữa server và client
    Với chức năng ẩn đi các traffic http giúp bớt đi phần nào việc bị lộ thông tin server
    Thông tin server bị lộ các đối tượng xấu có thể dùng để fake 1 host server và gian lận, bẻ khóa phần mềm, ...
    
    Usage::
        sv = HttpAntiDebug.SessionServer(base_url, base_ip)
        ....
        `base_url`: là hostname ( domain ) và giao thức - VD: https://example.com\n
        `base_ip`: là IP Hostting, VPS, ... được cố định để bảo mật kết nối, không khả dụng với host connect vs bên thứ 3 như cloudflare,...\n
        >>> import HttpAntiDebug
        >>> had = HttpAntiDebug('https://example.com', '93.184.216.34)
        >>> had.get('/path')
    """
    def __init__(self, base_url: str, base_ip: int = None):
        global ip_base_secret
        if base_ip: 
            ip_base_secret = base_ip
        if base_url:
            self.base_url = base_url
            self.parsed_url = urlparse(base_url)
            self.host = self.parsed_url.hostname
            self.port = self.parsed_url.port or (443 if self.parsed_url.scheme == 'https' else 80)
            self.secure = self.parsed_url.scheme == 'https'
            self.headers = {"User-Agent": "HttpAntiDebug/1.0"}
            self.cookies = {}
        else: 
            raise NotFoundURL("Không được bỏ trống url server")

    def _create_socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.secure:
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=self.host)
            return sock
        except Exception as e: 
            raise ConnectionError('Không thể tạo kết nối tới server')

    def _save_cookies(self, response_headers):
        set_cookie_headers = response_headers.get('Set-Cookie')
        if set_cookie_headers:
            if isinstance(set_cookie_headers, list):
                for set_cookie in set_cookie_headers:
                    self._parse_and_save_cookie(set_cookie)
            else:
                self._parse_and_save_cookie(set_cookie_headers)

    def _parse_and_save_cookie(self, set_cookie):
        cookie_parts = set_cookie.split(';')[0]
        if '=' in cookie_parts:
            key, value = cookie_parts.split('=', 1)
            self.cookies[key.strip()] = value.strip()

    def _add_cookies_to_headers(self, headers):
        if self.cookies:
            cookie_header = '; '.join([f'{key}={value}' for key, value in self.cookies.items()])
            headers['Cookie'] = cookie_header

    def _format_request(self, method, path, headers=None, data=None):
        if not path.startswith('/'):
            path = '/' + path
        request_line = f"{method} {path} HTTP/1.1\r\n"
        combined_headers = {**self.headers, **(headers or {})}
        combined_headers["Host"] = self.host
        combined_headers["Connection"] = "close"
        self._add_cookies_to_headers(combined_headers)

        if data:
            data_str = str(urllib.parse.urlencode(data))
            combined_headers["Content-Length"] = str(len(data_str))
            combined_headers['Content-Type'] = "application/x-www-form-urlencoded"
        else:
            data_str = ""
            
        header_lines = "\r\n".join(f"{key}: {value}" for key, value in combined_headers.items())
        full_request = f"{request_line}{header_lines}\r\n\r\n{data_str}"
        return full_request.encode()

    @check_base_ip
    def request(self, method, path, headers=None, data=None):
        with self._create_socket() as sock:
            sock.connect((self.host, self.port))
            request = self._format_request(method, path, headers, data)
            sock.sendall(request)

            response = b""
            while True:
                recv = sock.recv(4096)
                if not recv:
                    break
                response += recv
            response_parsed = Response(response.decode())
            self._save_cookies(response_parsed.headers)
            return response_parsed

    def get(self, path, headers=None):
        '''
        Usage:
            HttpAntiDebug.get(path, headers)\n
            `path`: là các đường path dẫn tới nơi tài nguyên được lưu trữ: VD: /auth hoặc /login.php, ...
        '''
        return self.request("GET", path, headers)

    def post(self, path, headers=None, data=None):
        '''
        Usage:
            HttpAntiDebug.post(path, headers, data)\n
            `path`: là các đường path dẫn tới nơi tài nguyên được lưu trữ: VD: /auth hoặc /login.php, ...
        '''
        return self.request("POST", path, headers, data)

    def put(self, path, headers=None, data=None):
        '''
        Usage:
            HttpAntiDebug.put(path, headers, data)\n
            `path`: là các đường path dẫn tới nơi tài nguyên được lưu trữ: VD: /update.php, ...
        '''
        return self.request("PUT", path, headers, data)

    def delete(self, path, headers=None):
        '''
        Usage:
            HttpAntiDebug.delete(path, headers)\n
            `path`: là các đường path dẫn tới nơi tài nguyên cần xóa: VD: /remove.php, ...
        '''
        return self.request("DELETE", path, headers)

    def options(self, path, headers=None):
        '''
        Usage:
            HttpAntiDebug.options(path, headers)\n
            `path`: là các đường path dùng để kiểm tra các phương thức HTTP được hỗ trợ: VD: /check.php, ...
        '''
        return self.request("OPTIONS", path, headers)
    
