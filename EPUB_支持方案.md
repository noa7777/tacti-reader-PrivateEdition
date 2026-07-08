# EPUB 支持方案

## 1. 概述

为 TactiReader 增加 EPUB 格式电子书阅读能力。通过**预览调整模式**将 EPUB 内容渲染为固定分页的静态页面，之后完全复用现有 PDF 交互逻辑。

## 2. 格式支持

| 格式 | 支持方式 |
|------|---------|
| EPUB | 直接使用 PyMuPDF（MuPDF 引擎）原生打开 |
| MOBI / AZW3 | 不支持。用户需自行用 Calibre 转换为 EPUB |

## 3. 总体流程

```
打开 .epub 文件
    │
    ├─ 已有排版配置 ──→ 进入正常阅读模式（与 PDF 完全相同）
    │
    └─ 首次打开（无排版配置）
         │
         ▼
    进入预览调整模式
         │
         ├─ 自动进入 F11 全屏
         ├─ 双栏显示（左页 / 右页）
         ├─ 悬浮窗（可拖拽移动，覆盖在页面之上）
         │   包含所有排版设置参数
         │   任一参数修改 → 实时重新排版 → 双栏同步刷新
         │
         └─ 点击 [确认] → 锁定参数 → 固定分页
              │
              ▼
         退出全屏 → 进入正常阅读模式
              │
              ├─ 状态栏显示页码（第 1~N 页）
              ├─ 翻页（A/D、←/→）✅ 复用现有逻辑
              ├─ 批注（B/H/V）✅ 复用现有逻辑
              ├─ 书签（Q~P）✅ 复用现有逻辑
              ├─ 主线页（Space）✅ 复用现有逻辑
              ├─ Ctrl+滚轮缩放 ✅ 复用现有逻辑（静态页放大）
              ├─ 跳转（G）✅ 复用现有逻辑
              └─ 所有其他快捷键 ✅ 复用现有逻辑
```

## 4. 预览调整模式（核心）

### 4.1 进入方式

- **首次打开** EPUB 时（无对应排版配置），自动进入预览调整模式
- 通过"打开文件"或"换书"菜单首次切换到该 EPUB 时，均进入预览调整模式
- 已配置的 EPUB 再次打开时**直接进入正常阅读模式**，跳过预览调整

### 4.2 窗口状态

- **仅预览调整模式**自动进入 F11 全屏
- 正常阅读模式为普通窗口，与 PDF 阅读模式一致
- 双栏显示（左页 + 右页），与 PDF 双栏布局一致
- 预览调整模式下**显示状态栏**（显示页码），这与 PDF 全屏隐藏状态栏不同
- 状态栏（EPUB 模式下）右侧显示 `[左页码/右页码]` 格式，置于所有信息的最右侧。例如：`Double | ×1 | Annot: None    [1/2]`
- 预览调整模式下，两页周围有黑色边框，用于示意纸张的形状和大小，与正常阅读模式的焦点边框无关

### 4.3 悬浮窗

#### 位置与交互

- 悬浮窗覆盖在左侧页面上方（z-index 高于页面）
- 可拖拽移动
- 默认在左侧上方

#### 设置项

| 设置项 | 控件类型 | 取值范围 | 默认值 | 说明 |
|--------|---------|---------|-------|------|
| 字体 | 下拉菜单 | 系统所有可用字体 + "默认书中的" | 默认书中的 | 选择"默认书中的"则使用 EPUB 原始 CSS 字体设置 |
| 字号 | 滑块/数字输入 | 8~48 | 25 | 字体大小（pt） |
| 行高 | 滑块/数字输入 | 1.0~2.5，步进 0.1 | 1.3 | 行间距倍数 |
| 段落间距 | 滑块/数字输入 | 0~32，步进 2 | 3 | 段落之间的额外间距（pt） |
| 首行缩进 | 滑块/数字输入 | 0~8，步进 1 | 2 | 每段首行缩进的字符数 |
| 两端对齐 | 开关 | 开/关 | 关 | 文字是否两端对齐（justify） |
| 字体粗细 | 下拉菜单 | 正常/加粗/ lighter / bolder | 正常 | 文字的粗细程度 |
| 上边距 | 数字输入 | 0~100 | 0 | 页面顶部留白（pt） |
| 下边距 | 数字输入 | 0~100 | 0 | 页面底部留白（pt） |
| 左边距 | 数字输入 | 0~100 | 20 | 页面左侧留白（pt） |
| 右边距 | 数字输入 | 0~100 | 20 | 页面右侧留白（pt） |

