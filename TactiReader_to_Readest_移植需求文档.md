# TactiReader 交互体验移植到 Readest 需求文档

## 1. 项目概述

**目标**：将 TactiReader 阅读器的优秀交互体验移植到 Readest，提升 PDF/EPUB 阅读的便利性和效率。

**Readest 现状**：
- 基于 Web 技术（TypeScript/Tauri）的跨平台阅读器
- 支持 EPUB/PDF/MOBI/AZW3 等格式
- 已有功能：分页/滚动模式、高亮、书签、笔记、TTS、翻译、云同步、主题切换

**需要去掉的不兼容功能**：
- 双栏模式（Readest 不支持双栏布局）
- 左窗格锁定/跟随（双栏特有）
- .tactinote 笔记本格式（Readest 有自己的数据格式）

---

## 2. TactiReader 核心交互特性

### 2.1 快捷键系统

| 快捷键 | 功能 | 移植优先级 | 备注 |
|--------|------|-----------|------|
| **导航** | | | |
| 1-9 | 设置翻页倍数 | **高** | 按数字键设置倍数，←/→ 按倍数翻页 |
| ←/→ | 按倍数翻页 | **高** | 配合 1-9 使用 |
| A/D | 单步翻页 | **高** | 固定翻 1 页，不受倍数影响 |
| Ctrl+A | 导航回退 | **高** | 单次回退到上一个位置 |
| 空格 | 返回 Home 页 | **高** | Home = 到达过的最远页码 |
| Ctrl+空格 | 重定义 Home 页 | **高** | 手动设置 Home 为当前页 |
| G | 跳转到页码 | **高** | 输入页码跳转 |
| Ctrl+G | 标定物理页码偏移 | 中 | 修正 PDF 页码与物理页码的偏差 |
| Ctrl+Shift+G | 清除物理页码偏移 | 中 | 重置偏移为 0 |
| F | 全文搜索 | **高** | Readest 已有，可保留 |
| Ctrl+L | 打开 PDF 目录（TOC） | **高** | Readest 已有，可保留 |
| **瞬时书签** | | | |
| Q-P | 跳转到瞬时书签 | **高** | 10 个标签位，快速跳转 |
| Ctrl+Q-P | 设置瞬时书签 | **高** | 保存当前位置到标签 |
| Alt+Q-P | 删除瞬时书签 | **高** | 清除指定标签 |
| **批注** | | | |
| B | 画笔批注 | **高** | 自由手绘 |
| H | 矩形高亮 | **高** | 矩形区域高亮 |
| V | 文字批注 | **高** | 在任意位置插入文字 |
| Ctrl+Enter | 确认文字批注 | **高** | 完成文字输入 |
| Esc | 退出批注模式 | **高** | 取消当前批注操作 |
| Ctrl+Shift+C | 清除当前页批注 | 中 | 删除当前页所有批注 |
| Ctrl+Z | 撤销批注 | **高** | 撤销最后一条批注 |
| **视图** | | | |
| Z | 切换单双页模式 | ❌ 不兼容 | Readest 无双栏 |
| C | 切换左窗格锁定 | ❌ 不兼容 | 双栏特有 |
| X | 重置当前页 | 中 | 重置缩放和旋转 |
| Ctrl+X | 重置双页并居中 | ❌ 不兼容 | 双栏特有 |
| Ctrl+Shift+X | 清除全书旋转 | 中 | 清除所有页面旋转 |
| ~ | 旋转当前页 | 中 | 顺时针旋转 90° |
| N | 显示/隐藏侧边栏 | **高** | Readest 已有侧边栏 |
| F11 | 全屏 | **高** | Readest 已有 |
| **其他** | | | |
| S | 保存配置 | 低 | Readest 自动保存 |
| Ctrl+Shift+R | 全局重置 | 中 | 清除所有配置（书签、批注等） |
| J | 文字选取模式 | 中 | 选中文本后可复制 |

### 2.2 批注系统

#### 2.2.1 画笔模式（B）
- **交互方式**：按 B 进入画笔模式，鼠标/触控笔自由绘制
- **颜色方案**：10 套预设颜色
  - #FF8280（亮红）、#59C6FF（亮蓝）、#A86CC8（亮紫）
  - #F08A9A（粉红）、#5BC0DE（亮青）、#E6A87A（暖杏橙）
  - #A8C89A（浅鼠尾草绿）、#D4C87A（淡米黄）、#A68B7A（暖灰褐）、#9E9E9E（中性灰）
- **颜色切换**：菜单中选择，当前选中项显示勾选标记

