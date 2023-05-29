import esp
import gc

# Init
esp.osdebug(None)
gc.collect()

# Start OTA Update
import ota

ota.start_ota()

# Start access point
import ap

ap.start_ap()

# Start firware serve
import fwserve

fwserve.serve_fw()

# Start webserver
import webserver

webserver.start_server()
