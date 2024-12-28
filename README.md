# SlashConverter - 自动将 Windows 路径中的反斜杠转换为正斜杠

**SlashConverter** 是一个简单的工具，用于将剪贴板中的文件路径中的反斜杠（`\`）转换为正斜杠（`/`）。该程序还会自动移除路径两端的双引号（`"`）。它非常适用于将 Windows 风格路径转换为 Unix 或跨平台兼容的路径格式。

## 特性
- **斜杠转换**：将 Windows 风格的反斜杠路径（如 `C:\Users\Username\Documents\file.txt`）转换为 Unix 风格的正斜杠路径（如 `C:/Users/Username/Documents/file.txt`）。
- **剪贴板支持**：程序会自动读取剪贴板中的路径并将转换后的路径重新放回剪贴板，简化操作。
- **双引号移除**：自动去除路径两端的双引号，确保路径格式清晰整洁。
- **无需编译**：您只需下载并运行程序，无需编译或配置任何环境。

## 如何使用
1. **下载程序**：
   - 从 [GitHub 页面](https://github.com/your-repo-path) 下载已编译好的可执行文件 `SlashConverter.exe`。

2. **运行程序**：
   - 下载并解压文件。
   - 直接运行 `SlashConverter.exe` 程序。
   - 程序会自动读取剪贴板中的路径，转换后将新的路径替换回剪贴板。

3. **剪贴板示例**：
   - 将 Windows 风格的文件路径（例如 `C:\Users\Username\Documents\File.txt`）复制到剪贴板。
   - 运行程序。
   - 程序会输出 `C:/Users/Username/Documents/File.txt` 并将转换后的路径重新放回剪贴板。

## 示例

### 输入（剪贴板）：
```
"C:\Users\JohnDoe\Documents\Project\file.txt"
```

### 输出（剪贴板）：
```
C:/Users/JohnDoe/Documents/Project/file.txt
```