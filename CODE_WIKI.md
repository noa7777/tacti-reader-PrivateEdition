# TactiReader Code Wiki

> 版本：2.0 Tactical Complete Edition | 最后更新：2026-06-17

---

## 目录

1. [项目概述](#1-项目概述)
2. [项目架构](#2-项目架构)
3. [目录结构](#3-目录结构)
4. [模块详解](#4-模块详解)
   - 4.1 [入口模块](#41-入口模块)
   - 4.2 [核心常量模块 (constants)](#42-核心常量模块-constants)
   - 4.3 [配置管理模块 (config)](#43-配置管理模块-config)
   - 4.4 [工具函数模块 (utils)](#44-工具函数模块-utils)
   - 4.5 [主窗口与业务逻辑 (tactireader.py)](#45-主窗口与业务逻辑-tactireaderpy)
5. [关键类说明](#5-关键类说明)
   - 5.1 [TactiReader (QMainWindow)](#51-tactireader-qmainwindow)
   - 5.2 [TacticalPane (QLabel)](#52-tacticalpane-qlabel)
   - 5.3 [BookmarkButton (QLabel)](#53-bookmarkbutton-qlabel)
   - 5.4 [InlineTextEdit (QTextEdit)](#54-inlinetextedit-qtextedit)
   - 5.5 [SearchDialog (QDialog)](#55-searchdialog-qdialog)
   - 5.6 [LanguageSelectDialog (QDialog)](#56-languageselectdialog-qdialog)
   - 5.7 [MarkdownViewer (QDialog)](#57-markdownviewer-qdialog)
   - 5.8 [ConfigManager](#58-configmanager)
6. [核心数据结构](#6-核心数据结构)
7. [依赖关系](#7-依赖关系)
8. [项目运行方式](#8-项目运行方式)
9. [配置与数据持久化](#9-配置与数据持久化)
10. [国际化机制](#10-国际化机制)
11. [快捷键体系](#11-快捷键体系)
12. [已知架构问题与优化方向](#12-已知架构问题与优化方向)

---

## 1. 项目概述

**TactiReader（战术阅读器）** 是一款专为长篇 PDF、工程手册、标准文档、教材查阅设计的**键盘优先阅读器**。其核心目标是解决高频跳转、对照阅读、批注记录和跨章节关联的问题。

### 核心特性

| 特性 | 说明 |
|------|------|
| 双页对照阅读 | 左页可锁定为参考页，右页自由浏览 |
| 瞬时书签 (Q-P) | 键盘顶行十键盲操设/跳/删书签 |
| 逻辑页码校准 | 支持物理页码与逻辑页码偏移标定 |
| 全文搜索高亮 | 搜索结果自动在页面中高亮显示 |
| 批注系统 | 画笔、矩形高亮、文本批注三种模式 |
| 笔记本导出 | `.tactinote` 格式打包 PDF + 全部状态 |
| 多标签页 | 同时打开多个文档，标签页可拖拽排序 |
| 新窗口并行 | 右键标签页可在独立窗口中打开文档 |
| 国际化 | 支持英文/简体中文切换 |

---

## 2. 项目架构

### 架构总览

```
┌─────────────────────────────────────────────────────┐
│                    用户入口                           │
│  tactireader.py (CLI) / main.py (包模式)             │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              TactiReader (QMainWindow)               │
│  ┌──────────┐  ┌──────────────────────────────────┐ │
│  │ 书签/TOC  │  │         阅读区域 (QSplitter)      │ │
│  │ 面板      │  │  ┌──────────┐  ┌──────────┐     │ │
│  │ (左侧栏)  │  │  │ LeftPane │  │RightPane │     │ │
│  │           │  │  │TacticalPane│ │TacticalPane│   │ │
│  └──────────┘  │  └──────────┘  └──────────┘     │ │
│                └──────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────┐│
│  │  QTabBar (多文档标签栏，>1文档时显示)              ││
│  └──────────────────────────────────────────────────┘│
│  ┌──────────────────────────────────────────────────┐│
│  │  MenuBar │ StatusBar                             ││
│  └──────────────────────────────────────────────────┘│
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   ┌──────────┐ ┌──────────┐ ┌──────────┐
   │constants │ │  config  │ │  utils   │
   │ 常量定义  │ │ConfigMgr │ │ 工具函数  │
   └──────────┘ └──────────┘ └──────────┘
```

### 架构特点

- **单文件核心 + 模块化拆分**：核心业务逻辑（约 4500 行）集中在 `tactireader.py`，已拆分出 `constants`、`config`、`utils` 三个辅助模块
- **MVC 混合模式**：`TactiReader` 类同时承担 Controller 和 View 职责，`TacticalPane` 承担部分 View 和 Model 职责
- **事件驱动**：所有交互通过 PyQt5 信号/槽机制和 `keyPressEvent` 统一处理

---

## 3. 目录结构

```
tacti-reader-master/
├── tactireader.py          # 主程序入口（含全部核心类，~4500行）
├── main.py                 # 包模式入口（python -m tacti_reader）
├── tactireader.ico         # Windows 应用图标
├── tactireader.png         # 应用图标（PNG）
├── README.md               # 项目说明
├── flake.nix               # Nix 开发环境配置
├── flake.lock              # Nix 锁文件
├── .gitignore
│
├── tacti_reader/           # 已拆分的模块化代码
│   ├── __init__.py         # 延迟导入 TactiReader
│   ├── __main__.py         # python -m tacti_reader 支持
│   ├── main.py             # run() 函数：创建 QApplication + TactiReader
│   ├── main_window.py      # 重导出：from tactireader import TactiReader
│   ├── config.py           # ConfigManager 类
│   ├── constants.py        # 全局常量（路径、缩放、颜色预设）
│   └── utils.py            # 工具函数（resource_path, get_config_path, serialize_annotations）
│
└── docs/                   # 文档
    ├── README.md           # 文档索引
    ├── README.en.md        # 英文概览
    ├── PLAN.md             # 架构优化计划
    ├── help.md             # 英文使用指南
    ├── help_zh.md          # 中文使用指南
    ├── about.md            # 英文关于页
    └── about_zh.md         # 中文关于页
```

---

## 4. 模块详解

### 4.1 入口模块

项目提供三种启动方式，最终都创建 `TactiReader` 实例：

| 入口文件 | 启动命令 | 说明 |
|----------|----------|------|
| `tactireader.py` | `python tactireader.py [file]` | **主入口**，包含完整代码，可直接运行 |
| `main.py` | `python main.py [file]` | 包模式入口，调用 `tacti_reader.main.run()` |
| `tacti_reader/__main__.py` | `python -m tacti_reader [file]` | 模块模式入口 |

启动流程：

```
CLI 参数 → QApplication 创建 → TactiReader(pdf_path) → 窗口显示 → app.exec_()
```

### 4.2 核心常量模块 (constants)

**文件**：[constants.py](file:///c:/Users/Administrator/Desktop/ml/tacti-reader-master/tacti-reader-master/tacti_reader/constants.py)

定义全局常量，模块加载时即创建配置目录：

| 常量 | 类型 | 说明 |
|------|------|------|
| `APP_NAME` | `str` | 应用名称 `"TactiReader"` |
| `BOOKMARK_DIR_NAME` | `str` | 书签子目录名 `"tactireader_bookmarks"` |
| `CONFIG_DIR` | `str` | 配置文件目录，Windows 下为 `%APPDATA%\TactiReader\tactireader_bookmarks\` |
| `GLOBAL_CONFIG_FILE` | `str` | 全局配置文件路径 `global_settings.json` |
| `RENDER_SCALE` | `float` | PDF 渲染缩放倍数 `2.0` |
| `PEN_COLOR_PRESETS` | `list[tuple]` | 10 种画笔颜色预设 (RGB) |
| `RECT_COLOR_PRESETS` | `list[tuple]` | 8 种矩形高亮颜色预设 (RGBA) |
| `TEXT_COLOR_PRESETS` | `list[tuple]` | 6 种文本颜色预设 (RGB) |

### 4.3 配置管理模块 (config)

**文件**：[config.py](file:///c:/Users/Administrator/Desktop/ml/tacti-reader-master/tacti-reader-master/tacti_reader/config.py)

封装 `ConfigManager` 类，统一管理全局配置和文档配置的读写。

### 4.4 工具函数模块 (utils)

**文件**：[utils.py](file:///c:/Users/Administrator/Desktop/ml/tacti-reader-master/tacti-reader-master/tacti_reader/utils.py)

| 函数 | 说明 |
|------|------|
| `resource_path(relative_path)` | 获取资源文件绝对路径，兼容 PyInstaller 打包 (`sys._MEIPASS`) |
| `get_config_path(pdf_path)` | 根据 PDF 路径生成唯一配置文件名（MD5 哈希 + 文件名） |
| `serialize_annotations(obj)` | 递归序列化批注数据，将 `QColor` 转为十六进制颜色字符串 |

### 4.5 主窗口与业务逻辑 (tactireader.py)

**文件**：[tactireader.py](file:///c:/Users/Administrator/Desktop/ml/tacti-reader-master/tacti-reader-master/tactireader.py)

这是项目的**核心文件**（约 4500 行），包含所有 UI 类和业务逻辑。详见下方关键类说明。

---

## 5. 关键类说明

### 5.1 TactiReader (QMainWindow)

**位置**：`tactireader.py` 第 1490-4474 行

主窗口类，是整个应用的控制器和视图容器。

#### 核心职责

1. **UI 构建**：菜单栏、书签面板、阅读窗格、标签栏、状态栏
2. **文档管理**：PDF 加载/关闭、多标签页切换、笔记本导入/导出
3. **键盘事件分发**：`keyPressEvent` 是所有快捷键的统一入口（约 370 行）
4. **配置持久化**：保存/加载文档配置和全局配置
5. **批注管理**：批注的保存、撤销、清除
6. **搜索系统**：全文搜索与高亮

#### 关键实例变量

| 变量 | 类型 | 说明 |
|------|------|------|
| `doc` | `fitz.Document` | 当前打开的 PDF 文档对象 |
| `pdf_path` | `str \| None` | 当前 PDF 文件路径 |
| `notebook_source_path` | `str \| None` | 笔记本源文件路径（.tactinote 模式） |
| `total_pages` | `int` | 当前文档总页数 |
| `right_page` | `int` | 右窗格当前页码（1-indexed） |
| `home_page` | `int` | 已到达的最远页码 |
| `bookmarks` | `dict` | 瞬时书签 `{key: {"page": int, "name": str}}` |
| `annotations` | `dict` | 批注数据 `{page_str: [annotation_dict]}` |
| `page_rotations` | `dict` | 页面旋转状态 `{page_str: angle}` |
| `page_number_offset` | `int` | 逻辑页码偏移（逻辑页 = 物理页 + offset） |
| `single_page_mode` | `bool` | 单页/双页模式 |
| `left_locked` | `bool` | 左窗格是否锁定 |
| `flip_multiplier` | `int` | 翻页倍数 (1-9) |
| `open_documents` | `list[str]` | 已打开文档路径列表 |
| `recent_files` | `list[str]` | 最近文件列表（最多5个） |
| `search_highlights` | `dict` | 搜索高亮数据 `{page_num: [highlight_dict]}` |
| `left_last_location` | `tuple \| None` | 左窗格导航回退位置 |
| `right_last_location` | `tuple \| None` | 右窗格导航回退位置 |
| `current_lang` | `str` | 当前语言 `"en"` / `"zh"` |
| `translations` | `dict` | 翻译字典（200+ 条目） |

#### 关键方法

| 方法 | 说明 |
|------|------|
| `load_pdf(pdf_path)` | 加载 PDF 文件，重置状态，加载配置 |
| `render_page(page_num)` | 渲染指定页面为 QPixmap（2x 缩放） |
| `render_facing()` | 渲染双页/单页视图，处理锁定逻辑 |
| `jump_to_page(page_1idx)` | 统一跳转入口，根据焦点窗格决定目标 |
| `_jump_to_page_internal(page, is_left)` | 内部跳转实现，记录导航历史 |
| `keyPressEvent(event)` | 键盘事件统一处理（~370行） |
| `save_config()` | 保存当前文档配置到 JSON |
| `load_config()` | 加载文档配置 |
| `save_global_config()` | 保存全局配置（语言、最近文件、已打开文档） |
| `search_text_with_highlight(term, case_sensitive)` | 全文搜索并生成高亮数据 |
| `set_annotation_mode(mode)` | 设置批注模式（pen/rect/text） |
| `export_notebook()` | 导出为 .tactinote 文件 |
| `import_notebook()` | 从 .tactinote 文件导入 |
| `import_notebook_from_path(path)` | 从指定路径导入笔记本（无对话框） |
| `_flush_notebook_to_source()` | 将工作区状态打包回源 .tactinote |
| `calibrate_page_number_offset()` | 标定物理页码偏移 |
| `navigate_back()` | 单步导航回退 |
| `refresh_bookmark_panel()` | 刷新书签面板和 TOC |
| `tr(text, **kwargs)` | 翻译文本（国际化核心方法） |
| `_trigger_shortcut(key, modifiers)` | 菜单项模拟快捷键（反模式） |
| `update_document_tabs()` | 更新多文档标签栏 |
| `on_doc_tab_changed(index)` | 标签切换时加载对应文档 |
| `close_document_tab(index)` | 关闭指定标签页 |

### 5.2 TacticalPane (QLabel)

**位置**：`tactireader.py` 第 421-1488 行

PDF 页面显示窗格，负责页面渲染、批注绘制、交互操作。

#### 核心职责

1. **页面显示**：将 QPixmap 渲染到 QLabel，支持缩放、平移、旋转
2. **批注绘制**：在 `paintEvent` 中绘制搜索高亮、批注、临时批注预览
3. **交互处理**：鼠标拖拽（平移/绘制批注/文本选取）、滚轮缩放
4. **坐标变换**：处理旋转状态下的坐标转换（PDF 坐标 ↔ 屏幕坐标）

#### 关键实例变量

| 变量 | 类型 | 说明 |
|------|------|------|
| `page_pixmap` | `QPixmap \| None` | 当前显示的页面图像（可能已旋转） |
| `original_pixmap` | `QPixmap \| None` | 原始未旋转的页面图像 |
| `page_num` | `int` | 当前页码（1-indexed，-1 表示无页面） |
| `is_left_pane` | `bool` | 是否为左窗格 |
| `rotation` | `int` | 当前旋转角度（0/90/180/270） |
| `scale_factor` | `float` | 缩放因子 |
| `offset` | `QPointF` | 平移偏移量 |
| `annotations` | `list` | 当前页面的批注列表 |
| `annotation_mode` | `str \| None` | 当前批注模式 (`"pen"` / `"rect"` / `"text"` / `None`) |
| `search_highlights` | `list` | 搜索高亮矩形列表 |
| `text_selection_mode` | `bool` | 是否处于文字选取模式 |
| `pen_color` | `QColor` | 画笔颜色 |
| `rect_color` | `QColor` | 矩形高亮颜色 |
| `text_color` | `QColor` | 文本批注颜色 |

#### 关键方法

| 方法 | 说明 |
|------|------|
| `set_page(pixmap, page_num, is_left, reset_view, annotations)` | 设置显示页面 |
| `paintEvent(event)` | 核心绘制：页面 + 搜索高亮 + 批注 + 临时批注 + 焦点边框 |
| `draw_annotation(painter, annotation, offset_x, offset_y)` | 绘制单个批注（支持旋转坐标变换） |
| `mousePressEvent(event)` | 处理鼠标按下（批注开始/文本选取/拖拽） |
| `mouseMoveEvent(event)` | 处理鼠标移动（批注绘制/文本选取/拖拽平移） |
| `mouseReleaseEvent(event)` | 处理鼠标释放（批注完成/文本选取完成） |
| `wheelEvent(event)` | Ctrl+滚轮缩放，普通滚轮垂直平移 |
| `rotate_clockwise()` | 顺时针旋转 90° |
| `reset_view()` | 重置缩放、平移、旋转 |
| `set_search_highlights(highlights, search_text)` | 设置搜索高亮 |
| `update_selected_text()` | 更新文本选取（坐标变换 + 智能插值） |
| `_transform_point_for_rotation(x, y, from_rot, to_rot, w, h)` | 旋转坐标变换 |
| `_pixmap_coord_to_pdf_0deg(px, py)` | 当前视图坐标 → 0° PDF 坐标 |
| `_pixmap_rect_to_pdf_0deg_rect(x, y, w, h)` | 当前视图矩形 → 0° PDF 包围盒 |
| `finish_text_annotation(text)` | 完成文本批注（计算尺寸并保存） |
| `cancel_annotation()` | 取消当前批注绘制 |

### 5.3 BookmarkButton (QLabel)

**位置**：`tactireader.py` 第 92-133 行

可点击的书签按钮，显示书签键名、名称和页码。

| 属性 | 说明 |
|------|------|
| `key` | 书签键名（Q/W/E/.../P） |
| `page` | 书签页码 |
| `bookmarkClicked` | 信号，点击时发射书签键名 |

### 5.4 InlineTextEdit (QTextEdit)

**位置**：`tactireader.py` 第 136-168 行

内联文本编辑器，用于文本批注输入。

| 信号 | 说明 |
|------|------|
| `textConfirmed(str)` | Ctrl+Enter 确认或失去焦点时发射 |
| `editingCancelled()` | Esc 取消编辑时发射 |

特殊行为：Enter 键换行（非确认），Ctrl+Enter 确认。

### 5.5 SearchDialog (QDialog)

**位置**：`tactireader.py` 第 194-418 行

全文搜索对话框，支持大小写敏感搜索、结果列表、上下导航。

| 信号 | 说明 |
|------|------|
| `searchResultSelected(int, str)` | 选中搜索结果时发射（页码, 上下文） |

| 方法 | 说明 |
|------|------|
| `perform_search()` | 执行搜索，遍历所有页面 |
| `go_to_previous()` / `go_to_next()` | 导航到上/下一个搜索结果 |
| `on_result_clicked(item)` | 单击跳转 |
| `on_result_double_clicked(item)` | 双击跳转并关闭 |

### 5.6 LanguageSelectDialog (QDialog)

**位置**：`tactireader.py` 第 172-190 行

首次运行时的语言选择对话框，提供 English 和简体中文两个选项。

### 5.7 MarkdownViewer (QDialog)

**位置**：`tactireader.py` 第 4477-4508 行

Markdown 文档查看器，用于显示帮助和关于页面。使用 `markdown` 库将 Markdown 转为 HTML，在 `QTextBrowser` 中渲染。

### 5.8 ConfigManager

**位置**：[config.py](file:///c:/Users/Administrator/Desktop/ml/tacti-reader-master/tacti-reader-master/tacti_reader/config.py)

| 方法 | 说明 |
|------|------|
| `load_global_config()` | 加载全局配置，返回 `global_config` 字段内容 |
| `save_global_config(global_config)` | 保存全局配置（包装在 `{"global_config": ...}` 中） |
| `load_document_config(config_file)` | 加载文档级配置 |
| `save_document_config(config_file, data, serializer)` | 保存文档级配置，支持自定义序列化器 |

---

## 6. 核心数据结构

### 文档配置 JSON 结构

每个 PDF 对应一个独立的 JSON 配置文件，存储在 `CONFIG_DIR` 下：

```json
{
  "config": {
    "multiplier": 1,
    "home_page": 42,
    "last_page": 50,
    "single_page_mode": false,
    "left_locked": true,
    "locked_left_page": 39,
    "pen_color_index": 0,
    "rect_color_index": 0,
    "text_color_index": 0,
    "bookmark_panel_visible": true,
    "splitter_sizes": [500, 500]
  },
  "Q": { "page": 10, "name": "帧结构" },
  "W": { "page": 87, "name": "错误码" },
  "page_rotations": { "10": 90, "87": 0 },
  "annotations": {
    "10": [
      { "type": "pen", "points": [[x,y], ...], "color": "#ff0000", "width": 3, "creation_rotation": 0 },
      { "type": "rect", "rect": [x, y, w, h], "color": "#ffff00", "creation_rotation": 0 },
      { "type": "text", "rect": [x, y, w, h], "color": "#000000", "text": "批注内容", "font_size": 12, "creation_rotation": 0 }
    ]
  },
  "page_number_offset": -9,
  "global_left_scale": 1.0,
  "global_left_offset": [0, 0],
  "global_left_rotation": 0,
  "global_right_scale": 1.0,
  "global_right_offset": [0, 0],
  "global_right_rotation": 0
}
```

### 全局配置 JSON 结构

存储在 `GLOBAL_CONFIG_FILE` (`global_settings.json`)：

```json
{
  "global_config": {
    "language": "zh",
    "recent_files": ["path/to/file1.pdf", "path/to/file2.tactinote"],
    "open_documents": ["path/to/file1.pdf"]
  }
}
```

### .tactinote 文件结构

`.tactinote` 是一个 ZIP 压缩包（无压缩存储）：

```
notebook.tactinote
├── document.pdf       # 原始 PDF 文件
└── session.json       # 完整的文档配置 JSON
```

### 批注数据格式

| 类型 | 字段 | 说明 |
|------|------|------|
| `pen` | `type`, `points`, `color`, `width`, `creation_rotation` | 自由画笔，`points` 为 `[[x, y], ...]` |
| `rect` | `type`, `rect`, `color`, `creation_rotation` | 矩形高亮，`rect` 为 `[x, y, w, h]` |
| `text` | `type`, `rect`, `color`, `text`, `font_size`, `creation_rotation` | 文本批注 |

所有坐标统一存储为 **0° PDF 坐标系**，渲染时根据当前旋转角度动态变换。

---

## 7. 依赖关系

### 外部依赖

| 依赖 | 版本要求 | 用途 |
|------|----------|------|
| `PyMuPDF` (fitz) | - | PDF 文档解析、渲染、文本搜索 |
| `PyQt5` | - | GUI 框架（窗口、控件、事件系统） |
| `markdown` | - | Markdown → HTML 渲染（帮助/关于页面） |

> **注意**：不要安装 `fitz` 这个同名包，TactiReader 依赖的是 `PyMuPDF`。

### 内部模块依赖图

```
tactireader.py
├── tacti_reader.constants  (CONFIG_DIR, GLOBAL_CONFIG_FILE, RENDER_SCALE, 颜色预设)
├── tacti_reader.config     (ConfigManager)
└── tacti_reader.utils      (get_config_path, resource_path, serialize_annotations)

main.py
└── tacti_reader.main       (run)
    └── tacti_reader.main_window  (TactiReader)
        └── tactireader     (通过 __init__.py 延迟导入)

tacti_reader/config.py
└── tacti_reader.constants  (GLOBAL_CONFIG_FILE)

tacti_reader/utils.py
├── tacti_reader.constants  (CONFIG_DIR)
└── PyQt5.QtGui             (QColor)
```

### Python 版本

要求 Python 3.14+（根据 `flake.nix` 配置）。

---

## 8. 项目运行方式

### 开发运行

```bash
# 安装依赖
pip install PyMuPDF PyQt5 markdown

# 方式1：直接运行主入口
python tactireader.py

# 方式2：打开指定文件
python tactireader.py your_file.pdf
python tactireader.py your_notebook.tactinote

# 方式3：包模式运行
python main.py
python -m tacti_reader
```

### Nix 开发环境

```bash
# 进入 Nix 开发 shell（自动配置 Qt 和 Python 环境）
nix develop
python tactireader.py
```

### 打包发布

使用 PyInstaller 打包：

**Windows:**
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

**macOS/Linux:** 将 `;` 分隔符改为 `:`。

---

## 9. 配置与数据持久化

### 存储位置

| 数据 | 路径 | 说明 |
|------|------|------|
| 全局配置 | `%APPDATA%\TactiReader\tactireader_bookmarks\global_settings.json` | 语言、最近文件、已打开文档 |
| 文档配置 | `%APPDATA%\TactiReader\tactireader_bookmarks\{filename}_{hash}.json` | 书签、批注、视图状态 |
| 笔记本临时文件 | `%APPDATA%\TactiReader\temp\nb_{hash}\` | 解压 .tactinote 的工作目录 |

> Linux/macOS 下，若 `APPDATA` 环境变量不存在，配置目录回退到当前工作目录下的 `tactireader_bookmarks/`。

### 保存时机

| 时机 | 保存内容 |
|------|----------|
| 按 `S` 键 | 当前文档配置（笔记本模式额外打包回源文件） |
| 切换标签页 | 当前文档配置 + 笔记本回写 |
| 关闭标签页 | 全局配置（更新 open_documents） |
| 关闭窗口 | 当前文档配置 + 笔记本回写 |
| 设置书签/批注/颜色 | 当前文档配置 |
| 切换语言 | 全局配置 + 当前文档配置 |

### 配置文件命名规则

`get_config_path(pdf_path)` 生成规则：
```
{basename}_{md5_hash[:12]}.json
```
其中 `basename` 为 PDF 文件名（`.` 和空格替换为 `_`），`md5_hash` 为 PDF 绝对路径的 MD5 前 12 位。

---

## 10. 国际化机制

### 实现方式

采用**内联翻译字典**方式，而非 Qt 的 `QTranslator` 体系：

1. `TactiReader.translations` 字典包含 `"en"` 和 `"zh"` 两个键，值均为 `{英文原文: 翻译文本}` 的映射
2. `tr(text, **kwargs)` 方法以英文原文为 key 查找翻译，支持 `str.format()` 模板参数
3. 首次运行时弹出 `LanguageSelectDialog`，选择结果保存到全局配置
4. 切换语言后需重启应用才能完全生效

### 翻译覆盖范围

- 菜单项文本（文件/视图/导航/批注/工具/帮助/语言）
- 对话框标题和按钮
- 状态栏提示消息
- 书签面板文本
- 帮助/关于页面（通过 `docs/help_zh.md` / `docs/about_zh.md` 独立文件）

---

## 11. 快捷键体系

### 导航

| 快捷键 | 功能 |
|--------|------|
| `A` / `D` | 上一页 / 下一页 |
| `←` / `→` | 向后/向前跳转 N 页（N 为翻页倍数） |
| `1`-`9` | 设置翻页倍数 N |
| `G` | 跳转到指定页码 |
| `Ctrl+G` | 标定物理页码偏移 |
| `Ctrl+Shift+G` | 清除页码偏移 |
| `Space` | 跳转到 Home 页 |
| `Ctrl+Space` | 将当前页设为 Home |
| `Ctrl+A` | 单步导航回退 |
| `F` | 全文搜索 |

### 书签

| 快捷键 | 功能 |
|--------|------|
| `Q`-`P` | 跳转到对应书签 |
| `Ctrl+Q`-`Ctrl+P` | 在当前页设置书签 |
| `Alt+Q`-`Alt+P` | 清除对应书签 |

### 视图

| 快捷键 | 功能 |
|--------|------|
| `Z` | 单页/双页模式切换 |
| `C` | 左窗格锁定/跟随切换 |
| `N` | 书签与目录面板显示/隐藏 |
| `~` (QuoteLeft) | 顺时针旋转当前页 90° |
| `X` | 重置当前页（缩放+平移+旋转） |
| `Ctrl+X` | 重置双页布局 + 分隔条居中 |
| `Ctrl+Shift+X` | 清除全书旋转 |
| `F11` | 全屏切换 |
| `Ctrl+滚轮` | 缩放 |

### 批注

| 快捷键 | 功能 |
|--------|------|
| `B` | 画笔模式 |
| `H` | 矩形高亮模式 |
| `V` | 文本批注模式 |
| `Esc` | 退出批注/文字选取模式 |
| `Ctrl+Enter` | 确认文本批注 |
| `Ctrl+Z` | 撤销最后一条批注 |
| `Ctrl+Shift+C` | 清除当前页所有批注 |
| `Ctrl+Shift+R` | 全局重置（不可撤销） |

### 工具

| 快捷键 | 功能 |
|--------|------|
| `J` | 切换文字选取模式 |
| `Ctrl+C` | 复制选中文本 |
| `S` | 保存配置 |

---

## 12. 已知架构问题与优化方向

根据 [PLAN.md](file:///c:/Users/Administrator/Desktop/ml/tacti-reader-master/tacti-reader-master/docs/PLAN.md) 中的规划，项目存在以下待优化问题：

### Phase 1: 模块化拆分（部分完成）

- [x] 已拆分 `constants.py`、`config.py`、`utils.py`
- [ ] 待拆分：`i18n.py`（200+ 行翻译字典）、`widgets/pane.py`（TacticalPane ~1000 行）、`widgets/dialogs.py`、`widgets/bookmark.py`

### Phase 2: 重复代码

- `import_notebook()` 与 `import_notebook_from_path()` 逻辑高度重复
- 搜索逻辑在 `search_text_with_highlight()` 和 `SearchDialog.perform_search()` 中重复
- `GLOBAL_CONFIG_FILE` 在 `__init__` 中被读取 3 次

### Phase 3: 代码规范

- 大量 `print()` 调试语句应替换为 `logging`
- 重复 import（`QVBoxLayout`、`QHBoxLayout`、`QTextEdit` 等在顶部 import 了两次）
- `keyPressEvent` 超过 280 行，应拆分为子方法

### Phase 4: 架构改进

- 菜单项通过 `_trigger_shortcut()` 模拟按键事件是反模式，应改为连接到同一 slot
- 配置路径仅处理 Windows `APPDATA`，应使用 `QStandardPaths`
- 批注逻辑分散在 `TacticalPane` 和 `TactiReader` 中，应封装为 `AnnotationManager`
- 多文档管理逻辑应从 `TactiReader` 中提取为 `DocumentManager`

### Phase 5: 构建与依赖

- 缺少 `pyproject.toml` 或 `setup.py` 声明依赖
- 缺少单元测试

---

> **TactiReader** — 不是 PDF 阅读器，而是你的战术认知外骨骼。