#### 按钮

- **[确认]**: 锁定当前参数，退出预览模式
- **[取消]**: 不打开 EPUB，直接关闭

#### 实时预览

- 修改任一参数 → 立即调用 `apply_css()` + `layout()` 重新排版 → 刷新左页和右页内容
- 预览期间只排版当前附近几页，避免整本书重新排版带来的卡顿
- 页码随排版变化动态更新

### 4.4 确认后的行为

- 保存排版参数到 EPUB 对应的配置文件中
- 调用 `doc.layout()` 对整个文档按最终参数重新分页
- 退出全屏（回到普通窗口模式）
- 进入正常阅读模式，所有交互与 PDF 一致（状态栏 `[左页码/右页码]` 格式同上）

## 5. 确认后限制

| 项目 | 限制 |
|------|------|
| 修改字体/排版 | ❌ 不可。需重新打开 EPUB 进入预览调整模式 |
| 批注 | ✅ 完全可用 |
| 书签 | ✅ 完全可用 |
| 主线页 | ✅ 完全可用 |
| Ctrl+滚轮缩放 | ✅ 完全可用（静态页放大，非字体放大） |
| 重新进入预览 | 丢弃所有批注和书签 |

## 6. 技术实现要点

### 6.1 EPUB 检测

```python
def is_epub(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return ext in ['.epub']
```

### 6.2 重新排版

```python
doc = fitz.open("book.epub")
doc.layout(
    fontsize=16,
    line_height=1.6,
    width=page_width,   # 由窗口宽度计算
    height=page_height,  # 固定为屏幕可用高度
)
```

### 6.3 参数存储

排版参数保存在 EPUB 对应的配置文件中，格式：

```json
{
    "font": "思源黑体",
    "fontsize": 16,
    "line_height": 1.6,
    "para_spacing": 4,
    "indent_chars": 2,
    "justify": true,
    "font_weight": "normal"
}
```

### 6.4 悬浮窗可拖拽

使用 Qt 无边框窗口或 QWidget，重写 `mousePressEvent` / `mouseMoveEvent` 实现拖拽。

### 6.5 CSS 注入策略

```python
# 构建完整 CSS
css = f"""
body * {{
    font-family: '{font_family}' !important;
    font-size: {fontsize}pt !important;
    line-height: {line_height} !important;
    text-indent: {indent_chars}em !important;
    text-align: {'justify' if justify else 'left'} !important;
    margin-bottom: {para_spacing}pt !important;
    font-weight: {font_weight} !important;
    padding-top: {margin_top}pt !important;
    padding-bottom: {margin_bottom}pt !important;
    padding-left: {margin_left}pt !important;
    padding-right: {margin_right}pt !important;
}}
"""
doc.apply_css(css, append=False)
doc.layout(fontsize=fontsize, width=page_width, height=page_height)
```

- 使用 `body *` 通用选择器匹配所有元素
- `append=False` 完全替换默认 CSS，避免与 EPUB 自带 CSS 冲突
- 所有属性加 `!important` 确保覆盖 EPUB 原始样式

## 7. 不受影响的功能清单

以下功能无需任何修改，直接复用现有代码：

- 翻页（A/D、←/→）
- 翻页倍数设置（1~9）
- 批注（B/H/V/ESC）
- 撤销批注（Ctrl+Z）
- 书签（Q~P / Ctrl+Q~P / Alt+Q~P）
- 主线页（Space / Ctrl+Space）
- 单步回退（Ctrl+A）
- 跳转（G）
- 页码偏移标定（Ctrl+G）
- 目录面板（L / N）
- 全文搜索（F）
- 旋转（~）
- 重置视图（X）
- 左窗格锁定/跟随（C）
- 单双页切换（Z）
- 文字选取（J）
- 保存（S）
- 全屏切换（F11）
- 主题切换（颜色模式）