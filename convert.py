import pyperclip  # 导入 pyperclip 库，用于操作剪贴板
import time  # 导入 time 库，用于设置延时


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


def main():
    """
    主函数：从剪贴板获取文件路径，转换格式后复制回剪贴板并打印结果。
    """
    # 从剪贴板获取路径内容
    path = pyperclip.paste()

    # 调用 convert_path 函数转换路径格式
    converted_path = convert_path(path)

    # 将转换后的路径复制到剪贴板
    pyperclip.copy(converted_path)

    # 打印原始路径和转换后的路径
    print(f"原始路径: {path}")
    print(f"转换后的路径: {converted_path}")
    print("转换后的路径已复制到剪贴板！")

    # 稍作延时，确保用户看到输出
    time.sleep(1)


if __name__ == "__main__":
    # 程序入口，执行 main 函数
    main()
