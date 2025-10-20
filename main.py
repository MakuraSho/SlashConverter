import pyperclip  # 导入 pyperclip 库，用于操作剪贴板
import time  # 导入 time 库，用于设置延时
import re  # 导入 re 库，用于正则表达式匹配


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
    if '\\' in text:
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
    print("=" * 50)
    print("剪贴板路径转换器已启动!")
    print("程序将在后台运行，自动监测剪贴板变化")
    print("当检测到 Windows 路径时，将自动转换为正斜杠格式")
    print("按 Ctrl+C 可以退出程序")
    print("=" * 50)
    print()
    
    last_clipboard = ""  # 记录上次剪贴板内容
    
    try:
        while True:
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
                time.sleep(0.5)
                
            except Exception as e:
                print(f"处理剪贴板时出错: {e}")
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n程序已退出")


def main():
    """
    主函数：启动剪贴板监控。
    """
    monitor_clipboard()


if __name__ == "__main__":
    # 程序入口，执行 main 函数
    main()
