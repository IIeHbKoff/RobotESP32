try:
    import usocket as socket
except ImportError:
    import socket

SYM_STAR = "*"
SYM_PLUS = "+"
SYM_MINUS = "-"
SYM_COLON = ":"
SYM_DOLLAR = "$"
SYM_CRLF = "\r\n"
SYM_EMPTY = ""


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
        self._opened_pipeline = False
        self._cmds = list()

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

    def pipeline(self, transaction=False):
        if self._opened_pipeline:
            raise RedisError("You already has opened pipeline")
        self._opened_pipeline = True
        return self

    def execute(self):
        self._opened_pipeline = False
        res = self._execute_many()
        self._cmds.clear()
        return res

    def _execute(self, cmd, *args):
        if not self._sock:
            raise RedisError("Not connected: use 'connect()' to connect to Redis server.")

        request = self._encode_request(cmd, *args)

        if self.debug:
            print("SEND: {!r}".format(request))

        self._sock.send(request.encode('utf-8'))
        return self._read_response()

    def _execute_many(self):
        pieces = list()
        result = list()
        for cmd in self._cmds:
            pieces.append(self._encode_request(*cmd))
        request = SYM_EMPTY.join(pieces)
        self._sock.send(request.encode('utf-8'))
        for _ in range(len(pieces)):
            result.append(self._read_response())
        return result

    def get(self, key: str):
        cmd = "GET"
        if self._opened_pipeline:
            self._cmds.append((cmd, key))
        else:
            return self._execute(cmd, key)

    def set(self, key: str, data: str):
        cmd = "SET"
        if self._opened_pipeline:
            self._cmds.append((cmd, key, data))
        else:
            return self._execute(cmd, key, data)

    @staticmethod
    def _encode_request(*args):
        """Pack a series of arguments into a RESP array of bulk strings."""
        result = [f"{SYM_STAR}{str(len(args))}{SYM_CRLF}"]

        for arg in args:
            if arg is None:
                result.append(f"{SYM_DOLLAR}-1{SYM_CRLF}")
            else:
                s = str(arg)
                result.append(f"{SYM_DOLLAR}{str(len(s))}{SYM_CRLF}{s}{SYM_CRLF}")
        return "".join(result)

    def _read_response(self):
        line = self._read_until(lambda l, pos: l[-2:] == SYM_CRLF.encode())
        rtype = line[:1].decode('utf-8')

        if rtype == SYM_PLUS:
            return line[1:-2]
        elif rtype == SYM_MINUS:
            raise RedisError(*line[1:-2].decode('utf-8').split(None, 1))
        elif rtype == SYM_COLON:
            return int(line[1:-2])
        elif rtype == SYM_DOLLAR:
            length = int(line[1:-2])
            if length == -1:
                return None

            return self._read_until(lambda l, pos: pos == length + 2)[:-2]
        elif rtype == SYM_STAR:
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
