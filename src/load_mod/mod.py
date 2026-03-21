import json
import logging
import os
from typing import *

import keyboard
from colorama import *

from clear_screen import *
from gui import *

init(autoreset=True)


def join_path(files, root, pack_list) -> Optional[list]:
    """
    遍历文件列表，查找名为 'pack.json' 的文件，并将其完整路径添加到 pack_list 中。

    参数:
        files (list): 当前目录下的文件名列表。
        root (str): 当前目录的根路径。
        pack_list (list): 用于存储找到的 'pack.json' 文件完整路径的列表。

    返回:
        Optional[list]: 如果找到 'pack.json' 文件，返回更新后的 pack_list；否则返回 None。
    """
    for file in files:
        if file == 'pack.json':
            # 获取完整的文件路径并添加到列表
            full_path = os.path.join(root, file)
            pack_list.append(full_path)
            return pack_list  # 找到后立即返回
    return None  # 遍历完所有文件仍未找到时返回 None


def mod_pack_path(mod_folder_path: str) -> List[str]:
    """
    遍历指定的 mod 文件夹，查找所有名为 'pack.json' 的文件，并返回它们的完整路径列表。

    参数:
        mod_folder_path (str): mod 文件夹的根路径。

    返回:
        List[str]: 包含所有找到的 'pack.json' 文件完整路径的列表。
    """
    pack_list: list = []

    # 遍历 mod 文件夹及其子目录
    for root, dirs, files in os.walk(mod_folder_path):
        pack = join_path(files, root, pack_list)
        if pack is None:
            continue
        pack_list = pack

    return pack_list


def load_pack(pack_path: str, all_color: dict) -> Optional[Tuple[str, str, str]]:
    """
    加载指定路径的mod配置文件，并解析其中的标题、描述和文件信息。

    参数:
        pack_path (str): mod配置文件的路径。
        all_color (dict): 颜色映射字典，用于根据配置中的颜色值获取对应的颜色代码。

    返回:
        Tuple[str, str, str]: 包含三个元素的元组：
            - 格式化后的标题（带颜色）。
            - mod的描述信息。
            - mod对应的文件名。

    异常处理:
        如果在读取或解析过程中发生异常，会记录错误日志并提示用户，然后退出程序。
    """
    try:
        with open(pack_path, 'r', encoding='utf-8') as f:
            pack: dict = json.load(f)
            title: dict = pack['title']
            title_text: str = title['text']
            title_color: str = all_color.get(title.get('color'), Style.RESET_ALL)
            title: str = f'{title_color}{title_text}{Style.RESET_ALL}'
            describe_: str = pack.get('describe', '无描述')
            file: str = pack['file']
            return title, describe_, file

    except Exception as e:
        clear()
        logging.error(f'Mod load error: {e}')
        print(f'{Fore.RED}一个mod加载失败： {e}')
        keyboard.read_key()
        clear_button()
        clear()
        return None


def mod_menu(pack_list: list, all_color: dict) -> Tuple[int, list, list]:
    """
    构建mod选择菜单，展示所有可用的mod及其描述信息。

    参数:
        pack_list (list): 包含所有mod配置文件路径的列表。
        all_color (dict): 颜色映射字典，用于格式化标题颜色。

    返回:
        Tuple[int, list, list]: 包含三个元素的元组：
            - 菜单项总数（包括“退出”选项）。
            - 格式化后的菜单项列表。
            - 每个mod对应的文件名列表。
    """
    menu: list = []
    mod_id: list = []
    for i in pack_list:
        title, describe_, file = load_pack(i, all_color)
        menu.append(f'{title}\n描述：{describe_}\n{Fore.LIGHTBLACK_EX}文件名地址： mod/{file}')
        mod_id.append(file)
    menu.append(f'{Fore.RED}退出')
    quit_: int = len(menu)
    # print(menu)
    # __import__('time').sleep(1)
    return quit_, menu, mod_id


def load_mod_level(mod_path: str, path: str, all_color: dict) -> Optional[Tuple[list, list]]:
    """
    加载并处理指定路径下的关卡和文件数据，返回格式化后的关卡菜单和文件列表。

    参数:
        mod_path (str): Mod的根目录路径。
        path (str): 相对于Mod根目录的子路径。
        all_color (dict): 颜色映射字典，用于为关卡文本添加颜色。

    返回:
        Optional[Tuple[list, list]]:
            - 第一个元素是格式化后的关卡菜单列表（带颜色）。
            - 第二个元素是加载的文件列表。
            - 如果发生异常则返回None。
    """
    level_menu: list = []
    try:
        # 尝试读取关卡配置文件和文件配置文件
        with open(f'{mod_path}{path}/level.json', 'r', encoding='utf-8') as f:
            level: list = json.load(f)
        with open(f'{mod_path}{path}/file.json', 'r', encoding='utf-8') as f:
            file: list = json.load(f)

        # 遍历关卡数据，根据颜色映射为每个关卡文本添加颜色，并构建关卡菜单
        for i in level:
            color: int = all_color.get(i.get('color'), Style.RESET_ALL)
            text: str = f'{color}{i.get("text")}{Style.RESET_ALL}'
            level_menu.append(text)

        level_menu.append(f'{Fore.RED}退出')

        # 返回格式化后的关卡菜单和文件列表
        return level_menu, file
    except Exception as e:
        # 发生异常时清屏并记录错误日志，提示用户后等待按键继续
        clear()
        logging.error(f'Mod load error: {e}')
        print(f'{Fore.RED}一个mod加载失败： {e}')
        keyboard.read_key()
        clear_button()
        clear()
        return None


def mod_menu_loop(quit_: int, menu: list, mod_id: list) -> Optional[str]:
    """
    进入mod选择循环，允许用户通过菜单选择并加载特定的mod。

    参数:
        quit_ (int): 表示“退出”选项在菜单中的索引位置。
        menu (list): 格式化后的菜单项列表。
        mod_id (list): 每个mod对应的文件名列表。

    功能说明:
        循环显示菜单供用户选择。如果用户选择某个mod，则尝试加载该mod；
        如果用户选择“退出”，则结束循环。
        若加载mod时出现异常，会记录错误日志并提示用户后退出程序。
    """
    while True:
        choose = menu_loop(menu)

        if choose + 1 == quit_:
            break

        try:
            print(mod_id[choose])
            return mod_id[choose]
        except Exception as e:
            clear()
            logging.error(f'Mod load error: {e}')
            print(f'{Fore.RED}一个mod加载失败： {e}')
            keyboard.read_key()
            clear_button()
            clear()
            return None
