import network
import socket
import time

OTA_RETRY = 0
MAX_OTA_RETRY = 3
SLEEP_TIME__S = 1

SSID_PREFIX = "BFH-Challenge-"
OTA_PORT = 880

def _fetch_fw(ip):
    sock_info = socket.getaddrinfo(ip, OTA_PORT, 0, socket.SOCK_STREAM)[0][-1]
    print(f'[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] Fetching from: {sock_info}')
    try:
        s = socket.socket()
        s.connect(sock_info)
        print(f'[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] Connected')

        fw_len = len(s.read())
        print(f'[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] Got response: {fw_len} bytes')
        s.close()
    except Exception as ex:
        print(f'[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] Failed fetching OTA, {type(ex)} {ex}')
        return False

    return True

def _update_fom_station(sta_if, ssid):
    sta_if.connect(ssid)

    for _ in range(MAX_OTA_RETRY):
        if sta_if.isconnected():
            break
        print(f'[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] Waiting for connection')
        time.sleep(SLEEP_TIME__S)

    (ip, netmask, gateway, dns) = sta_if.ifconfig()
    print(f'[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] Connected: {sta_if.ifconfig()}')
    return _fetch_fw(gateway)

def _do_update(sta_if):
    update_completed = False
    stations = sta_if.scan()
    for (ssid, bssid, channel, RSSI, security, hidden) in stations:
        if ssid.startswith(SSID_PREFIX):
            print(f'[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] Connecting to network: {ssid}')
            if _update_fom_station(sta_if, ssid):
                update_completed = True

    return update_completed

def start_ota():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    while sta_if.active() == False:
      pass

    global OTA_RETRY
    for OTA_RETRY in range(MAX_OTA_RETRY):
        print(f'[OTA {OTA_RETRY}/{MAX_OTA_RETRY}] Searching for OTA device')
        if _do_update(sta_if):
            break
        time.sleep(SLEEP_TIME__S)
