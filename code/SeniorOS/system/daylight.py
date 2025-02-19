import SeniorOS.system.core as Core
import math
import gc
import time
from SeniorOS.system.devlib import *
import SeniorOS.system.log_manager as LogManager
import SeniorOS.system.pages_manager as PagesManager
import micropython
LogManager.Output("system/daylight.mpy", "INFO")

# 缓存时间相关的字符串
def UITime(pages=True):
    h = str(Core.GetTime.Hour())
    m = str(Core.GetTime.Min())
    return ('0' + str(h) if len(str(h)) == 1 else str(h)) + \
             (':' if pages else "") + \
            ('0' + str(m) if len(str(m)) == 1 else str(m))

def GetCharWidth(s):
    # 获取字符宽度的优化实现
    return oled.DispChar(s, 0, 0, Colormode.noshow)[0][0] + int(len(s)/2)

AutoCenter = lambda string: 64 - GetCharWidth(string) // 2
HomeTimeAutoCenter = AutoCenter
def Box(x1, y1, x2, y2, fill = False):
    UITools()
    if fill:
        oled.fill_rect(x1 + 1, y1 + 1, x2 - 2, y2 - 2, 0)
    oled.rect(x1, y1, x2, y2, 1)

def ProgressBoxMove(x,y,w,h,progress,step=8):
    #progress使用百分制%
    now=0
    OurUI=UI(oled)#我们的 UI (苏里苏气)
    for _ in range(step):
        OurUI.ProgressBar(x, y, w, h, ((w - 0) / (100 - 0)) * (now - 0) + 0)
        oled.show()
        now+=(progress-now)//2
        time.sleep_ms(25)
    del OurUI#苏联解体力(悲)
    del now;gc.collect()
class App:
    def Style1(appTitle:str, window = False):
        gc.collect()
        oled.fill(0)
        if window:
            Box(1, 1, 126, 62)
        UITools()
        Text(appTitle, 5, 0, 3, 1, 100)
        oled.DispChar(UITime(True), 93, 0, 1)

    def Style2(appTitle:str, window = False):
        gc.collect()
        oled.fill(0)
        if window:
            Box(1, 1, 126, 62)
        UITools()
        Text(appTitle, 5, 5, 3, 1, 90)

