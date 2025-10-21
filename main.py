import pyperclip  # 导入 pyperclip 库,用于操作剪贴板
import time  # 导入 time 库,用于设置延时
import ctypes
import threading
import json
import os
import sys
from pystray import Icon, MenuItem, Menu
from PIL import Image
import tkinter as tk
from tkinter import messagebox

# === 解决DPI模糊问题 ===
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Windows 10+
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()  # 旧版本兼容
    except Exception:
        pass


# === 全局变量 ===
clipboard_monitor_running = False
clipboard_thread = None
check_interval = 0.5  # 默认检测间隔为0.5秒


# 获取资源文件路径（兼容PyInstaller打包）
def get_resource_path(relative_path):
    """获取资源文件的绝对路径，兼容开发环境和PyInstaller打包后的环境"""
    try:
        # PyInstaller创建临时文件夹，并将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except AttributeError:
        # 如果不是打包后的环境，使用当前文件所在目录
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


# 获取配置文件路径（保存在用户的AppData目录）
def get_config_path():
    """获取配置文件的完整路径"""
    # 获取用户AppData目录
    appdata = os.getenv("APPDATA")
    if appdata:
        # 在AppData中创建应用专用文件夹
        app_dir = os.path.join(appdata, "SlashConverter")
        # 确保目录存在
        os.makedirs(app_dir, exist_ok=True)
        return os.path.join(app_dir, "config.json")
    else:
        # 备用方案：使用当前目录
        return "config.json"


CONFIG_FILE = get_config_path()  # 配置文件路径


# === 配置文件管理 ===
def load_config():
    """从配置文件加载设置"""
    global check_interval
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                check_interval = config.get("check_interval", 0.5)
                print(f"[配置加载] 从配置文件加载检测间隔：{check_interval} 秒")
        else:
            print(f"[配置加载] 配置文件不存在，使用默认值：{check_interval} 秒")
    except Exception as e:
        print(f"[配置加载] 加载配置文件失败：{e}，使用默认值")


def save_config():
    """保存设置到配置文件"""
    try:
        config = {"check_interval": check_interval, "version": "1.0"}
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print(f"[配置保存] 配置已保存到文件：{CONFIG_FILE}")
        return True
    except Exception as e:
        print(f"[配置保存] 保存配置文件失败：{e}")
        return False


def is_windows_path(text):
    """
    判断文本是否为 Windows 路径格式（包含反斜杠）。

    参数:
    text (str): 要检查的文本

    返回:
    bool: 如果是 Windows 路径返回 True，否则返回 False
    """
    # 检查是否包含反斜杠，并且符合路径特征
    # 例如: C:\path\to\file 或 \\network\path 或相对路径 folder\file
    if not text or not isinstance(text, str):
        return False

    # 如果包含反斜杠，认为是 Windows 路径
    if "\\" in text:
        return True

    return False


def convert_path(path):
    """
    将文件路径中的反斜杠 ('\\') 转换为正斜杠 ('/')，并去除路径中的双引号（如果有的话）。

    参数:
    path (str): 输入的文件路径

    返回:
    str: 转换后的文件路径
    """
    path = path.strip('"')  # 去掉路径两端的双引号
    converted_path = path.replace("\\", "/")  # 将反斜杠替换为正斜杠
    return converted_path


def monitor_clipboard():
    """
    持续监控剪贴板变化，自动转换 Windows 路径格式。
    """
    global clipboard_monitor_running, check_interval

    print("=" * 50)
    print("剪贴板路径转换器已启动!")
    print("程序将在后台运行，自动监测剪贴板变化")
    print("当检测到 Windows 路径时，将自动转换为正斜杠格式")
    print(f"当前检测间隔：{check_interval} 秒")
    print("=" * 50)
    print()

    last_clipboard = ""  # 记录上次剪贴板内容
    clipboard_monitor_running = True

    try:
        while clipboard_monitor_running:
            try:
                # 获取当前剪贴板内容
                current_clipboard = pyperclip.paste()

                # 如果剪贴板内容发生变化且不为空
                if current_clipboard != last_clipboard and current_clipboard:
                    # 检查是否为 Windows 路径
                    if is_windows_path(current_clipboard):
                        # 转换路径
                        converted_path = convert_path(current_clipboard)

                        # 将转换后的路径复制到剪贴板
                        pyperclip.copy(converted_path)

                        # 打印转换信息
                        print(f"[{time.strftime('%H:%M:%S')}] 检测到新的 Windows 路径")
                        print(f"原始路径: {current_clipboard}")
                        print(f"转换后: {converted_path}")
                        print("-" * 50)

                        # 更新上次剪贴板内容为转换后的内容
                        last_clipboard = converted_path
                    else:
                        # 不是路径，只更新记录
                        last_clipboard = current_clipboard

                # 短暂延时，避免占用过多 CPU 资源
                time.sleep(check_interval)

            except Exception as e:
                print(f"处理剪贴板时出错: {e}")
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n程序已退出")
    finally:
        clipboard_monitor_running = False


