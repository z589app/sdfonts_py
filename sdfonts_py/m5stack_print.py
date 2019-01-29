
import sdfonts_py
from m5stack import lcd

class M5StackPrint:
    _font_path = None
    font_color = 0xFFFFFF
    back_color = 0x000000
    font_size = 16
    rect = (0,0,320,240)

    append = False ##TODO


    def __init__(self, font_path,
        font_color=0xFFFFFF, back_color=0x000000,
        font_size=16, rect=(0,0,320,240),
        append=False):

        self._font_path = font_path
        self.font_color = font_color
        self.back_color = back_color
        self.font_size = font_size
        self.rect = rect
        self.append = append

    def print(self, strings):
        if type(strings) is not str:
            strings = str(strings)

        self._print_core(strings,
            font_path=self._font_path, font_size=self.font_size, 
            rect=self.rect, fg=self.font_color, bg=self.back_color,
            append=self.append)

    def prinln(self, strings):
        if type(strings) is not str:
            strings = str(strings)
        strings += "\n"

        self._print_core(strings,
            font_path=self._font_path, font_size=self.font_size, 
            rect=self.rect, fg=self.font_color, bg=self.back_color,
            append=self.append)

    _last_xy = None

    def _print_core(self, strings, font_path, font_size=8,
            rect=(0, 0, 320, 240), fg=0xFFFFFF, bg=0x000000,
            append=False):
        SDFont = sdfonts_py.SDFonts()
        SDFont.open(font_path)
        SDFont.setFontSize(font_size)
    
        start_x, start_y = rect[0:2]
        end_x = rect[0] + rect[2]
        end_y = rect[1] + rect[3]
        if append:
            if self._last_xy is None: ##TODO
                self.clear() ##TODO
            x, y = self._last_xy
        else:
            x, y = start_x, start_y
            ## Fill backgound
            lcd.rect(rect[0], rect[1],
                rect[2], rect[3],
                color=bg, fillcolor=bg)
            ## lcd.rect(x=rect[0], y=rect[1],
            ##     width=rect[2], height=rect[3],
            ##     color=bg, fillcolor=bg)
            bg = None
    
        for s in strings:

            ## NextLine
            if s == "\n":
                x = start_x
                y += font_size
                continue

            b = SDFont.getFontData(s)
            if b is None:
                continue

            w = SDFont.getWidth()
            h = SDFont.getHeight()

            self._putc(b, x=x, y=y, fg=fg, bg=bg, w=w, h=h)

            x += w
            if x > end_x:
                x = start_x
                y += h
                if y > end_y:
                    y = start_y
                    if append:
                        self.clear() ## go top ##TODO
                    else:
                        break ## over


        self._last_xy = (x, y)
        SDFont.close()

    ## print 1 Char to M5Stack
    def _putc(self, buf, x=0, y=0, fg=0xFFFFFF, bg=0x000000, w=8, h=8):
        if type(buf) is not bytearray:
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

    def clear(self): ##TODO
        self._last_xy = self.rect[0:2]
        lcd.rect(self.rect[0], self.rect[1],
            self.rect[2], self.rect[3],
            color=self.back_color, fillcolor=self.back_color)


