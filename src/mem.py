import pymemcache
from pymemcache.client.base import _recv, RECV_SIZE


class MemClient(pymemcache.Client):


    def __init__(self, host, port):

        super().__init__((host, port))


    def get_all_keys(self):
        return self._lru_crawler_metadump_all()


    def _lru_crawler_metadump_all(self):

        cmd = b'lru_crawler metadump all\r\n'
        result = None
        try:
            if self.sock is None:
                self._connect()

            self.sock.sendall(cmd)

            buf = b''
            result = []
            while True:
                buf, line = _readline(self.sock, buf)
                if line.startswith(b'OK') or line.startswith(b'END'):
                    break
                if line.startswith(b'key='):
                    result.append(line.split(b' ')[0].split(b'=')[1])
        except Exception:
            self.close()
            if self.ignore_exc:
                return []
            raise


        return result

def _readline(sock, buf):
    """
    patched version of _readline that handles \n instead of \r\n
    made specifically for handling the output of 'lru_crawler metadump'
    """
    chunks = []
    last_char = b''

    while True:
        if buf.find(b'\n') != -1:
            before, sep, after = buf.partition(b"\n")
            chunks.append(before)
            return after, b''.join(chunks)

        if buf:
            chunks.append(buf)
            last_char = buf[-1:]

        buf = _recv(sock, RECV_SIZE)
        if not buf:
            raise Error()


def connect(host='localhost', port=11211):

    return MemClient(host, port)

