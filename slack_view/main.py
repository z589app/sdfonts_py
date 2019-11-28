
from m5stack_print import M5StackPrint
import utime
import uos
import machine
import time
import sdfonts_py
import _thread
import urequests

from slack_env import *
## import re

FONTPATH = '/sd/font/FONT.BIN'

def th_time():

    ## _thread.allowsuspend(True)

    m5p_date = M5StackPrint(FONTPATH, font_size=16, rect=(0,0,16*6,16*1))
    m5p_date.font_color = 0xFF8080
    m5p_time = M5StackPrint(FONTPATH, font_size=16, rect=(16*7,0,16*6,16*1))
    m5p_time.font_color = 0x80FF80
    
    ## Time
    while True:
        t = utime.localtime()
        t_date = u"{:04}/{:02}/{:02}".format(t[0], t[1], t[2])
        t_time = u"{:02}:{:02}:{:02}".format(t[3], t[4], t[5])

        m5p_date.print(t_date)
        m5p_time.print(t_time)

        time.sleep(1)

def connectWIFI():
    ## WIFI
    m5p_wifi = M5StackPrint(FONTPATH, font_size=16, rect=(0,0,320,16*8),
        append=True)
    m5p_wifi.clear() ## if append=True

    import simple_wifi
    simple_wifi.do_connect(m5p_wifi.print)

    m5p_wifi.print(u"Sync RTC\n")
    rtc = machine.RTC()
    rtc.ntp_sync(server='ntp.nict.jp', tz='JST-9')
    for _ in range(100):
        if rtc.synced():
            break
        utime.sleep_ms(10)
    m5p_wifi.print(u"Synced:{}\n".format(rtc.synced()))
    m5p_wifi.print(u"Connected RTC\n")

def getSlack():
    m5p = M5StackPrint(FONTPATH, font_size=16, rect=(0,0,320-16,16*8),
        append=True)
    m5p.clear() ## if append=True

    url = "https://slack.com/api/channels.history"
    url = url + "?token=" + SLACK_TOKEN + "&channel=" + SLACK_CHANNEL_ID + "&count=5"
    print(url)
    response = urequests.get(url)
    ## response = urequests.get(url, data=payload)

    json_data = response.json()
    messages = json_data["messages"]
    for i in sorted(messages, key=lambda mes: mes['ts'], reverse=True)[5::-1]:
        text = i['text']
        user = i['user']
        ## text = re.sub(r':[\w_]*:', "", text)
        m5p.print(text + "\n")
        ## m5p.print(user + ": " + text + "\n")
    m5p = None

def btnA_pressed():
    lcd.clear()
    getSlack()

def btnB_pressed():
    lcd.clear()

def btnC_pressed():
    lcd.clear()
    connectWIFI()

if __name__ == '__main__':

    buttonA.wasPressed(callback=btnA_pressed)
    buttonB.wasPressed(callback=btnB_pressed)
    buttonC.wasPressed(callback=btnC_pressed)

    uos.mountsd()

    m5p = M5StackPrint(FONTPATH)
    m5p.font_size = 16
    m5p.font_color = 0xFFFFFF
    m5p.back_color = 0x444444
    m5p.rect = (0, 0, 320, 240)
    m5p.append = False

    lcd.clear()
    connectWIFI()

