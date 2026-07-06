# TactiReader

> 专为长篇 PDF、工程手册、标准文档设计的键盘优先双栏阅读器。
>
> 原项目地址：[github.com/p3psi-boo/tacti-reader](https://github.com/p3psi-boo/tacti-reader)

## 快速开始

```bash
pip install PyMuPDF PyQt5 markdown
python tactireader.py your_file.pdf
```

## 核心快捷键

| 按键 | 功能 |
|------|------|
| `A` / `D` | 上页 / 下页 |
| `←` / `→` | 快退 / 快进 N 页 |
| `1` ~ `9` | **非批注模式**：设置翻页倍数 N（1~9 页）<br>**批注模式**：切换当前批注工具的 9 种颜色 |
| `F` | 全文搜索 |
| `G` | 跳转指定页码 |
| `Ctrl + G` | 标定物理页码偏移 |
| `Space` | 跳转到最远页（阅读过的最大页码） |
| `Ctrl + Space` | 将当前页设为最远页 |
| `Ctrl + A` | 单步回退 |
| `Q` ~ `P` | 跳转到对应书签 |
| `Ctrl + Q` ~ `P` | 设置书签 |
| `Alt + Q` ~ `P` | 清除书签 |
| `C` | 切换左窗格锁定/跟随 |
| `Z` | 单页 / 双页切换 |
| `N` | 显示/隐藏目录面板 |
| `X` | 重置当前窗格视图 |
| `~` | 顺时针旋转 90° |
| `B` / `H` / `V` | 画笔 / 高亮 / 文字批注 |
| `ESC` | 退出批注模式 |
| `Ctrl + Z` | 撤销批注 |
| `J` | 文字选取模式 |
| `S` | 立即保存状态 |
| `F11` | 全屏 |

批注三种工具（画笔、高亮、文字）均提供 9 色可选，默认均为**纯正红**，文字批注默认字号 25pt。

**界面特性**

- **颜色模式**：视图菜单支持切换颜色模式。
- **目录交互**：全新目录面板，适合层级深、条目多的 PDF，自动展开并记忆选中状态。

## 更多文档

- [中文使用指南](docs/help_zh.md)
- [English User Guide](docs/help.md)
- [关于 / About](docs/about_zh.md)

## 打包

```powershell
pip install pyinstaller
pyinstaller --windowed --name "TactiReader" --icon=tactireader.ico ^
  --add-data "tactireader.png;." ^
  --add-data "docs/help.md;docs" ^
  --add-data "docs/about.md;docs" ^
  --add-data "docs/help_zh.md;docs" ^
  --add-data "docs/about_zh.md;docs" ^
  tactireader.py
```

macOS / Linux 将 `;` 改为 `:`。
