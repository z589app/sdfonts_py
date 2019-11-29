
from m5stack import *

from m5stack_print import M5StackPrint
import utime
## import uos
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

def show_time():

    m5p_date = M5StackPrint(FONTPATH, font_size=16, rect=(0,0,16*6,16*1))
    m5p_date.font_color = 0xFF8080
    m5p_time = M5StackPrint(FONTPATH, font_size=16, rect=(16*7,0,16*6,16*1))
    m5p_time.font_color = 0x80FF80
    
    ## Time
    t = utime.localtime()
    t_date = u"{:04}/{:02}/{:02}".format(t[0], t[1], t[2])
    t_time = u"{:02}:{:02}:{:02}".format(t[3], t[4], t[5])

    m5p_date.print(t_date)
    m5p_time.print(t_time)


def connectWIFI():
    ## WIFI
    m5p_wifi = M5StackPrint(FONTPATH, font_size=16, rect=(0,0,320,16*8),
        append=True)
    m5p_wifi.clear() ## if append=True

    import simple_wifi
    simple_wifi.do_connect(m5p_wifi.print)

    m5p_wifi.print(u"Sync RTC\n")
    import ntptime
    ntptime.settime(9*60*60)
    m5p_wifi.print(u"Connected RTC\n")

def getSlack():
    m5p = M5StackPrint(FONTPATH, font_size=24, rect=(0,16*2,320-16,16*8),
        append=True)
    m5p.clear() ## if append=True

    show_time()

    COUNT = 5
    url = "https://slack.com/api/channels.history"
    ## url = url + "?token=" + SLACK_TOKEN + "&channel=" + SLACK_CHANNEL_ID + "&count=5"
    url = "{0}?token={1}&channel={2}&count={3}".format(url, SLACK_TOKEN, SLACK_CHANNEL_ID, COUNT)
    print(url)
    response = urequests.get(url)
    ## response = urequests.get(url, data=payload)

    json_data = response.json()
    messages = json_data["messages"]
    texts = sorted(messages, key=lambda mes: mes['ts'], reverse=False)
    texts = [m['text'] for m in texts]
    ## ## 後ろから数えて行って超えたら終わり。
    ## MAX_LINE, MAX_CHAR = 8, 13 ##?
    ## l, c = 0, 0
    ## i = 1
    ## for text in reversed(texts):
    ##     l += text.count('\n')
    ##     for t in text.split('\n'):
    ##         l += (len(str(t)) // MAX_CHAR)
    ##     if l >= MAX_LINE:
    ##         break
    ##     i += 1
    ##     
    ## for text in texts[5-i:]:
    ##     m5p.print(text + "\n")
    for text in texts:
        m5p.print(text + "\n")
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

    btnA.wasPressed(callback=btnA_pressed)
    btnB.wasPressed(callback=btnB_pressed)
    btnC.wasPressed(callback=btnC_pressed)

    ## uos.mountsd()

    m5p = M5StackPrint(FONTPATH)
    m5p.font_size = 16
    m5p.font_color = 0xFFFFFF
    m5p.back_color = 0x444444
    m5p.rect = (0, 0, 320, 240)
    m5p.append = False

    lcd.clear()
    connectWIFI()

