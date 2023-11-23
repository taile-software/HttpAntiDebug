import json

__attrs__ = [
    'text', 
    'json'
]

class Response:
    
    def __init__(self, response) -> None:
        status_line, _, rest = response.partition('\r\n')
        self.status_code = self._parse_status_line(status_line)
        headers, _, body = response.partition('\r\n\r\n')
        self.headers = self._parse_headers(headers)
        self.body = self._parse_body(body)

    def _parse_status_line(self, status_line):
        parts = status_line.split(' ', 2)
        if len(parts) >= 2 and parts[1].isdigit():
            return int(parts[1])
        else:
            raise ValueError("Không thể phân tích dòng trạng thái HTTP.")
        
    def _parse_headers(self, headers):
        header_lines = headers.split('\r\n')
        header_dict = {}
        for line in header_lines[1:]:
            key, value = line.split(': ', 1)
            header_dict[key] = value
        return header_dict

    def _parse_body(self, body):
        if 'chunked' in self.headers.get('Transfer-Encoding', ''):
            return self._parse_chunked_body(body)
        else:
            return body
    
    def _parse_chunked_body(self, body):
        chunks = body.split('\r\n')
        body = ''
        for i in range(0, len(chunks), 2):
            if chunks[i] == '0':
                break
            size = int(chunks[i], 16)
            body += chunks[i + 1][:size]
        return body
    
    @property
    def text(self):
        return self.body
    
    @property
    def json(self):
        try:
            return json.loads(self.body)
        except json.JSONDecodeError:
            raise ValueError("Phản hồi trả về không phải là 1 JSON")
        
