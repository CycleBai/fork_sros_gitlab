from mpython import wifi,oled
from mpython import touchPad_P,touchPad_Y,touchPad_H,touchPad_O,touchPad_N,touchPad_T
from mpython import button_a,button_b
from SeniorOS.apps.port import *
from SeniorOS.style.lib import *
import SeniorOS.system.core as Core
import time

#-----------------------------------------------------------------------------------#
def Style1(appTitle):
    oled.DispChar(appTitle, 5, 0, 1)
    oled.DispChar(UITime(True), 93, 0, 1)
#-----------------------------------------------------------------------------------#
def Style2(appTitle):
    pass
#-----------------------------------------------------------------------------------#
def Style3(appTitle):
    oled.DispChar(appTitle, 5, 0, 1)
#-----------------------------------------------------------------------------------#
def Style4(appTitle):
    oled.DispChar(appTitle, AutoCenter(appTitle), 0, 1)