class HTTPAntiError(Exception):
    def __init__(self, message, response=None):
        super().__init__(message)
        self.response = response
    
    def __str__(self):
        if self.response: return self.response
        return ''

class NotFoundURL(HTTPAntiError):...

class HTTPError(HTTPAntiError):...

class ConnectionError(HTTPAntiError):...

class InvalidResponseError(HTTPAntiError):...

class JSONDecodeError(InvalidResponseError):...

class ProxyError(ConnectionError):...

class SSLError(ConnectionError):...

class PermissionDenied(HTTPAntiError):...

class BaseIpError(HTTPAntiError):
    def __init__(self, message, ip_host, base_ip):
        self.ip_host = ip_host
        self.base_ip = base_ip
        super().__init__(message, f"{self.args[0]}\nIP Host: {self.ip_host}\nIP Default: {self.base_ip}")