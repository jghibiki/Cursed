import socket
import json
import struct
import time
import threading
import logging

log = logging.getLogger('simple_example')

class JsonSocket:
    def __init__(self, address='127.0.0.1', port=5489):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.conn = self.socket
        self._timeout = None,
        self._address = address
        self._port = port

    def send(self, obj):
        msg = json.dumps(obj)
        if self.socket:
            frmt = "=%ds" % len(msg)
            packedMsg = struct.pack(frmt, msg.encode("UTF-8"))
            packedHdr = struct.pack('=I', len(packedMsg))

            self._send(packedHdr)
            self._send(packedMsg)

    def _send(self, msg):
        sent = 0
        while sent < len(msg):
            sent += self.conn.send(msg[sent:])

    def _read(self, size):
        data = ''
        while len(data) < size:
            dataTmp = self.conn.recv(size-len(data))
            data += dataTmp.decode("UTF-8")
            if dataTmp == '':
                raise RuntimeError("socket conection broken")
        return data

    def _read_hdr(self, size):
        data = b''
        while len(data) < size:
            dataTmp = self.conn.recv(size-len(data))
            data += dataTmp
            if dataTmp == '':
                raise RuntimeError("socket conection broken")
        return data

    def _msgLength(self):
        d = self._read_hdr(4)
        s = struct.unpack('=I', d)
        return s[0]

    def read(self):
        size = self._msgLength()
        data = self._read(size).encode("UTF-8")
        frmt = "=%ds" % size
        msg = struct.unpack(frmt, data)
        return json.loads(msg[0].decode("UTF-8"))

    def close(self):
        self._closeSocket()
        if self.socket is not self.conn:
            self._closeConnection()

    def _closeSocket(self):
        self.socket.close()

    def _closeConnection(self):
        self.conn.close()

    def _get_timeout(self):
        return self._timeout

    def _set_timeout(self, timeout):
        self._timeout = timeout
        self.socket.settimeout(timeout)

    def _get_address(self):
        return self._address

    def _set_address(self, address):
        pass

    def _get_port(self):
        return self._port

    def _set_port(self, port):
        pass

    timeout = property(_get_timeout, _set_timeout, doc='Get/set socket timeout')
    address = property(_get_address, _set_address, doc='Get/set socket address')
    port = property(_get_port, _set_port, doc='Get/set socket port')


class JsonServer(JsonSocket):
    def __init__(self, address='127.0.0.1', port=5489):
        super(JsonServer, self).__init__(address, port)
        self._bind()

    def _bind(self):
        self.socket.bind( (self.address, self.port) )

    def _listen(self):
        self.socket.listen(20)

    def _accept(self):
        return self.socket.accept()

    def acceptConnection(self):
        self._listen()

        self.conn, addr = self._accept()
        self.conn.settimeout(self.timeout)


class JsonClient(JsonSocket):
    def __init__(self, address='127.0.0.1', port=5489):
        super(JsonClient, self).__init__(address, port)

    def connect(self):
        for i in range(60):
            try:
                self.socket.connect((self.address, self.port))
            except socket.error as msg:
                #print("SocketError: %s" % msg)
                time.sleep(3)
                continue
            #print("Socket Connected")
            return True
        return False


class ThreadedJsonServer(threading.Thread, JsonServer):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        JsonServer.__init__(self)
        self._isAlive = False

    def _processMessage(self, obj):
        """ Virtual method """
        pass

    def _each_iteration(self):
        """ Virtual method """
        pass

    def run(self):
        while self._isAlive:
            self._each_iteration()
            try:
                self.acceptConnection()
            except socket.timeout as e:
                #print("socket.timeout %s" % e)
                continue
            except Exception as e:
                #print(e)
                continue

            while self._isAlive:
                self._each_iteration()
                try:
                    obj = self.read()
                    self._processMessages(obj)
                except socket.timeout as e:
                    #print("socket.timeout %s" % e)
                    pass
                except Exception as e:
                    #print(e)
                    self._closeConnection()
                    break

    def start(self):
        self._isAlive = True
        log.debug("server started")
        super(ThreadedJsonServer, self).start()

    def stop(self):
        log.debug("server stopped")
        self._isAlive = False


class Server(ThreadedJsonServer):
    def __init__(self, queue):
        super(Server, self).__init__()
        self.timeout = 2.0
        self.queue = queue
        self.map_data = None

    def _each_iteration(self):
        try:
            q_data = self.queue.get_nowait()
            if q_data:
                self.map_data = q_data
        except:
            pass

    def _processMessages(self, obj):
        log.debug("server tick")
        if obj != '':
            #print(obj)
            if "command" in obj:

                if obj["command"] == "get":
                    self.send(self.map_data)
                    self.run()
                elif obj["command"] == "kill":
                    print("Killing server...")
                    self.stop()
                    print("Exiting...")
                    exit()



