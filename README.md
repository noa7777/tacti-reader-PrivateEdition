# TactiReader

> 专为长篇 PDF、工程手册、标准文档设计的键盘优先双栏阅读器。
>
> 原项目地址：[github.com/googleismylove](https://github.com/googleismylove)

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
| `1` ~ `9` | 设置翻页倍数 N |
| `F` | 全文搜索 |
| `G` | 跳转指定页码 |
| `Ctrl + G` | 标定物理页码偏移 |
| `Space` | 跳转到 Home（最远阅读页） |
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
| `Ctrl + Z` | 撤销批注 |
| `J` | 文字选取模式 |
| `S` | 立即保存状态 |
| `F11` | 全屏 |

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
