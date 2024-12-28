#include <stdio.h>
#include <string.h>
#include <windows.h>

void convertPath(char *path) {
    // 移除两端的双引号
    int len = strlen(path);
    if (path[0] == '"') {
        memmove(path, path + 1, len - 1); // 移除起始双引号
        path[len - 2] = '\0'; // 移除结尾双引号
    }

    // 替换反斜杠为正斜杠
    for (int i = 0; path[i] != '\0'; i++) {
        if (path[i] == '\\') {
            path[i] = '/';
        }
    }
}

int main() {
    // 打开剪贴板
    if (!OpenClipboard(NULL)) {
        printf("无法打开剪贴板\n");
        return 1;
    }

    // 获取剪贴板中的文本
    HANDLE hData = GetClipboardData(CF_TEXT);
    if (hData == NULL) {
        printf("剪贴板中没有文本数据\n");
        CloseClipboard();
        return 1;
    }

    // 将剪贴板中的数据指向一个字符指针
    char *path = (char *) GlobalLock(hData);
    if (path == NULL) {
        printf("无法访问剪贴板数据\n");
        CloseClipboard();
        return 1;
    }

    // 输出原始路径
    printf("原始路径: %s\n", path);

    // 转换路径
    convertPath(path);

    // 输出转换后的路径
    printf("转换后的路径: %s\n", path);

    // 清空剪贴板并将转换后的路径放回剪贴板
    EmptyClipboard(); // 清空剪贴板

    size_t len = strlen(path) + 1;
    HANDLE hMem = GlobalAlloc(GMEM_MOVEABLE, len);
    if (hMem == NULL) {
        printf("无法分配内存\n");
        CloseClipboard();
        return 1;
    }

    // 锁定内存并复制转换后的路径到内存
    char *clipMem = (char *) GlobalLock(hMem);
    strcpy(clipMem, path);
    GlobalUnlock(hMem);

    // 将转换后的文本设置到剪贴板
    SetClipboardData(CF_TEXT, hMem);

    // 关闭剪贴板
    CloseClipboard();

    printf("转换后的路径已复制到剪贴板！\n");

    // 模拟等待 3 秒
    Sleep(1000);

    return 0;
}