#### 2.2.2 矩形高亮（H）
- **交互方式**：按 H 进入高亮模式，拖拽绘制矩形区域
- **颜色方案**：8 套预设颜色（半透明）
  - #D4A373（金盏菊黄）、#D97A5C（珊瑚橙）、#B5838D（玫瑰粉褐）
  - #80B291（鼠尾草绿）、#9B9E8F（橄榄灰）、#C58B6B（杏色）
  - #A69CAC（薰衣草灰）、#B56B6B（砖红）

#### 2.2.3 文字批注（V）
- **交互方式**：按 V 进入文字模式，在页面任意位置点击插入光标
- **自动换行**：到达纸边自动换行，每行起始点对齐
- **颜色方案**：6 套预设颜色
  - #FF8280（亮红）、#59C6FF（亮蓝）、#A86CC8（亮紫）
  - #8B5A2B（正棕）、#7DA87D（柔绿）、#D69A6A（暖橙）
- **字体大小**：默认 19pt，可通过菜单调整

### 2.3 书签系统

#### 2.3.1 瞬时书签（Q-P）
- **10 个标签位**：Q、W、E、R、T、Y、U、I、O、P
- **跳转**：直接按字母键跳转到对应位置
- **设置**：Ctrl+字母键保存当前位置（可附加名称）
- **删除**：Alt+字母键清除指定标签
- **优势**：比传统书签更快，无需打开面板

#### 2.3.2 左侧书签面板（N）
- **显示/隐藏**：按 N 切换面板可见性
- **内容**：显示所有书签列表，点击跳转
- **与瞬时书签共存**：面板显示传统书签，瞬时书签独立管理

### 2.4 导航系统

#### 2.4.1 Home 页概念
- **定义**：Home = 到达过的最远页码
- **自动更新**：通过 D、→、G、搜索、书签跳转到更远的页面时，Home 自动更新
- **向后翻页不降低 Home**：A、← 不会降低 Home 值
- **空格**：瞬间返回 Home 页
- **Ctrl+空格**：手动重设 Home 为当前页（唯一可以降低 Home 的方式）

#### 2.4.2 翻页倍数
- **设置**：按 1-9 数字键设置倍数
- **应用**：←/→ 按倍数翻页（如设置 ×3，按 → 翻 3 页）
- **A/D 不受影响**：始终翻 1 页

#### 2.4.3 页码标定
- **场景**：PDF 物理页码与书籍印刷页码不一致时
- **Ctrl+G**：标定偏移量（如物理第 10 页 = 印刷第 5 页，偏移 = -5）
- **Ctrl+Shift+G**：清除偏移，恢复默认

#### 2.4.4 导航回退（Ctrl+A）
- **功能**：回退到上一个跨页位置（仅 1 步）
- **场景**：跳转后发现跳错了，快速返回

### 2.5 主题系统

- **浅色**：#FFFFFF 背景，#141414 文字
- **黄色**：#F5EFD7 背景，#141412 文字
- **绿色**：#C7EDCC 背景，#101310 文字
- **和光**：#E0E0E0 背景，#141414 文字（低对比度，护眼）

### 2.6 视图控制

#### 2.6.1 旋转（~）
- **功能**：顺时针旋转当前页 90°
- **场景**：扫描版 PDF 页面方向错误时
- **持久化**：旋转状态保存到配置文件

#### 2.6.2 重置（X）
- **X**：重置当前页的缩放、平移、旋转
- **Ctrl+Shift+X**：清除全书所有页面的旋转

#### 2.6.3 默认大小
- **实际大小**：100% 缩放
- **适合宽度**：页面宽度填满窗格
- **适合页面**：页面完整显示在窗格内（默认）

### 2.7 搜索功能

- **快捷键**：F
- **对话框尺寸**：宽 = 屏幕宽度 × 3/5，高 = 屏幕高度 × 7/10
- **字体大小**：所有文字 21pt
- **功能**：
  - 全文搜索（所有页面）
  - 搜索结果高亮显示
  - 点击结果跳转到对应页面
  - 大小写敏感切换

### 2.8 文字选取模式（J）

- **进入/退出**：按 J 切换模式
- **功能**：选中文本后可右键复制
- **退出**：按 Esc 退出模式

### 2.9 配置保存

- **自动保存**：翻页、批注、书签等操作后自动保存
- **手动保存**：按 S 立即保存
- **保存内容**：
  - 书签、瞬时书签
  - 批注（画笔、高亮、文字）
  - 页码偏移、Home 页
  - 单双页模式、左窗格锁定状态
  - 页面旋转、缩放、平移
  - 主题、颜色方案
  - 最近文件列表

### 2.10 全局重置（Ctrl+Shift+R）

- **功能**：清除当前 PDF 的所有配置
- **清除内容**：
  - 书签、瞬时书签
  - 批注
  - 页码偏移、Home 页
  - 单双页模式、左窗格锁定
  - 页面旋转
  - 颜色方案索引
- **确认对话框**：防止误操作

---

