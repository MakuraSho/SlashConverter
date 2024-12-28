#include <stdio.h>
#include <string.h>
#include <windows.h>

void convertPath(char *path) {
    // �Ƴ����˵�˫����
    int len = strlen(path);
    if (path[0] == '"') {
        memmove(path, path + 1, len - 1); // �Ƴ���ʼ˫����
        path[len - 2] = '\0'; // �Ƴ���β˫����
    }

    // �滻��б��Ϊ��б��
    for (int i = 0; path[i] != '\0'; i++) {
        if (path[i] == '\\') {
            path[i] = '/';
        }
    }
}

int main() {
    // �򿪼�����
    if (!OpenClipboard(NULL)) {
        printf("�޷��򿪼�����\n");
        return 1;
    }

    // ��ȡ�������е��ı�
    HANDLE hData = GetClipboardData(CF_TEXT);
    if (hData == NULL) {
        printf("��������û���ı�����\n");
        CloseClipboard();
        return 1;
    }

    // ���������е�����ָ��һ���ַ�ָ��
    char *path = (char *) GlobalLock(hData);
    if (path == NULL) {
        printf("�޷����ʼ���������\n");
        CloseClipboard();
        return 1;
    }

    // ���ԭʼ·��
    printf("ԭʼ·��: %s\n", path);

    // ת��·��
    convertPath(path);

    // ���ת�����·��
    printf("ת�����·��: %s\n", path);

    // ��ռ����岢��ת�����·���Żؼ�����
    EmptyClipboard(); // ��ռ�����

    size_t len = strlen(path) + 1;
    HANDLE hMem = GlobalAlloc(GMEM_MOVEABLE, len);
    if (hMem == NULL) {
        printf("�޷������ڴ�\n");
        CloseClipboard();
        return 1;
    }

    // �����ڴ沢����ת�����·�����ڴ�
    char *clipMem = (char *) GlobalLock(hMem);
    strcpy(clipMem, path);
    GlobalUnlock(hMem);

    // ��ת������ı����õ�������
    SetClipboardData(CF_TEXT, hMem);

    // �رռ�����
    CloseClipboard();

    printf("ת�����·���Ѹ��Ƶ������壡\n");

    // ģ��ȴ� 3 ��
    Sleep(1000);

    return 0;
}