# === 弹出设置窗口 ===
def open_settings_window():
    """打开首选项设置窗口"""
    global check_interval

    def save_settings():
        try:
            # 获取输入的检测间隔值
            new_interval = float(interval_entry.get())

            # 验证输入范围（0.1秒到10秒）
            if new_interval < 0.1:
                messagebox.showwarning("输入错误", "检测间隔不能小于0.1秒")
                return
            if new_interval > 10:
                messagebox.showwarning("输入错误", "检测间隔不能大于10秒")
                return

            # 保存设置
            global check_interval
            check_interval = new_interval

            # 保存到配置文件
            if save_config():
                messagebox.showinfo(
                    "保存成功",
                    f"检测间隔已设置为：{check_interval} 秒\n\n设置已保存，将在下次检测循环时生效",
                )
                print(f"[设置更新] 剪贴板检测间隔已更新为：{check_interval} 秒")
            else:
                messagebox.showwarning(
                    "保存警告",
                    f"检测间隔已设置为：{check_interval} 秒\n\n但保存配置文件失败，重启后将恢复默认值",
                )
            window.destroy()

        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字（0.1-10）")

    # 创建新窗口（独立线程中运行）
    window = tk.Tk()
    window.title("首选项设置 - SlashConverter")
    window.geometry("800x400")
    window.resizable(False, False)

    # 设置窗口图标（.ico 文件）
    try:
        icon_path = get_resource_path("makura.ico")
        window.iconbitmap(icon_path)
    except Exception as e:
        print(f"未找到图标文件：{e}")

    # 创建主框架（居中）
    main_frame = tk.Frame(window)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # 标题
    tk.Label(
        main_frame, text="剪贴板检测设置", font=("Microsoft YaHei", 12, "bold")
    ).pack(pady=(0, 20))

    # 检测间隔设置框架（居中）
    interval_frame = tk.Frame(main_frame)
    interval_frame.pack(pady=10)

    tk.Label(
        interval_frame, text="检测间隔（秒）：", font=("Microsoft YaHei", 10)
    ).pack(side=tk.LEFT)

    interval_entry = tk.Entry(interval_frame, width=10, font=("Microsoft YaHei", 10))
    interval_entry.pack(side=tk.LEFT, padx=10)
    interval_entry.insert(0, str(check_interval))  # 显示当前值

    # 说明文字（居中）
    tk.Label(
        main_frame, text="(范围：0.1 - 10 秒)", font=("Microsoft YaHei", 9), fg="gray"
    ).pack()

    tk.Label(
        main_frame,
        text="较小的值响应更快，但会占用更多CPU资源",
        font=("Microsoft YaHei", 9),
        fg="gray",
    ).pack(pady=(5, 20))

    # 保存按钮（居中）
    tk.Button(
        main_frame,
        text="保存设置",
        width=15,
        height=2,
        command=save_settings,
        font=("Microsoft YaHei", 10),
    ).pack(pady=10)

    window.mainloop()


# === 托盘菜单回调 ===
def on_preferences(icon, item):
    """打开首选项设置窗口"""
    # 为避免 tkinter 与 pystray 线程冲突，用线程启动
    threading.Thread(target=open_settings_window, daemon=True).start()


def on_exit(icon, item):
    """退出程序"""
    global clipboard_monitor_running
    clipboard_monitor_running = False
    icon.stop()


def main():
    """
    主函数：启动剪贴板监控和系统托盘图标。
    """
    global clipboard_thread

    # 加载配置文件
    load_config()

    # 在后台线程中启动剪贴板监控
    clipboard_thread = threading.Thread(target=monitor_clipboard, daemon=True)
    clipboard_thread.start()

    # 创建并运行系统托盘图标
    try:
        icon_path = get_resource_path("makura.ico")
        icon = Icon(
            "SlashConverter",
            Image.open(icon_path),
            "SlashConverter - 路径转换器",
            menu=Menu(
                MenuItem("首选项设置", on_preferences), MenuItem("退出", on_exit)
            ),
        )
        icon.run()
    except FileNotFoundError as e:
        print(f"错误：未找到 makura.ico 图标文件 - {e}")
        print("程序将继续运行，但没有系统托盘图标")
        # 如果找不到图标文件，直接运行监控
        clipboard_thread.join()
    except Exception as e:
        print(f"错误：加载图标时出错 - {e}")
        print("程序将继续运行，但没有系统托盘图标")
        clipboard_thread.join()


if __name__ == "__main__":
    # 程序入口，执行 main 函数
    main()