class Select:
    @staticmethod
    def Style1(dispContent:list, y:int, window:bool = False, appTitle = None):
        oled.fill(0)
        UITools()
        selectNum = 0
        if appTitle:
            if not window:
                App.Style1(appTitle)
            else:
                App.Style1(appTitle, True)
        elif window:
            Box(1,1,126,62)
        oled.show()
        while not button_a.is_pressed():
            oled.fill_rect(0, 20, 128, 45, 0)
            oled.DispChar(dispContent[selectNum], AutoCenter(dispContent[selectNum]), y, 1)
            oled.DispChar(Core.ListState(dispContent, selectNum), 105, 40, 1)
            oled.show()
            on_pressed = eval("[/GetButtonExpr('on')/]")
            py_pressed = eval("[/GetButtonExpr('py')/]")
            th_pressed = eval("[/GetButtonExpr('th')/]")
            if on_pressed:
                selectNum = min(selectNum + 1, len(dispContent) - 1)
            if py_pressed:
                selectNum = max(selectNum - 1, 0)
            if th_pressed:
                return selectNum
            time.sleep_ms(int(eval("[/Const('interval')/]")))
        return

    @staticmethod
    def Style2(dispContent:list, tip:list, y:int, window:bool = False, appTitle = None):
        oled.fill(0)
        UITools()
        selectNum = 0
        if appTitle:
            if not window:
                App.Style1(appTitle)
            else:
                App.Style1(appTitle, True)
        elif window:
            Box(1,1,126,62)
        oled.show()
        while not button_a.is_pressed():
            if window:
                oled.RoundRect(2, y - 18, 124, 55, 2, 1)
            oled.show()
            on_pressed = eval("[/GetButtonExpr('on')/]")
            py_pressed = eval("[/GetButtonExpr('py')/]")
            th_pressed = eval("[/GetButtonExpr('th')/]")
            if on_pressed:
                selectNum = min(selectNum + 1, len(dispContent) - 1)
            if py_pressed:
                selectNum = max(selectNum - 1, 0)
            if th_pressed:
                return selectNum
            time.sleep_ms(int(eval("[/Const('interval')/]")))
            Text(tip[selectNum], 5, y, 2)
            Text(dispContent[selectNum], 5, y + 27, 3)
            oled.DispChar(Core.ListState(dispContent, selectNum), 105, 45, 1)
            oled.show()

    @staticmethod
    def Style3():
        UITools()
        selectNum = 0
        while not button_a.is_pressed():
            if eval("[/GetButtonExpr('on')/]"):
                selectNum = 1
                return selectNum
            if eval("[/GetButtonExpr('py')/]"):
                selectNum = 0
                return selectNum
            time.sleep_ms(int(eval("[/Const('interval')/]")))

    @staticmethod        
    def Style4(dispContent:list, window:False, appTitle:str = False):
        lendispcontext = len(dispContent)
        maxdispcontextindex = lendispcontext - 1
        UITools()
        listNum = 0
        while True:
            oled.fill(0)
            if appTitle:
                App.Style1(appTitle,window)
            start = max(0, min(len(dispContent) - 3, listNum - 1))
            displayItems = dispContent[start:start + 3]
            for i, item in enumerate(displayItems):
                Text(item, 5, 16 * (i + 1), 2, showMode=1)
            if len(displayItems) > 0:
                oled.fill_rect(5, 16 + 16 * (listNum - start), GetCharWidth(displayItems[listNum - start]), 16, 1)
                Text(displayItems[listNum - start], 5, 16 + 16 * (listNum - start), 2, showMode = 2)
            if window:
                Box(1, 1, 126, 62)
            oled.show()
            while not button_a.is_pressed():
                if eval("[/GetButtonExpr('on')/]"):
                    if listNum < maxdispcontextindex:
                        VastSea.SelsetBoxMove(5, 16+16*(listNum-start),displayItems[listNum - start],
                                              5,16+16*(listNum-start+1),displayItems[listNum - start+1],
                                              MODE="fill_rect")
                        listNum += 1
                        break
                elif eval("[/GetButtonExpr('py')/]"):
                    if listNum > 0:
                        VastSea.SelsetBoxMove(5,16+16*(listNum-start),displayItems[listNum - start],
                                              5,16+16*(listNum-start-1),displayItems[listNum - start-1],
                                              MODE="fill_rect")
                        listNum -= 1
                        break
                elif eval("[/GetButtonExpr('th')/]"):
                    return listNum
                elif button_a.is_pressed():return None

ListOptions = Select.Style4

