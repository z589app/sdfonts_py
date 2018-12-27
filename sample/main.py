
from m5stack_print import M5StackPrint
import utime
import uos
import machine

FONTPATH = '/sd/font/FONT.BIN'


def th_time():

    _thread.allowsuspend(True)

    m5p_date = M5StackPrint(FONTPATH, font_size=16, rect=(0,0,16*6,16*1))
    m5p_date.font_color = 0xFF8080
    m5p_time = M5StackPrint(FONTPATH, font_size=16, rect=(16*7,0,16*6,16*1))
    m5p_time.font_color = 0x80FF80
    
    ## Time
    for i in range(10):
        t = utime.localtime()
        t_date = u"{:04}/{:02}/{:02}".format(t[0], t[1], t[2])
        t_time = u"{:02}:{:02}:{:02}".format(t[3], t[4], t[5])

        m5p_date.print(t_date)
        m5p_time.print(t_time)

        utime.sleep_ms(1000)
        



btnAStr = u'あ'
thid = None

def btnA_pressed():
    lcd.clear()

    m5p_mess = M5StackPrint(FONTPATH, font_size=16, rect=(0,16*2,320,240-16*2))

    import _thread
    global thid
    if thid==None:
        thid = _thread.start_new_thread("THTIME", th_time, None)
    else:
        _thread.kill(thid)
        thid = None
    
    ## Message
    global btnAStr
    s = btnAStr
    mess = s
    for j in range(100):
        s = chr(ord(s) + 1)
        if s == u'ン':
            s = u'亜'
        if s == u'鰐':
            s = u'あ'
        mess += s

    btnAStr = s

    m5p_mess.print(mess)

    

def btnB_pressed():
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

def btnC_pressed():
    lcd.clear()

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

    m5p.print(u"aAあア亜\n")

