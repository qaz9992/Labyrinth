import winreg
import sys
import os

def register_custom_url_protocol():
    """
    自动注册 app:// 协议
    自动根据【相对路径】获取程序绝对路径
    """
    # ===================== 【只需填写相对路径】 =====================
    # 相对于当前 .py 文件所在文件夹 的 程序路径
    # 例子：如果 exe 和 py 在同一个文件夹 → 直接写文件名
    RELATIVE_APP_PATH = "labyrinth.exe"  # 👈 只改这里
    # =================================================================

    try:
        # ========== 核心：相对路径 → 自动转 绝对路径 ==========
        # 获取当前 Python 脚本所在的文件夹
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 拼接成完整绝对路径
        APP_PATH = os.path.join(current_dir, RELATIVE_APP_PATH)
        # 规范化路径（解决 / \ 混乱问题）
        APP_PATH = os.path.abspath(APP_PATH)

        print(f"📌 自动识别程序路径：{APP_PATH}")

        # 检查文件是否存在
        if not os.path.exists(APP_PATH):
            print(f"❌ 错误：文件不存在！")
            return

        # ===================== 注册到注册表 =====================
        # 1. 创建主协议项
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "app") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "URL:App Protocol")
            winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")

        # 2. 设置图标（可选）
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"app\DefaultIcon") as icon_key:
            winreg.SetValue(icon_key, "", winreg.REG_SZ, f'"{APP_PATH}",0')

        # 3. 设置启动命令（核心）
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"app\shell\open\command") as cmd_key:
            command_value = f'"{APP_PATH}" "%1"'
            winreg.SetValue(cmd_key, "", winreg.REG_SZ, command_value)

        print("\n✅ 注册成功！")
        print("👉 Win+R 输入 app://start 即可运行程序")

    except PermissionError:
        print("\n❌ 权限不足！请【右键 → 以管理员身份运行】此脚本")
    except Exception as e:
        print(f"\n❌ 注册失败：{e}")

if __name__ == "__main__":
    register_custom_url_protocol()