## 3. 移植优先级与实施计划

### 阶段一：核心交互（1-2 周）

#### 3.1 翻页倍数系统
**实现要点**：
```typescript
// 状态管理
let flipMultiplier = 1;

// 键盘事件
document.addEventListener('keydown', (e) => {
  // 数字键 1-9 设置倍数
  if (e.key >= '1' && e.key <= '9' && !e.ctrlKey && !e.altKey) {
    flipMultiplier = parseInt(e.key);
    showToast(`翻页倍数: ×${flipMultiplier}`);
    return;
  }
  
  // ←/→ 按倍数翻页
  if (e.key === 'ArrowLeft' && !e.ctrlKey && !e.altKey) {
    goToPage(currentPage - flipMultiplier);
    return;
  }
  if (e.key === 'ArrowRight' && !e.ctrlKey && !e.altKey) {
    goToPage(currentPage + flipMultiplier);
    return;
  }
  
  // A/D 固定翻 1 页
  if (e.key === 'a' && !e.ctrlKey && !e.altKey) {
    goToPage(currentPage - 1);
    return;
  }
  if (e.key === 'd' && !e.ctrlKey && !e.altKey) {
    goToPage(currentPage + 1);
    return;
  }
});
```

#### 3.2 Home 页概念
**实现要点**：
```typescript
// 状态管理
let homePage = 1;

// 跳转时自动更新 Home
function goToPage(page: number) {
  if (page > homePage) {
    homePage = page;
  }
  currentPage = page;
  renderPage();
}

// 空格返回 Home
document.addEventListener('keydown', (e) => {
  if (e.key === ' ' && !e.ctrlKey && !e.altKey) {
    goToPage(homePage);
    return;
  }
  
  // Ctrl+空格重定义 Home
  if (e.key === ' ' && e.ctrlKey) {
    homePage = currentPage;
    showToast(`Home 已设置为第 ${homePage} 页`);
    return;
  }
});
```

#### 3.3 瞬时书签（Q-P）
**实现要点**：
```typescript
// 数据结构
interface InstantBookmark {
  page: number;
  name?: string;
}

const instantBookmarks: Record<string, InstantBookmark> = {};

// 键盘事件
document.addEventListener('keydown', (e) => {
  const bookmarkKeys = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'];
  
  if (bookmarkKeys.includes(e.key.toLowerCase())) {
    const key = e.key.toUpperCase();
    
    // 直接按：跳转
    if (!e.ctrlKey && !e.altKey) {
      if (instantBookmarks[key]) {
        goToPage(instantBookmarks[key].page);
      } else {
        showToast(`书签 ${key} 未设置`);
      }
      return;
    }
    
    // Ctrl+按键：设置
    if (e.ctrlKey) {
      instantBookmarks[key] = { page: currentPage };
      showToast(`书签 ${key} 已设置`);
      saveConfig();
      return;
    }
    
    // Alt+按键：删除
    if (e.altKey) {
      delete instantBookmarks[key];
      showToast(`书签 ${key} 已删除`);
      saveConfig();
      return;
    }
  }
});
```

#### 3.4 导航回退（Ctrl+A）
**实现要点**：
```typescript
// 历史记录（仅保留最近 1 次）
let lastLocation: { page: number; rotation: number; scale: number } | null = null;

// 跳转前保存位置
function goToPage(page: number) {
  lastLocation = {
    page: currentPage,
    rotation: currentRotation,
    scale: currentScale
  };
  currentPage = page;
  renderPage();
}

// Ctrl+A 回退
document.addEventListener('keydown', (e) => {
  if (e.key === 'a' && e.ctrlKey) {
    if (lastLocation) {
      currentPage = lastLocation.page;
      currentRotation = lastLocation.rotation;
      currentScale = lastLocation.scale;
      lastLocation = null; // 清空，避免重复回退
      renderPage();
    } else {
      showToast('没有可回退的位置');
    }
    return;
  }
});
```

### 阶段二：批注增强（1-2 周）

#### 3.5 画笔批注（B）
**实现要点**：
- 按 B 进入画笔模式
- 鼠标/触控笔自由绘制
- 10 套预设颜色，菜单切换
- Esc 退出模式

#### 3.6 矩形高亮（H）
**实现要点**：
- 按 H 进入高亮模式
- 拖拽绘制矩形区域
- 8 套预设颜色（半透明）
- Esc 退出模式

#### 3.7 文字批注（V）
**实现要点**：
- 按 V 进入文字模式
- 点击页面任意位置插入光标
- 自动换行（到达纸边）
- 6 套预设颜色
- 默认字体 19pt
- Ctrl+Enter 确认，Esc 取消

#### 3.8 批注管理
**实现要点**：
- Ctrl+Shift+C：清除当前页批注
- Ctrl+Z：撤销最后一条批注

