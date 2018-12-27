# -*- coding: utf-8 -*-

from __future__ import print_function
import sdfonts_py

def printKari(strings, fontpath,
    fontsize=8, rect=(0, 0, 320, 240), fg=0xFFFFFF, bg=0x000000):

    SDFont = sdfonts_py.SDFonts()
    SDFont.open(fontpath)
    SDFont.setFontSize(fontsize)

    start_x = rect[0]
    start_y = rect[1]
    end_x = rect[0] + rect[2]
    end_y = rect[1] + rect[3]
    x, y = start_x, start_y

    ## Fill backgound
    ##TMP lcd.rect(x=rect[0], y=rect[1], width=rect[2], height=rect[3], color=bg, fillcolor=bg)

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
        
def putc(buf, x=0, y=0, fg=0xFFFFFF, bg=0x000000, w=8, h=8): ## Dummy
    print(x, y, w, h)

## Kari, print to Terminal
def printTerm(buf, x=0, y=0, fg=0xFFFFFF, bg=0x444444, w=8, h=8):
    if type(buf) is not bytearray:
        print("printTerm(), Error")
        return

    byteWidth = (w+7)>>3
    print(w, h, byteWidth)

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


def test_printTerm():
    SDFont = sdfonts_py.SDFonts()
    SDFont.open('../../fontbin/FONT.BIN')
    SDFont.setFontSize(10)

    utf16s = (u'A\nあ亜イｲ/')
    ## utf16s = (u'A', u'あ', u'亜', u'イ', u'ｲ')

    for utf16 in utf16s:
        print(utf16)
        b = SDFont.getFontData(utf16)
        ## b = SDFont._getFontDataByUTF16(utf16)
        print(b)
        printTerm(b, w=SDFont.getWidth(), h=SDFont.getHeight())


    SDFont.close()

if __name__ == '__main__':
    
    test_printTerm()

    ## printKari(u"Aabcdefあいうえお"*4, '../../fontbin/FONT.BIN', fontsize=24)

