
# -*- coding: utf-8 -*-

class SDFonts:
    ## EXFONTNUM = 14 ## 登録フォント数
    FULL_OFST = 7 ## フォントサイズから全角フォント種類変換用オフセット値
    ## MAXFONTLEN = 72 ## 最大フォントバイトサイズ(=24x24フォント)
    ## MAXSIZETYPE = 7 ## フォントサイズの種類数

    ## フォントサイズ
    EXFONT = (
        8, ## 8ドット美咲フォント
        10, ## 10ドット nagaフォント
        12, ## 12ドット東雲フォント
        14, ## 14ドット東雲フォント
        16, ## 16ドット東雲フォント
        20, ## 20ドットJiskanフォント
        24 ## 24ドットXフォント
    )

    FONTFILE = "/sd/font/FONT.BIN" ## フォントファイル名
    ## FONTFILE = "FONT.BIN" ## フォントファイル名

    OFSET_IDXA = 0
    OFSET_DATA = 3
    OFSET_FNUM = 6
    OFSET_BNUM = 8
    OFSET_W = 9
    OFSET_H = 10
    RCDSIZ = 11

    ## フォント種別テーブル
    _finfo = (
        (0x00,0x00,0x00, 0x00,0x01,0x7E,  0x00,0xbf,  8,  4,  8) , ## 0:u_4x8a.hex
        (0x00,0x07,0x76, 0x00,0x09,0x76,  0x01,0x00, 10,  5, 10) , ## 1:u_5x10a.hex
        (0x00,0x13,0x76, 0x00,0x15,0x76,  0x01,0x00, 12,  6, 12) , ## 2:u_6x12a.hex
        (0x00,0x21,0x76, 0x00,0x23,0x30,  0x00,0xdd, 14,  7, 14) , ## 3:u_7x14a.hex
        (0x00,0x2F,0x46, 0x00,0x31,0x00,  0x00,0xdd, 16,  8, 16) , ## 4:u_8x16a.hex
        (0x00,0x3E,0xD0, 0x00,0x40,0x4C,  0x00,0xbe, 40, 10, 20) , ## 5:u_10x20a.hex
        (0x00,0x5D,0xFC, 0x00,0x5F,0xB6,  0x00,0xdd, 48, 12, 24) , ## 6:u_12x24a.hex
        (0x00,0x89,0x26, 0x00,0xBE,0xE4,  0x1a,0xdf,  8,  8,  8) , ## 7:u_8x8.hex
        (0x01,0x95,0xDC, 0x01,0xCB,0x96,  0x1a,0xdd, 20, 10, 10) , ## 8:u_10x10.hex
        (0x03,0xE4,0xDA, 0x04,0x1A,0x98,  0x1a,0xdf, 24, 12, 12) , ## 9:u_12x12.hex
        (0x06,0x9F,0x80, 0x06,0xD5,0x3E,  0x1a,0xdf, 28, 14, 14) , ## 10:u_14x14.hex
        (0x09,0xC5,0xA2, 0x09,0xFB,0x60,  0x1a,0xdf, 32, 16, 16) , ## 11:u_16x16.hex
        (0x0D,0x57,0x40, 0x0D,0x8C,0xFE,  0x1a,0xdf, 60, 20, 20) , ## 12:u_20x20.hex
        (0x13,0xD9,0x42, 0x14,0x0E,0xFC,  0x1a,0xdd, 72, 24, 24) , ## 13:u_24x24.hex
    )

    ## 半角カナ全角変換テーブル
    _hkremap = (
        0x02,0x0C,0x0D,0x01,0xFB,0xF2,0xA1,0xA3,0xA5,0xA7,0xA9,0xE3,0xE5,0xE7,0xC3,0xFD,
        0xA2,0xA4,0xA6,0xA8,0xAA,0xAB,0xAD,0xAF,0xB1,0xB3,0xB5,0xB7,0xB9,0xBB,0xBD,0xBF,
        0xC1,0xC4,0xC6,0xC8,0xCA,0xCB,0xCC,0xCD,0xCE,0xCF,0xD2,0xD5,0xD8,0xDB,0xDE,0xDF,
        0xE0,0xE1,0xE2,0xE4,0xE6,0xE8,0xE9,0xEA,0xEB,0xEC,0xED,0xEF,0xF3,0x9B,0x9C
    )

    ## 
    _fontSize = EXFONT[0]
    _fontNo = EXFONT[0]+FULL_OFST
    ## _code = 0

    _open_font = None

    def __init__(self):
        pass

    ## def init(self, cs): ## 初期化
    ##     pass

    ## def setLCDMode(self, flg): ## グラフィック液晶モードの設定
    ##     pass

    def setFontSizeAsIndex(self, sz):
        """
        利用サイズを番号で設定
        """
        self._fontSize = sz
        self._fontNo = sz+self.FULL_OFST

    def getFontSizeIndex(self):
        """
        現在利用フォントサイズの番号取得      
        """
        return self._fontSize

    def setFontSize(self, sz):
        """
        利用サイズの設定
        """
        n = 0
        for num, s in enumerate(self.EXFONT):
            if s <= sz:
                n = num
            
        self.setFontSizeAsIndex(n)

    def getFontSize(self):
        """
        現在利用フォントサイズの取得      
        """
        return self.getHeight()

    def getFontDataUTF8(self, utf8):
        """
        指定したUTF8コードに該当するフォントデータの取得
        """
        utf16 = self.charUTF8toUTF16(utf8)
        return self.getFontData(utf16)
        

    def getFontData(self, utf16):
        """
        指定したUTF16コードに該当するフォントデータの取得
        """
        flgZenkaku = True
        utf16 = ord(utf16)

        ## 文字コードの変更(＼￠￡￢)
        if utf16 == 0xFF3C: utf16 = 0x5C
        elif utf16 == 0xFFE0: utf16 = 0xA2
        elif utf16 == 0xFFE1: utf16 = 0xA3
        elif utf16 == 0xFFE2: utf16 = 0xAC


        ## 文字コードから全角、半角を判定する
        if utf16 < 0x100:
            if utf16 in (
                0x5C, 0xA2, 0xA3, 0xA7,
                0xA8, 0xAC, 0xB0, 0xB1,
                0xB4, 0xB6, 0xD7, 0xF7,
            ):
                flgZenkaku = True
            else:
                flgZenkaku = False
        else:
            ## 半角カナは全角カナに置き換える
            if self._isHkana(utf16):
                utf16 = self._hkana2kana(utf16)

        ## フォント種別の設定
        if flgZenkaku:
            self._setFontNo(self.getFontSizeIndex() + self.FULL_OFST)
        else:
            self._setFontNo(self.getFontSizeIndex())

        ## self._code = utf16
        return self._getFontDataByUTF16(utf16)


    def getRowLength(self):
        """
        1行のバイト数
        """
        return (self._finfo[self._fontNo][self.OFSET_W] + 7)>>3

    def getWidth(self):
        """
         現在利用フォントの幅の取得
        """
        return self._finfo[self._fontNo][self.OFSET_W]

    def getHeight(self):
        """
         現在利用フォントの高さの取得
        """
        return self._finfo[self._fontNo][self.OFSET_H]

    def getLength(self):
        """
         現在利用フォントのデータサイズ
        """
        return self._finfo[self._fontNo][self.OFSET_BNUM]

    def open(self, font_path = None):
        """
         フォントファイルのオープン
        """
        if font_path is None:
            font_path = self.FONTFILE
        self._open_font = open(font_path, "rb")

    def close(self): ## フォントファイルのクローズ
        self._open_font.close()
        self._open_font = None

    ## def getCode(self):
    ##    """
    ##    直前に処理した文字コード
    ##    """
    ##   return _code
   
    def charUTF8toUTF16(self, utf8):
        """
        UTF8文字(1～3バイト)をUTF16に変換する
        """
        return utf8.decode('utf-8')

    ## def Utf8ToUtf16(self, pUTF16, pUTF8):
    ##    """
    ##    UTF8文字列をUTF16文字列に変換す
    ##    """
    ##     pass

    ## private:
    def _setFontNo(self, fno):
        """
        利用フォント種類の設定 fno : フォント種別番号 (0-13)
        """
        self._fontNo = fno

    def _getFontNo(self):
        """
        現在の利用フォント種類の取得
        """
        return self._fontNo

    def _read_code(self, pos):
        """
        ROM上検索テーブルのフォントコードを取得する
        """
        addr = self._cnvAddres(self.OFSET_IDXA, self._fontNo) + pos+pos
        rcv = self._fontfile_read(addr, 2)
        if rcv==None:
            return 0xFFFF
        return (rcv[0]<<8) + rcv[1]

    def _findcode(self, ucode):
        """
        UTF16コードに該当するテーブル上のフォントコードを取得する
        """
        t_p = 0  ##　検索範囲上限
        e_p = (self._finfo[self._fontNo][self.OFSET_FNUM]<<8) + self._finfo[self._fontNo][self.OFSET_FNUM+1] -1 ##  検索範囲下限
        pos = 0
        d = 0
        flg_stop = 0
       
        while True:
            pos = t_p + ((e_p - t_p+1)>>1)
            d = self._read_code(pos)
            ##DBG print(self._fontNo, t_p, e_p, pos, ucode, d)

            if d == 0xFFFF:
                return -1;  
       	
            if d == ucode: ## 等しい
                flg_stop = 1
                break
            elif ucode > d: ## 大きい
                t_p = pos + 1;
                if t_p > e_p:
                    break
            else: ## 小さい
                e_p = pos -1;
                if e_p < t_p:
                    break
      
        if flg_stop==0:
            return -1
        return pos

    def _hkana2kana(self, ucode):
        """
        半角カナ全角変換 JISX0208 -> UTF16の不整合対応
        """
        if self._isHkana(ucode):
            return self._hkremap[ucode-0xFF61] + 0x3000
        return ucode

    ## def _hkana2uhkana(self, ucode):
    ##     """
    ##     UTF半角カナ半角utf16コード変換 JISX0208 -> UTF16の不整合対応
    ##     """
    ##     pass

    def _getFontDataByUTF8(self, utf8):
        """
         種類に該当するフォントデータの取得
        """
        utf16 = self.charUTF8toUTF16(utf8)
        return self._getFontDataByUTF16(utf16)

    def _getFontDataByUTF16(self, utf16):
        """
         種類に該当するフォントデータの取得
        """
        if type(utf16) is not int:
            utf16 = ord(utf16)

        code = self._findcode(utf16)
        ##DBG print("No: %d, Code is %d" % (self._fontNo, code))
        if 0 > code:
            return None ## 該当するフォントが存在しない
    
        bnum = self._finfo[self._fontNo][self.OFSET_BNUM]
        addr = self._cnvAddres(self.OFSET_DATA, self._fontNo) + code * bnum
        return self._fontfile_read(addr, bnum)

    def _isHkana(self, ucode):
        """
        半角カナ判定
        """
        return (ucode >=0xFF61 and ucode <= 0xFF9F)

    def _cnvAddres(self, pos, ln):  
        """
        get Address
        """
        addr = (self._finfo[ln][pos]<<16)+ (self._finfo[ln][pos+1]<<8) + (self._finfo[ln][pos+2])
        return addr

    def _fontfile_read(self, pos, sz) :
        """
        read font bytearray
        """
        b = None
        f = self._open_font
        v = f.seek(pos, 0)
        b = f.read(sz)
        b = bytearray(b) ## for Python2.7
    
        if sz!=len(b):
            b = None

        return b

