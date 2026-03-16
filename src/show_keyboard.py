from clear_screen import *
import keyboard

def print_keyboard() -> None:
    """
    打印游戏的键位说明，帮助玩家了解游戏操作方式。
    """
    clear()
    print('键位说明：')
    print('W / Up Arrow: 向上移动')
    print('S / Down Arrow: 向下移动')
    print('A / Left Arrow: 向左移动')
    print('D / Right Arrow: 向右移动')
    print('R: 重新开始当前关卡')
    print('ESC: 退出当前关卡')

    print('地图: \n# - 墙壁\nX/@ - 回到起点\n> - 向右传送\n< - 向左传送\n^ - 向上传送\nv - 向下传送\nE - 终点')


    print('\n按任意键返回主菜单...')
    keyboard.read_key()
    clear_button()