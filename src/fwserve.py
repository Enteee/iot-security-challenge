import socket
import _thread

ADDR = socket.getaddrinfo('0.0.0.0', 880)[0][-1]

def _serve_fw_thread():
    print(f'[FW] Binding socket')
    s = socket.socket()
    s.bind(ADDR)
    s.listen(1)

    while True:
        print(f'[FW] Accepting connection')
        try:
            cl, addr = s.accept()
            print(f'[FW] Client connected from: {addr}')
            with open("ota_firmware.zip", "rb") as fd:
                cl.send(fd.read())
            print(f'[FW] Serving firmware done')
        except:
            print(f'[FW] Failed serving firmware')

        try:
            cl.close()
        except:
            print(f'[FW] Failed closing socket')

def serve_fw():
    _thread.start_new_thread(_serve_fw_thread, ())