### 阶段三：视图控制（1 周）

#### 3.9 页面旋转（~）
**实现要点**：
```typescript
// 按 ~ 旋转当前页
document.addEventListener('keydown', (e) => {
  if (e.key === '`') { // ~ 键
    currentRotation = (currentRotation + 90) % 360;
    renderPage();
    showToast(`旋转至 ${currentRotation}°`);
    return;
  }
});
```

#### 3.10 重置视图（X）
**实现要点**：
- X：重置当前页缩放、平移、旋转
- Ctrl+Shift+X：清除全书所有页面的旋转

#### 3.11 页码标定（Ctrl+G）
**实现要点**：
```typescript
// 页码偏移
let pageNumberOffset = 0;

// Ctrl+G 标定偏移
document.addEventListener('keydown', (e) => {
  if (e.key === 'g' && e.ctrlKey && !e.shiftKey) {
    const physicalPage = prompt('请输入当前页的印刷页码:');
    if (physicalPage) {
      pageNumberOffset = parseInt(physicalPage) - currentPage;
      showToast(`页码偏移: ${pageNumberOffset}`);
      saveConfig();
    }
    return;
  }
  
  // Ctrl+Shift+G 清除偏移
  if (e.key === 'g' && e.ctrlKey && e.shiftKey) {
    pageNumberOffset = 0;
    showToast('页码偏移已清除');
    saveConfig();
    return;
  }
});
```

### 阶段四：其他功能（1 周）

#### 3.12 文字选取模式（J）
**实现要点**：
- 按 J 进入/退出文字选取模式
- 选中文本后可右键复制
- Esc 退出模式

#### 3.13 全局重置（Ctrl+Shift+R）
**实现要点**：
- 弹出确认对话框
- 清除所有配置（书签、批注、页码偏移、Home 页等）
- 重新渲染页面

---

## 4. 技术实现建议

### 4.1 键盘事件管理
Readest 基于 Web 技术，建议使用统一的键盘事件管理器：

```typescript
class KeyboardManager {
  private handlers: Map<string, (e: KeyboardEvent) => void> = new Map();
  
  register(key: string, handler: (e: KeyboardEvent) => void) {
    this.handlers.set(key, handler);
  }
  
  init() {
    document.addEventListener('keydown', (e) => {
      const key = this.getKeyString(e);
      const handler = this.handlers.get(key);
      if (handler) {
        e.preventDefault();
        handler(e);
      }
    });
  }
  
  private getKeyString(e: KeyboardEvent): string {
    const parts: string[] = [];
    if (e.ctrlKey) parts.push('Ctrl');
    if (e.altKey) parts.push('Alt');
    if (e.shiftKey) parts.push('Shift');
    parts.push(e.key.toLowerCase());
    return parts.join('+');
  }
}
```

### 4.2 状态持久化
Readest 已有云同步功能，可以将 TactiReader 的配置数据整合到现有存储结构：

```typescript
interface TactiReaderConfig {
  // 书签
  bookmarks: Record<string, { page: number; name?: string }>;
  instantBookmarks: Record<string, { page: number; name?: string }>;
  
  // 批注
  annotations: Record<string, Annotation[]>;
  
  // 导航
  homePage: number;
  pageNumberOffset: number;
  flipMultiplier: number;
  
  // 视图
  pageRotations: Record<string, number>;
  
  // 主题
  theme: string;
  penColorIndex: number;
  rectColorIndex: number;
  textColorIndex: number;
}
```

### 4.3 UI 反馈
使用 Toast 提示用户操作结果：

```typescript
function showToast(message: string, duration = 2000) {
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.classList.add('fade-out');
    setTimeout(() => toast.remove(), 300);
  }, duration);
}
```

---

## 5. 测试要点

### 5.1 快捷键冲突检测
- 检查 TactiReader 快捷键与 Readest 现有快捷键是否冲突
- 冲突时优先保留 Readest 原有快捷键，TactiReader 功能改用其他键

### 5.2 批注兼容性
- 确保 TactiReader 批注格式与 Readest 现有批注格式兼容
- 或提供转换工具

### 5.3 性能测试
- 大量批注（1000+ 条）时的渲染性能
- 大文件（1000+ 页）时的翻页性能

### 5.4 跨平台测试
- Windows/macOS/Linux 桌面端
- Android/iOS 移动端（触控操作适配）

---

## 6. 参考资源

- TactiReader 源码：`c:\Users\Administrator\Desktop\ml\tacti-reader-master\tacti-reader-master\tactireader.py`
- Readest 官方文档：https://readest.com
- Readest GitHub：https://github.com/readest/readest

---

**文档版本**：v1.0  
**创建日期**：2026-06-19  
**最后更新**：2026-06-19  
**作者**：TactiReader 开发团队