class VastSea:
    @staticmethod   
    def Switch():
        while not button_a.is_pressed():
            oled.fill(0)
            UITools()
            App.Style2(eval("[/Language('动效开关')/]"))
            time.sleep_ms(5)
            get = int(Core.Data.Get("text", "VastSeaSwitch"))
            oled.DispChar([eval("[/Language('关闭')/]"), eval("[/Language('开启')/]")][get], 5, 18, 1)
            oled.show()
            get = Select.Style3()
            Core.Data.Write("text", 'VastSeaSwitch', str(get))
        return
    def SpeedSet():
        presuppose = {
            0:"100",
            1:"200",
            2:"300",
        }
        while not button_a.is_pressed():
            options = Select.Style4(["高效", "优雅", "柔和"], False, "动画速率")
            if options != None:
                VastSea.Transition()
                Core.Data.Write("text", "VastSeaSpeed", presuppose[options])
                PagesManager.Main.Import('SeniorOS.system.pages', 'Message', True, "设置成功\n{}".format(["故事半古之人，功必倍之", "用心聆听，深深呼吸", "松风吹解带，山月照弹琴"][options]))
                VastSea.Transition(False)

        else:
            VastSea.Transition(False)
    @staticmethod
    def SelsetBoxMove(x,y,char,ToX,ToY,NewChar,MODE="rect"):
        sx=x;sy=y
        ToWidth = GetCharWidth(NewChar)
        if ToWidth > 0:
            NowW=GetCharWidth(char)
            if MODE == "rect":
                for i in range(7):
                    oled.DispChar(char,sx,sy)
                    oled.DispChar(NewChar,ToX,ToY)
                    oled.rect(x,y,NowW,16,1)
                    oled.show()
                    oled.rect(x,y,NowW,16,1)
                    NowW+=(ToWidth-NowW)//2
                    x+=(ToX-x)//2
                    y+=(ToY-y)//2
                return
            else:
                for i in range(7):
                    oled.DispChar(char,sx,sy)
                    oled.fill_rect(x,y,NowW,16,1)
                    oled.DispChar(NewChar,ToX,ToY,2)
                    oled.show()
                    oled.fill_rect(x,y,NowW,16,0)
                    NowW+=(ToWidth-NowW)//2
                    x+=(ToX-x)//2
                    y+=(ToY-y)//2
                return
    @staticmethod   
    def Off():
        oled.fill(0)
        oled.show()
        time.sleep_ms(int(eval("[/Const('interval')/]")))
        return
    @staticmethod   
    def Transition(mode:bool = True):
        if int(Core.Data.Get("text", "VastSeaSwitch")) == 1:
            if mode:
                for i in range(13):
                    times = i**2
                    oled.vline(times, 0, 64, 1)
                    oled.vline(times+1, 0, 64, 0)
                    oled.fill_rect(0, 0, times, 64, 0)
                    oled.show()
            else:
                for i in range(13):
                    times = 13 - i
                    times_squared = times ** 2
                    oled.fill_rect(0, 0, 128, 64, 0)
                    oled.vline(times_squared, 0, 64, 1)
                    oled.vline(times_squared + 1, 0, 64, 0)
                    oled.show()
                oled.fill_rect(0, 0, 128, 64, 0)
                oled.show()
        else:
            VastSea.Off()
        
    
    class SeniorMove:
        @staticmethod
        def LoadText(text,x,y):
            gc.collect()
            total=x+140
            for i in range(7):
                oled.DispChar(text,total,y)
                total=total-((7-i)**2)
                oled.show()
                oled.DispChar(text,total,y,2)
        @staticmethod
        def Box(text, x=0, y=0, h=16):
            speed = int(Core.Data.Get("text", "VastSeaSpeed"))
            w = GetCharWidth(text)
            target_w = 128
            target_h = 64
            remaining_steps = 12
            step_x_total = x
            step_y_total = y
            step_w_total = target_w - w
            step_h_total = target_h - h
            step_x = step_x_total / remaining_steps
            step_y = step_y_total / remaining_steps
            step_w = step_w_total / remaining_steps
            step_h = step_h_total / remaining_steps
            oled.fill_rect(x, y, w, h, 0)
            oled.DispChar(text, x, y)
            oled.rect(x, y, w, h, 1)
            oled.show()
            time.sleep_ms(100)
            for i in range(12):
                oled.fill_rect(x, y, w, h, 0)
                oled.rect(x, y, w, h, 1)
                oled.show()
                oled.rect(x, y, w, h, 0)
                x -= int(step_x)
                y -= int(step_y)
                w += int(step_w)
                h += int(step_h)
                remaining_steps -= 1
                if remaining_steps > 0:
                    step_x = (x / remaining_steps) if remaining_steps > 0 else 0
                    step_y = (y / remaining_steps) if remaining_steps > 0 else 0
                    step_w = ((target_w - w) / remaining_steps) if remaining_steps > 0 else 0
                    step_h = ((target_h - h) / remaining_steps) if remaining_steps > 0 else 0
            oled.fill(0)
            time.sleep_ms(100)

        def Text(text, startX, startY, endX, endY):
            speed = int(Core.Data.Get("text", "VastSeaSpeed"))
            if int(Core.Data.Get("text", "VastSeaSwitch")) == 1:
                elapsedTime = 0  # 已过去的时间
                timer = 10  # 定时器间隔（毫秒）
                oled.fill(0)
                while elapsedTime < speed:
                    elapsedTime += timer
                    t = elapsedTime / speed
                    factor = -(math.cos(math.pi * t) - 1) / 2
                    currentX= startX + (endX - startX) * factor
                    currentY = startY + (endY - startY) * factor
                    # 根据计算出的 current_x 和 current_y 更新位置
                    oled.fill(0)
                    oled.DispChar(text, int(currentX), int(currentY))
                    oled.show()
            else:
                VastSea.Off()

        def Line(startX, startY, startX2,startY2, endX, endY, endX2, endY2, fill:bool = True):
            speed = int(Core.Data.Get("text", "VastSeaSpeed"))
            if int(Core.Data.Get("text", "VastSeaSwitch")) == 1:
                elapsedTime = 0  # 已过去的时间
                timer = 10  # 定时器间隔（毫秒）
                while elapsedTime < speed:
                    elapsedTime += timer
                    t = elapsedTime / speed
                    factor = -(math.cos(math.pi * t) - 1) / 2
                    currentX = startX + (endX - startX) * factor
                    currentY = startY + (endY - startY) * factor
                    currentX2 = startX2 + (endX2 - startX2) * factor
                    currentY2 = startY2 + (endY2 - startY2) * factor
                    # 根据计算出的 currentX、currentY、currentX2 和 currentY2 更新线条的位置
                    if fill:
                        oled.fill(0)
                    else:
                        oled.fill_rect(startX, startY, 128, 3, 0)
                    oled.line(int(currentX), int(currentY), int(currentX2), int(currentY2), 1)
                    oled.show()
            else:
                VastSea.Off()

        def Bitmap(bitMap, startX, startY, endX, endY, h, w):
            speed = int(Core.Data.Get("text", "VastSeaSpeed"))
            if int(Core.Data.Get("text", "VastSeaSwitch")) == 1:
                elapsedTime = 0  # 已过去的时间
                timer = 10  # 定时器间隔（毫秒）
                while elapsedTime < speed:
                    elapsedTime += timer
                    t = elapsedTime / speed
                    factor = -(math.cos(math.pi * t) - 1) / 2
                    currentX= startX + (endX - startX) * factor
                    currentY = startY + (endY - startY) * factor
                    # 根据计算出的 current_x 和 current_y 更新位置
                    oled.fill(0)
                    oled.Bitmap(int(currentX), int(currentY), bitMap, w, h, 1)
                    oled.show()
            else:
                VastSea.Off()
            

