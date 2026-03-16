import json
import logging
import sys

import keyboard
from colorama import *

from clear_screen import *

init(autoreset=True)


def read_menu(path: str) -> list:
    """
    从指定路径加载菜单数据并返回。

    参数:
        path (str): 菜单文件的路径，文件应为JSON格式。

    返回:
        list: 解析后的菜单数据列表。如果加载失败，则程序会退出。

    异常处理:
        如果在读取或解析文件时发生异常，会记录错误日志，打印错误信息，
        并等待用户按键后退出程序。
    """
    try:
        # 尝试以UTF-8编码打开文件并加载JSON数据
        with open(path, 'r', encoding='utf-8') as f:
            menu: list = json.load(f)
            return menu

    except Exception as e:
        # 清屏并记录错误日志
        clear()
        logging.error(f'Menu load error: {e}')
        # 打印红色错误信息提示用户
        print(Fore.RED + f'菜单读取时发生错误： {e}')
        # 等待用户按键（抑制按键输出）后退出程序
        keyboard.read_key()
        clear_button()
        sys.exit(0)


def load_menu(menu: list, choose: int) -> str:
    """
    加载并显示菜单选项，高亮当前选中的选项，并等待用户按键输入。

    参数:
        menu (list): 菜单选项列表，每个元素为一个字符串。
        choose (int): 当前选中的菜单项索引（从0开始）。

    返回:
        str: 用户按下的键值（通过keyboard.read_key获取）。
    """
    # 构建菜单内容为一个字符串列表
    menu_lines = []
    # 如果当前索引等于choose，则使用白色背景和黑色字体高亮显示
    for i in range(len(menu)):
        if i == choose:
            menu_lines.append(f'{Back.WHITE}{Fore.BLACK}{i + 1}. {menu[i]}{Style.RESET_ALL}')
        else:
            menu_lines.append(f'{i + 1}. {menu[i]}{Style.RESET_ALL}')

    # 一次性输出整个菜单
    print('\n'.join(menu_lines))

    # 等待用户按键输入，并返回按键值
    move: str = keyboard.read_key()
    clear_button()
    return move


def menu_loop(menu: list) -> int:
    """
    循环显示菜单并处理用户输入，直到用户选择一个选项为止。

    参数:
        menu (list): 菜单项列表，每个元素代表一个菜单项。

    返回:
        int: 用户选择的菜单项索引。
    """

    def trigger(choose_: int) -> int:
        """
        处理选择索引越界的情况，确保索引在有效范围内循环。

        参数:
            choose_ (int): 当前选择的索引。

        返回:
            int: 处理后的有效索引。
        """
        if choose_ < 0:
            choose_: int = len(menu) - 1
        elif choose_ >= len(menu):
            choose_: int = 0
        return choose_

    choose: int = 0

    while True:
        # 清屏并加载菜单显示
        clear()
        move = load_menu(menu, choose)

        # 处理用户输入：向上移动选择
        if move in ['w', 'up']:
            choose -= 1
            choose = trigger(choose)

        # 处理用户输入：向下移动选择
        elif move in ['s', 'down']:
            choose += 1
            choose = trigger(choose)

        # 处理用户输入：确认选择
        elif move in ['space', 'enter']:
            return choose
