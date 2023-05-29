import socket
import _thread

OTA_PORT = 880
ADDR = socket.getaddrinfo("0.0.0.0", OTA_PORT)[0][-1]


def _accept_connection(sock):
    cl, addr = sock.accept()

    print(f"[FW] Client connected from: {addr}")
    with open("ota_firmware.zip", "rb") as fd:
        cl.send(fd.read())

    print(f"[FW] Closing socket")
    cl.close()


def _bind_socket():
    sock = socket.socket()
    sock.bind(ADDR)
    sock.listen(1)
    return sock


def _serve_fw_thread():
    print(f"[FW] Binding socket")
    sock = None
    while sock is None:
        try:
            sock = _bind_socket()
        except Exception as ex:
            print(f"[FW] Failed: {type(ex)} {ex}")

    print(f"[FW] Accepting connection")
    while True:
        try:
            _accept_connection(sock)
        except Exception as ex:
            print(f"[FW] Failed: {type(ex)} {ex}")


def serve_fw():
    print(f"[FW] Start serving firmware")
    _thread.start_new_thread(_serve_fw_thread, ())
