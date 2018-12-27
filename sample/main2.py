# -*- coding: utf-8 -*-

## from __future__ import print_function
import sdfonts_py
import uos


## print strings for M5Stack
def printKari(strings, fontpath, fontsize=8, rect=(0, 0, 320, 240), fg=0xFFFFFF, bg=0x000000):
    SDFont = sdfonts_py.SDFonts()
    SDFont.open(fontpath)
    SDFont.setFontSize(fontsize)

    start_x = rect[0]
    start_y = rect[1]
    end_x = rect[0] + rect[2]
    end_y = rect[1] + rect[3]
    x, y = start_x, start_y

    ## Fill backgound
    lcd.rect(x=rect[0], y=rect[1], width=rect[2], height=rect[3], color=bg, fillcolor=bg)

    for s in strings:
        b = SDFont.getFontData(s)
        w = SDFont.getWidth()
        h = SDFont.getHeight()
        x += w
        if x > end_x:
            x = start_x
            y += h
            if y > end_y:
                y = start_y
                break ## Over

        putc(s, x=x, y=y, fg=fg, bg=None, w=w, h=h)
        

def pixelM5(x, y, color):
    lcd.pixel(x, y, color)

def pixelTerm(x, y, color):
    pass

## print 1 Char to M5Stack
def putc(buf, x=0, y=0, fg=0xFFFFFF, bg=0x000000, w=8, h=8):
    if type(buf) is not bytearray:
        print("printTerm(), Error")
        return

    byteWidth = (w+7)>>3 ## RoundUp(w/8)

    b = 0
    for j in range(h):
        for i in range(w):
            if i%8==0: ## Next Byte
                b = buf[j*byteWidth + (i>>3)]
            else: ## Shift
                b = b<<1

            if b & 0x80:
                lcd.pixel(x+i, y+j, fg)
            elif bg!=None:
                lcd.pixel(x+i, y+j, bg)


## Kari, print to Terminal
def printTerm(buf, x=0, y=0, fg=0xFFFFFF, bg=0x444444, w=8, h=8):
    if type(buf) is not bytearray:
        print("printTerm(), Error")
        return

    byteWidth = (w+7)>>3

    b = 0
    for j in range(h):
        for i in range(w):
            if i%8==0:
                b = buf[j*byteWidth + (i>>3)]
                ## print(hex(b))
            else:
                b = b<<1

            if b & 0x80:
                print("#", end="")
            else:
                print(".", end="")
        print("")

def test_putc():
    SDFont = sdfonts_py.SDFonts()
    SDFont.open('/sd/font/FONT.BIN')

    fontSizes = (8, 10, 12, 14, 16, 20, 24)
    utf16s = (u'0aAあアｱ亜/')

    y = 50
    for n, fontSize in enumerate(fontSizes):
        SDFont.setFontSize(fontSize)
        ## print("FontSize:%d" % SDFont.getFontSize())

        x = 0
        
        for utf16 in utf16s:
            print(utf16)
            b = SDFont.getFontData(utf16)
            print(SDFont.getWidth(), SDFont.getHeight(), len(b))
            putc(b, x=x, y=y, w=SDFont.getWidth(), h=SDFont.getHeight())
            x += SDFont.getWidth()

        y += SDFont.getHeight()


    SDFont.close()

btnAStr = u'あ'
                
def btnA_pressed():
    global btnAStr
    SDFont = sdfonts_py.SDFonts()
    SDFont.open('/sd/font/FONT.BIN')
    SDFont.setFontSize(16)

    ## Increment Nihongo
    x = 0
    y = 50
    for j in range(10):
        for i in range(10):
            b = SDFont.getFontData(btnAStr)
            putc(b, x=x, y=y, w=SDFont.getWidth(), h=SDFont.getHeight())
            x += SDFont.getWidth()
    
            btnAStr = chr(ord(btnAStr) + 1)
            if btnAStr == u'ン':
                btnAStr = u'亜'
            if btnAStr == u'鰐':
                bntAStr = u'あ'
        x = 0
        y += SDFont.getHeight()

    SDFont.close()

def btnB_pressed():
    test_putc()
    pass

def btnC_pressed():
    lcd.clear()


if __name__ == '__main__':

    lcd.print("Start,")
    uos.mountsd()

    buttonA.wasPressed(callback=btnA_pressed)
    buttonB.wasPressed(callback=btnB_pressed)
    buttonC.wasPressed(callback=btnC_pressed)

    ## test_putc()
    fontpath = '/sd/font/FONT.BIN'
    printKari(u"Aabcdefあいうえお"*4, fontpath,
        fontsize=16, rect=(0,60, 160, 180), fg=0xFFFFFF, bg=0x444444)

    lcd.print("End,")