def UITools():
    try:
        oled.invert(int(Core.Data.Get("text", "lightMode")))
        oled.contrast(int(Core.Data.Get("text", "luminance")))
    except:
        pass

def LightModeSet():
    mode = [eval("[/Language('关闭')/]"),
            eval("[/Language('开启')/]")]
    while not button_a.is_pressed():
        oled.fill(0)
        UITools()
        App.Style2(eval("[/Language('日光模式')/]"))
        time.sleep_ms(5)
        get = int(Core.Data.Get("text", "lightMode"))
        oled.DispChar(mode[get], 5, 18, 1)
        oled.show()
        get = Select.Style3()
        Core.Data.Write("text",'lightMode', str(get))

def LuminanceSet():
    luminance = int(Core.Data.Get("text", "luminance"))
    oled.contrast(luminance)
    UITools()
    while not button_a.is_pressed():
        oled.contrast(luminance)
        oled.fill(0)
        App.Style2(eval("[/Language('亮度调节')/]"))
        time.sleep_ms(5)
        oled.DispChar(eval("[/Language('当前值')/]") + str(luminance), 5, 18, 1)
        oled.show()
        if eval("[/GetButtonExpr('on')/]"):
            luminance = luminance + 5
            if luminance > 255:
                luminance = 255
            oled.contrast(luminance)
        if eval("[/GetButtonExpr('py')/]"):
            luminance = luminance - 5
            if luminance < 0:
                luminance = 0
            oled.contrast(luminance)
    oled.contrast(luminance)
    Core.Data.Write("text",'luminance',str(luminance))
    return luminance

def TouchPadValueSet():
    sensitivity = int(Core.Data.Get("text", "touchPadValue"))
    while not button_A.is_pressed():
        oled.fill(0)
        App.Style2(eval("[/Language('触摸键灵敏度')/]"))
        time.sleep_ms(5)
        oled.DispChar(eval("[/Language('当前值')/]") + str(sensitivity), 5, 18, 1)
        oled.show()
        if eval("[/GetButtonExpr('on')/]"):
            sensitivity = sensitivity + 5
            if sensitivity > 800:
                sensitivity = 800
            TouchPad.config(sensitivity)
        if eval("[/GetButtonExpr('py')/]"):
            sensitivity = sensitivity - 5
            if sensitivity < -100:
                sensitivity = -100
            TouchPad.config(sensitivity)
    TouchPad.config(sensitivity)
    Core.Data.Write("text",'luminance',str(sensitivity))
    return sensitivity

mode={0:Outmode.stop,1:Outmode.autoreturn,2:Outmode.ellipsis}
def Text(text, x, y, outMode, space = 1, maximum_x = 126, returnX = 5, returnAddy = 16, showMode = 1):
    oled.DispChar(text, x, y, showMode, mode.get(outMode), maximum_x, space, return_x = returnX, return_addy = returnAddy)
    return
