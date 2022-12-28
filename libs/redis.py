try:
    import usocket as socket
except ImportError:
    import socket

try:
    import uselect as select
except ImportError:
    import select

CRLF = "\r\n"


class RedisError(Exception):
    """RESP error returned by the Redis server."""
    pass


class RedisTimeout(Exception):
    """Reply from the Redis server cannot be read within timeout."""


class ParseError(Exception):
    """Invalid input while parsing RESP data."""
    pass


class Redis:
    """A very minimal Redis client."""

    def __init__(self, host='127.0.0.1', port=6379, timeout=3000, debug=False):
        self.debug = debug
        self._sock = None
        self._host = host
        self._port = port
        self._timeout = timeout

    def __call__(self, cmd, *args):
        return self.do_cmd(cmd, *args)

    def __getattr__(self, name):
        if name.isalpha():
            return lambda *args: self.do_cmd(name, *args)

        raise AttributeError

    def connect(self):
        if not self._sock:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect(socket.getaddrinfo(self._host, self._port)[0][-1])

    def close(self):
        if self._sock:
            self._sock.close()
            self._sock = None

    def do_cmd(self, cmd, *args):
        if not self._sock:
            raise RedisError("Not connected: use 'connect()' to connect to Redis server.")

        request = self._encode_request(cmd, *args)

        if self.debug:
            print("SEND: {!r}".format(request))

        self._sock.send(request.encode('utf-8'))
        return self._read_response()

    def get(self, key: str):
        return self.do_cmd("GET", key).decode()

    def set(self, key: str, data: str):
        return self.do_cmd("SET", key, data).decode()

    @staticmethod
    def _encode_request(*args):
        """Pack a series of arguments into a RESP array of bulk strings."""
        result = ["*" + str(len(args)) + CRLF]

        for arg in args:
            if arg is None:
                result.append('$-1' + CRLF)
            else:
                s = str(arg)
                result.append('$' + str(len(s)) + CRLF + s + CRLF)

        return "".join(result)

    def _read_response(self):
        line = self._read_until(lambda l, pos: l[-2:] == b'\r\n')
        rtype = line[:1].decode('utf-8')

        if rtype == '+':
            return line[1:-2]
        elif rtype == '-':
            raise RedisError(*line[1:-2].decode('utf-8').split(None, 1))
        elif rtype == ':':
            return int(line[1:-2])
        elif rtype == '$':
            length = int(line[1:-2])

            if length == -1:
                return None

            return self._read_until(lambda l, pos: pos == length + 2)[:-2]
        elif rtype == '*':
            length = int(line[1:-2])

            if length == -1:
                return None

            return [self._read_response() for _ in range(length)]
        else:
            raise ParseError("Invalid response header byte.")

    def _read_until(self, predicate):
        buf = b''
        pos = 0
        while not predicate(buf, pos):
            try:
                self._sock.settimeout(5)
                buf += self._sock.recv(1)
                pos += 1
            except TimeoutError:
                self.close()
                raise RedisTimeout
        return buf
