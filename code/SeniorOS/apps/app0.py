from SeniorOS.system.devlib import *
import SeniorOS.system.core as Core
import SeniorOS.system.daylight as DayLight
import time

list = [eval("[/Language('网络与时间')/]"), 
        eval("[/Language('界面与动效')/]"), 
        eval("[/Language('缓存与运存')/]"), 
        eval("[/Language('系统与设备')/]")]
DayLight.UITools()
import SeniorOS.system.pages as Pages
import SeniorOS.style.port as Style
time.sleep_ms(5)

Settings0 = {
    0: Pages.WifiPages,
    1: Pages.Time,
    2: Pages.Choosewifi,
    3: Pages.ConnectWiFiMode
}

Settings1 = {
    0: DayLight.LightModeSet,
    1: DayLight.LuminanceSet,
    2: DayLight.VastSea.Switch,
    3: DayLight.VastSea.SpeedSet,
    4: Style.homeStyleSet,
    5: Pages.HomeomePlugInSet,
    6: DayLight.TouchPadValueSet,
}

Settings2 = {
    0: Pages.Collect,
    1: Pages.Collect,
}

Settings3 = {
    0: Pages.About,
    1: Pages.About,
}

def Main():
    while not button_a.value()==0:
        settingsNum = DayLight.Select.Style4(list, False, "设置")
        if eval("[/GetButtonExpr('th')/]"):
            if settingsNum != None:
                DayLight.VastSea.Transition()
                options = eval('DayLight.Select.Style4(list{}, False, "选择")'.format(str(settingsNum)),
                            {'list0':['重连网络', '同步时间', '新建网络配置','网络连接方式'],
                            'list1':['日光模式','亮度调节','动效开关', '动画速率', '桌面风格', '桌面快速启动', '触摸键灵敏度'],
                            'list2':['释放内存', '内存信息'],
                            'list3':['设备信息', '系统更新'],
                            'DayLight':DayLight})
                if options != None:
                    DayLight.VastSea.Transition()
                    eval("{}.get({})()".format("Settings" + str(settingsNum), options))
                    DayLight.VastSea.Transition(False)

                else:
                    DayLight.VastSea.Transition(False)