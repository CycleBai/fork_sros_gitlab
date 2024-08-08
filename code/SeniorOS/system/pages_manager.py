# PagesManager
# Copyright (C) 2024 CycleBai
# 
# This code is offered under the following two licenses:
# 
# 1. **GNU General Public License (GNU GPL)**
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
# 2. **Commercial License**
#   - If you intend to use this code for commercial purposes or need to use 
#     it in a way that does not comply with the GNU GPL, please contact 
#     zeeker-dev@proton.me to obtain a commercial license.
#   - The fees and terms for the commercial license will be discussed and 
#     determined with CycleBai.
# 

import SeniorOS.system.log_manager as LogManager

Log = LogManager.Log

# 定义错误类

# class InternalPageError(Exception):
    # '''捕获的所有屏幕内部异常都会直接引起此异常'''
    # pass

#  class ScreenError(Exception):
    # pass

# class PageError(Exception):
    # Log.Error('PageError 在 PagesManager V2 版本被弃用，请注意更换相关逻辑。')

class Main:
    def __init__(self) -> None:
        pass

    @staticmethod
    def Import(moduleLoc: str, funcName: str) -> bool:
        '''
        动态引入页面并执行
        Parameters:
            moudleLoc: 如何导入此页面所在的模块
            funcName: 页面所对应的函数名称
        Returns:
            布尔值，表示是否执行成功（指无报错）
        示例:
        import SeniorOS.system.pages_manager as PagesManager
        PagesManager.Main.Import("...", "...")
        
        '''

        module = __import__(moduleLoc, fromlist=[funcName])
        func = getattr(module, funcName)
        try:
            func()
            return True
        except Exception as e:
            Log.Error('在执行 {} 中的 {} 时意外抛出异常: {}'.format(moduleLoc, funcName, e))
            # raise InternalPageError(f'在执行 {moduleLoc} 中的 {funcName} 时意外抛出异常: {e}')
            return False