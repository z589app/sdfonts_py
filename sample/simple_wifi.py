import _thread, network, ujson, ubinascii, machine
from m5stack import lcd
import utime as time

wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)

def do_connect(printfunc):
    if wlan_sta.isconnected():
        printfunc("Connected Wifi\n")
        return True

    try:
        with open("config.json") as f:
            jdata = ujson.loads(f.read())
            ssid = jdata['wifi']['ssid']
            passwd = jdata['wifi']['password']
    except:
        printfunc("Check wificonfig.json")
        return False

    printfunc('Connect WiFi: SSID:{}\n'.format(ssid))
    wlan_sta.connect(ssid, passwd)
    printfunc('Connecting.')
    a=0
    while not wlan_sta.isconnected() | (a > 50) :
        time.sleep_ms(500)
        a+=1
        printfunc('.')
    printfunc("\n")
    if wlan_sta.isconnected():
        printfunc("Connected!{}\n".format(ssid))
        return (True)
    else : 
        printfunc('Problem. Not Connected to :{}\n'.format(ssid))
        return (False)

def isconnected():
    return wlan_sta.isconnected()

