import network
import socket
import time

OTA_RETRY = 0
MAX_OTA_RETRY = 3
SLEEP_TIME__S = 1
FETCH_SOCKET_TIMEOUT__S = 1.0

SSID_PREFIX = "IOT-Challenge-"
OTA_PORT = 880


def _fetch_fw(ip):
    sock_info = socket.getaddrinfo(ip, OTA_PORT, 0, socket.SOCK_STREAM)[0][-1]
    print(f"[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] connecting to: {sock_info}")
    sock = socket.socket()
    sock.settimeout(FETCH_SOCKET_TIMEOUT__S)
    sock.connect(sock_info)

    fw_len = len(sock.read())
    print(f"[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] got firmware: {fw_len} bytes")

    sock.close()


def _update_fom_station(sta_if, ssid):
    sta_if.connect(ssid)

    for _ in range(MAX_OTA_RETRY):
        if sta_if.isconnected():
            break
        print(f"[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] waiting for connection")
        time.sleep(SLEEP_TIME__S)

    (ip, netmask, gateway, dns) = sta_if.ifconfig()
    print(f"[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] connected: {sta_if.ifconfig()}")
    _fetch_fw(gateway)
    sta_if.disconnect()


def _do_update(sta_if):
    update_completed = 0
    print(f"[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] searching for OTA device")
    stations = sta_if.scan()
    for ssid, bssid, channel, RSSI, security, hidden in stations:
        if ssid.startswith(SSID_PREFIX):
            print(f"[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] connecting to network: {ssid}")
            _update_fom_station(sta_if, ssid)
            update_completed += 1

    print(f"[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] updated from {update_completed} devices")
    return update_completed > 0


def _reset_sta_if(sta_if):
    sta_if.active(False)
    while sta_if.active():
        pass

    sta_if.active(True)
    while not sta_if.active():
        pass

    sta_if.disconnect()
    while sta_if.isconnected():
        pass


def start_ota():
    global OTA_RETRY
    sta_if = network.WLAN(network.STA_IF)
    print(f"[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] start OTA")
    for OTA_RETRY in range(MAX_OTA_RETRY):
        try:
            _reset_sta_if(sta_if)
            if _do_update(sta_if):
                print(f"[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] update completed")
                break
        except Exception as ex:
            print(f"[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] failed: {type(ex)} {ex}")
        finally:
            sta_if.active(False)
            while sta_if.active():
                pass

        time.sleep(SLEEP_TIME__S)
