# -*- coding: utf-8 -*-

from context import sdfonts_py


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
    SDFont.open('../FONT.BIN')
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

