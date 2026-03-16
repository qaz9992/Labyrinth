import json
import logging
import sys
from typing import *

import keyboard
from colorama import *

from clear_screen import *

init(autoreset=True)


def find_player(map_: list) -> Tuple[int, int]:
    """
    在给定的地图中查找玩家的位置。

    参数:
        map_ (list): 一个二维列表，表示游戏地图。每个元素代表地图上的一个位置，
                     其中 'I' 表示玩家的位置。

    返回:
        Tuple[int, int]: 玩家在地图中的坐标 (行索引, 列索引)。

    异常:
        ValueError: 如果地图中没有找到玩家 ('I')，则抛出此异常。
    """
    # 遍历地图的每一行和每一列
    for i in range(len(map_)):
        for j in range(len(map_[i])):
            # 如果找到玩家标记 'I'，则返回其坐标
            if map_[i][j] == 'S':
                return i, j
    # 如果遍历完整张地图仍未找到玩家，则抛出异常
    raise ValueError('Player not found')


def read_map(path) -> dict:
    """
    从指定路径读取地图文件并解析为字典格式。

    参数:
        path (str): 地图文件的路径，文件应为JSON格式。

    返回:
        dict: 包含地图数据和玩家位置的字典，结构如下：
            {
                'map': list,          # 地图数据，二维列表形式
                'player_y': int,      # 玩家在地图中的行坐标
                'player_x': int       # 玩家在地图中的列坐标
            }

    异常处理:
        如果读取或解析过程中发生异常，会记录错误日志并打印红色错误信息，
        然后终止程序运行。
    """
    try:
        # 打开并读取地图文件，解析为JSON格式
        with open(path, 'r') as f:
            map_: list = json.load(f)
            # 查找玩家在地图中的初始位置
            player_location: Tuple[int, int] = find_player(map_)
            player_y: int = player_location[0]
            player_x: int = player_location[1]

        # 构造包含地图数据和玩家位置的字典
        map_data: dict = {
            'map': map_,
            'player_y': player_y,
            'player_x': player_x,
        }
        return map_data

    except Exception as e:
        # 清屏并记录错误日志
        clear()
        logging.error(f'Map load error: {e}')
        # 打印红色错误信息并退出程序
        print(f'{Fore.RED}地图解析时错误： {e}')
        keyboard.read_key()
        clear_button()
        sys.exit()


def print_map(map_: list, color_dict: dict, all_color: dict) -> None:
    """
    打印一个二维地图，每个单元格根据颜色字典进行着色。

    参数:
        map_ (list): 一个二维列表，表示地图的每一行和每一列。
        color_dict (dict): 一部字典，键为地图中的单元格值，值为对应的颜色名称。
        all_color (dict): 一部字典，键为颜色名称，值为对应的ANSI转义序列，用于在终端中显示颜色。

    返回值:
        None: 该函数不返回任何值，直接打印结果到标准输出。
    """
    # 初始化一个空列表，用于存储每一行的着色字符串
    lines = []

    # 遍历地图的每一行
    for row in map_:
        # 将当前行的每个单元格根据颜色字典进行着色，并拼接成一行字符串
        line = ''.join(
            f"{all_color[color_dict.get(cell, 'reset')]}{cell}"
            for cell in row
        )
        # 将处理好的行字符串添加到lines列表中
        lines.append(line)

    # print('# - 墙壁\nX/@ - 回到起点\n> - 向右传送\n< - 向左传送\n^ - 向上传送\nv - 向下传送\nE - 终点')
    # 将所有行用换行符连接，并打印到标准输出
    print('\n'.join(lines))


def map_loop(map_data: dict, color_dict: dict, all_color: dict) -> str:
    """
    主循环函数，用于处理地图中的玩家移动和交互逻辑。

    参数:
        map_data (dict): 包含地图信息的字典，包括：
            - 'map': 二维列表，表示游戏地图。
            - 'player_y': 玩家当前所在的行索引。
            - 'player_x': 玩家当前所在的列索引。

    返回:
        str: 返回游戏状态，可能的值包括：
            - 'win': 玩家成功到达终点。
            - 'reload': 玩家选择重新开始游戏。
            - 'back': 玩家选择退出游戏。
    """
    map_ = map_data['map']
    player_y: int = map_data['player_y']
    player_x: int = map_data['player_x']
    start_y: int = player_y
    start_x: int = player_x
    flag = True

    while flag:
        # 备份当前位置的字符，以便后续恢复
        original_char = map_[player_y][player_x]

        # 将玩家当前位置标记为 'I'
        map_[player_y][player_x] = 'I'

        # 清屏并打印当前地图状态
        clear()
        print_map(map_, color_dict, all_color)

        # 恢复地图中原有字符
        map_[player_y][player_x] = original_char

        # 获取玩家输入的按键
        move = keyboard.read_key()
        clear_button()

        # 根据按键计算新的坐标
        if move in ['w', 'up']:
            new_y, new_x = player_y - 1, player_x
        elif move in ['s', 'down']:
            new_y, new_x = player_y + 1, player_x
        elif move in ['a', 'left']:
            new_y, new_x = player_y, player_x - 1
        elif move in ['d', 'right']:
            new_y, new_x = player_y, player_x + 1
        elif move == 'r':
            flag = False
            continue
        elif move == 'esc':
            break
        else:
            continue

        # 判断新位置是否合法，并根据地图元素更新玩家位置
        if map_[new_y][new_x] == '#':
            continue
        elif map_[new_y][new_x] in ['@', 'X']:
            player_y, player_x = start_y, start_x
        elif map_[new_y][new_x] == '>':
            player_y, player_x = new_y, new_x + 2
        elif map_[new_y][new_x] == '<':
            player_y, player_x = new_y, new_x - 2
        elif map_[new_y][new_x] == '^':
            player_y, player_x = new_y - 2, new_x
        elif map_[new_y][new_x] == 'v':
            player_y, player_x = new_y + 2, new_x
        elif map_[new_y][new_x] == 'E':
            return 'win'
        else:
            player_y, player_x = new_y, new_x

    # 根据循环结束条件返回对应的游戏状态
    return 'reload' if not flag else 'back'
