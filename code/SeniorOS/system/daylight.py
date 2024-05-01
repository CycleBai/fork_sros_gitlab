import SeniorOS.system.core as Core
import ntptime
import network
import time
import ustruct
import framebuf
from mpython import wifi,oled
from mpython import touchPad_P,touchPad_Y,touchPad_H,touchPad_O,touchPad_N,touchPad_T
from mpython import button_a,button_b
import gc
import time,uos

def UITime(pages:True):
    h=str(Core.GetTime.Hour())
    m=str(Core.GetTime.Min())
    if pages:
       return ('0' + h if len(h)==1 else h) + ':' + ('0' + m if len(m)==1 else m)
    else:
        return ('0' + h if len(h)==1 else h) + ('0' + m if len(m)==1 else m)


def consani(consani_done_x, consani_done_y, consani_done_wide, consani_done_height, consani_start_x, consani_start_y, consani_start_wide, consani_start_height):
    try:
      oled.invert(int(Core.Data.Get('light')))
    except:
        pass

    try:
      consani_done_wait = 3
      oled.fill(0)
      for count in range(7):
          oled.RoundRect(consani_done_x, consani_done_y, consani_done_wide, consani_done_height, 2, 1)
          oled.fill(0)
          consani_done_x = (consani_done_x - consani_start_x) // 2
          consani_done_y = (consani_done_y - consani_start_y) // 2
          consani_done_wide = (consani_start_wide + consani_done_wide) // 2
          consani_done_height = (consani_start_height + consani_done_height) // 2
          oled.RoundRect(consani_done_x, consani_done_y, consani_done_wide, consani_done_height, 2, 1)
          oled.show()
    except:
        oled.DispChar(' :( 我们遇到了一些问题，将在 3 秒后返回', 5, 25, 1, True)
        oled.show()
        return
    if touchPad_P.is_pressed() and touchPad_Y.is_pressed():
        return
    time.sleep_ms(consani_done_wait)
    consani_done_wait = consani_done_wait + 3

def ConsaniApp(consani_done_x, consani_done_y, consani_done_wide, consani_done_height, consani_start_x, consani_start_y, consani_start_wide, consani_start_height, logo, logo_x):
    try:
      oled.invert(int(Core.Data.Get('light')))
    except:
        pass

    try:
      consani_done_wait = 3
      oled.fill(0)
      for count in range(7):
          oled.RoundRect(consani_done_x, consani_done_y, consani_done_wide, consani_done_height, 2, 1)
          oled.fill(0)
          consani_done_x = (consani_done_x - consani_start_x) // 2
          consani_done_y = (consani_done_y - consani_start_y) // 2
          consani_done_wide = (consani_start_wide + consani_done_wide) // 2
          consani_done_height = (consani_start_height + consani_done_height) // 2
          logo_x = (logo_x + 52) //2
          oled.RoundRect(consani_done_x, consani_done_y, consani_done_wide, consani_done_height, 2, 1)
          oled.Bitmap(logo_x, 20, logo, 25, 25, 1)
          oled.show()
    except:
        oled.DispChar(' :( 我们遇到了一些问题，将在 3 秒后返回', 5, 25, 1, True)
        oled.show()
        return
    if touchPad_P.is_pressed() and touchPad_Y.is_pressed():
        return
    time.sleep_ms(consani_done_wait)
    consani_done_wait = consani_done_wait + 3

def GetCharWidth(s):
    strWidth = 0
    for c in s:
        charData = oled.f.GetCharacterData(c)
        if charData is None:continue
        strWidth += ustruct.unpack('HH', charData[:4])[0] + 1
    return strWidth
AutoCenter=lambda string:64-GetCharWidth(string)//2
HomeTimeAutoCenter=lambda string:64-GetCharWidth(string)//2-22

def app(appTitle:str):
    oled.fill(0)
    try:
      oled.invert(int(Core.Data.Get('light')))
    except:
        pass
    oled.fill_rect(1, 0, 126, 16, 1)
    oled.DispChar(appTitle, 5, 0, 2)
    oled.DispChar(UITime(True), 93, 0, 2)
    oled.hline(50, 62, 30, 1)

def DisplayFont(_font, _str, _x, _y, _wrap, _z=0):
    _start = _x
    for _c in _str:
        _d = _font.get_ch(_c)
        if _wrap and _x > 128 - _d[2]: _x = _start; _y += _d[1]
        if _c == '1' and _z > 0: oled.fill_rect(_x, _y, _d[2], _d[1], 0)
        oled.blit(framebuf.FrameBuffer(bytearray(_d[0]), _d[2], _d[1],framebuf.MONO_HLSB), (_x+int(_d[2]/_z)) if _c=='1' and _z>0 else _x, _y)
        _x += _d[2]

def Select(dispContent:list,appTitle:str):
    selectNum = 0
    while not button_a.is_pressed():
        oled.rect(2, 4, 124, 16, 1)
        app(appTitle)
        oled.RoundRect(2, 2, 124, 60, 2, 1)
        oled.DispChar(dispContent[selectNum], 5, 20, 1)
        oled.DispChar(''.join([str(selectNum + 1),'/',str(len(dispContent))]), 105, 45, 1)
        oled.show()
        if touchPad_O.is_pressed() and touchPad_N.is_pressed():
            selectNum = selectNum + 1
            if selectNum + 1 > len(dispContent):
                selectNum = len(dispContent) - 1
        if touchPad_P.is_pressed() and touchPad_Y.is_pressed():
            selectNum = selectNum - 1
            if selectNum < 0:
                selectNum = 0
        if touchPad_T.is_pressed() and touchPad_H.is_pressed():
            return selectNum
    return

def message(dispContent:list):
    oled.rect(2, 2, 124, 16, 1)
    for i in range(len(dispContent)):
        oled.DispChar(dispContent[i], 5, 5+16*i, 1)
    # 然而这里实测只能放两排（
    oled.Dispchar("PY-明白", 42, 45)
    oled.show()
    while not button_a.is_pressed():
        if touchPad_P.is_pressed():
            return

def Tti(mode=True):
    """if mode is True then Draw the Left Transition animation
Else Draw the Left Transition animation
time=380ms
"""
    ckt=128
    ckr=0
    if mode:
        for i in range(10):
            ckt=ckt/2
            ckr=ckr + ckt
            oled.fill_rect(0, 0,round(ckr), 64, 0)
            oled.show()
            #time.sleep_ms(10)
    else:
        for i in range(10):
            ckt=ckt/2
            oled.fill_rect(int(ckt), 0, 128, 64, 0)
            oled.show()
            #time.sleep_ms(10)