import sys
import time
from typing import *

from colorama import *

from clear_screen import *
from game import *
from gui import *
from load_asset import *
from load_config import *
from load_log import *
from load_mod import *
from show_keyboard import *
import json
import importlib.util
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


# 初始化 colorama 库，用于在终端中显示彩色文本
init(autoreset=True)

# 定义日志配置文件路径和资源配置文件路径
LOG_CONFIG_PATH: Final[str] = '../config/log_config.json'
ASSET_CONFIG_PATH: Final[str] = '../config/asset_config.json'
COLOR_CONFIG_PATH: Final[str] = '../config/color.json'
MOD_CONFIG_PATH: Final[str] = '../config/mod_config.json'
PLUGIN_CONFIG_PATH: Final[str] = '../config/plugin.json'

# 加载日志配置并初始化日志系统
log_config = load_config_log(LOG_CONFIG_PATH)
load_log(log_config)

# 加载资源配置，获取 logo 和 title 文件路径
asset_config = load_config_asset(ASSET_CONFIG_PATH)
logo_path: str = asset_config[0]
title_path: str = asset_config[1]
map_path: str = asset_config[2]
menu_path: str = asset_config[3]

# 加载模组配置
mod_path = load_config_mod(MOD_CONFIG_PATH)

# 加载颜色配置
color_dict: dict = read_color(COLOR_CONFIG_PATH)

ALL_COLORS: Final[dict] = {
    'black': Fore.BLACK,
    'red': Fore.RED,
    'green': Fore.GREEN,
    'yellow': Fore.YELLOW,
    'blue': Fore.BLUE,
    'purple': Fore.MAGENTA,
    'aqua': Fore.CYAN,
    'white': Fore.WHITE,
    'reset': Fore.RESET,
    'gray': Fore.LIGHTBLACK_EX,
    'light_red': Fore.LIGHTRED_EX,
    'light_green': Fore.LIGHTGREEN_EX,
    'light_yellow': Fore.LIGHTYELLOW_EX,
    'light_blue': Fore.LIGHTBLUE_EX,
    'light_purple': Fore.LIGHTMAGENTA_EX,
    'light_aqua': Fore.LIGHTCYAN_EX,
    'light_white': Fore.LIGHTWHITE_EX
}

# 从文件中加载 logo 和 title 文本内容
LOGO: Final[str] = load_asset_text(logo_path)
TITLE: Final[str] = load_asset_text(title_path)

START_GAME: Final[int] = 0
MOD: Final[int] = 1
ABOUT: Final[int] = 2
QUIT: Final[int] = 3
KEYBOARD: Final[int] = 4

def load_plugins():
    plugins = []
    try:
        with open(PLUGIN_CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            plugin_path = data.get('path', '../plugin')
            plugin_files = data.get('files', [])
            if plugin_files == []:
                pass
            else:
                plugins = []
                for file in plugin_files:
                    module_name = file[:-4]  # 去掉文件扩展名
                    plugins.append(importlib.import_module("plugin." + module_name))
                    # module_path = f'{plugin_path}/{file}'
                    # spec = importlib.util.spec_from_file_location(module_name, module_path)
                    # if spec and spec.loader:
                    #     module = importlib.util.module_from_spec(spec)
                    #     sys.modules[module_name] = module
                    #     spec.loader.exec_module(module)
                    #     plugins.append(module)
                    for plugin in plugins:
                        if hasattr(plugin, 'register'):
                            plugin.register()
                        for func in plugin.__all__:
                            if hasattr(plugin, func):
                                # function = globals().get(func)
                                function = getattr(plugin, func)
                                if "@loadStart" in function.__doc__:
                                    function()
    # except Exception as e:
    #     print(f'加载插件时发生错误: {e}')
    #     time.sleep(5)
    finally:
        pass
    


def main() -> None:
    # 清屏并显示标题动画
    clear()
    for i in TITLE.split('\n'):
        print(i)
        time.sleep(0.15)
    time.sleep(1)

    # 清屏并显示Logo动画
    clear()
    for i in LOGO.split('\n'):
        print(i)
        time.sleep(0.15)
    time.sleep(1)

    clear()
    load_plugins()
    # 进入主菜单循环
    while True:
        # 读取主菜单配置文件
        menu_ = read_menu(f'{menu_path}main_menu.json')
        # 显示菜单并获取用户选择
        choose = menu_loop(menu_)

        # 根据用户选择执行相应操作
        if choose == START_GAME:
            start_game(menu_path, map_path, color_dict, ALL_COLORS)
        elif choose == MOD:
            mods = mod_pack_path(mod_path)
            quit_, menu, mod_id = mod_menu(mods, ALL_COLORS)
            path = mod_menu_loop(quit_, menu, mod_id)
            level_menu(mod_path, path, path, color_dict, ALL_COLORS)
        elif choose == ABOUT:
            print_about()
        elif choose == QUIT:
            # 清空屏幕并退出程序
            clear()
            sys.exit(0)
        elif choose == KEYBOARD:
            print_keyboard()


if __name__ == '__main__':
    main()
