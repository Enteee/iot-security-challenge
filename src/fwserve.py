import socket
import _thread

OTA_PORT = 880
ADDR = socket.getaddrinfo("0.0.0.0", OTA_PORT)[0][-1]


def _accept_connection(sock):
    cl, addr = sock.accept()

    print(f"[FW] client connected from: {addr}")
    with open("ota_firmware.zip", "rb") as fd:
        while True:
            data = fd.read(100)
            if not data:
                break
            cl.send(data)

    print(f"[FW] closing socket")
    cl.close()


def _bind_socket():
    sock = socket.socket()
    sock.bind(ADDR)
    sock.listen(10)
    return sock


def _serve_fw_thread():
    print(f"[FW] binding socket")
    sock = None
    while sock is None:
        try:
            sock = _bind_socket()
        except Exception as ex:
            print(f"[FW] failed: {type(ex)} {ex}")

    print(f"[FW] accepting connection")
    while True:
        try:
            _accept_connection(sock)
        except Exception as ex:
            print(f"[FW] failed: {type(ex)} {ex}")


def serve_fw():
    print(f"[FW] start serving firmware")
    _thread.start_new_thread(_serve_fw_thread, ())
