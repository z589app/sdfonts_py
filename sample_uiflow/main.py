from m5stack import *
from m5ui import *
from uiflow import *

from m5stack_print import M5StackPrint
import utime
## import uos
import machine
import time
import sdfonts_py
import _thread

FONTPATH = '/sd/font/FONT.BIN'

def show_time():

    ## _thread.allowsuspend(True)

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


btnAStr = u'あ'

def btnA_pressed():
    lcd.clear()

    ## Message
    m5p_mess = M5StackPrint(FONTPATH, font_size=16, rect=(0,16*2,320-1,240-16*2))

    global btnAStr
    s = btnAStr
    mess = s
    for j in range(10):
        s = chr(ord(s) + 1)
        if s == u'ン':
            s = u'亜'
        if s == u'鰐':
            s = u'あ'
        mess += s

    btnAStr = s

    m5p_mess.print(mess)

    show_time()
    

def btnB_pressed():
    m5p_wifi = M5StackPrint(FONTPATH, font_size=16, rect=(0,0,320-1,16*8),
        append=True)
    m5p_wifi.clear() ## if append=True

    import simple_wifi
    simple_wifi.do_connect(m5p_wifi.print)

    m5p_wifi.print(u"Sync RTC\n")
    import ntptime
    ntptime.settime(9*60*60)
    m5p_wifi.print(u"Connected RTC\n")

def btnC_pressed():
    lcd.clear()

if __name__ == '__main__':

    btnA.wasPressed(callback=btnA_pressed)
    btnB.wasPressed(callback=btnB_pressed)
    btnC.wasPressed(callback=btnC_pressed)

    ## uos.mountsd()

    m5p = M5StackPrint(FONTPATH)
    m5p.font_size = 16
    m5p.font_color = 0xFFFFFF
    m5p.back_color = 0x444444
    m5p.rect = (0, 0, 320-1, 240)
    m5p.append = False

    lcd.clear()
    m5p.print(u"aAあア亜\n")

