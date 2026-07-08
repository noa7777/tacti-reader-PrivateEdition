import tkinter as tk
from tkinter import messagebox


def hex_to_rgb(hex_color):
    """将 #RRGGBB 转为 (R, G, B) 元组。"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb_tuple):
    """将 (R, G, B) 元组转回 #RRGGBB 字符串。"""
    return "#{:02x}{:02x}{:02x}".format(
        max(0, min(255, int(round(rgb_tuple[0])))),
        max(0, min(255, int(round(rgb_tuple[1])))),
        max(0, min(255, int(round(rgb_tuple[2]))))
    )


def transform_color(hex_color, W_hex, B_hex):
    """
    根据主题白色 W 和黑色 B，对基础颜色 hex_color 做逐通道线性映射。
    V_out = B_channel + (W_channel - B_channel) * (V_in / 255)
    """
    rgb_in = hex_to_rgb(hex_color)
    W = hex_to_rgb(W_hex)
    B = hex_to_rgb(B_hex)

    out = []
    for v_in, w, b in zip(rgb_in, W, B):
        v_out = b + (w - b) * (v_in / 255.0)
        v_out = round(v_out)
        v_out = max(0, min(255, v_out))
        out.append(v_out)

    return rgb_to_hex(tuple(out))


# 四组主题参数：白色 W，黑色 B
THEMES = {
    'light': ('#FFFFFF', '#141414'),
    'yellow': ('#F5EFD7', '#141412'),
    'green': ('#C7EDCC', '#101310'),
    'dark': ('#000000', '#ECECEC'),
}

# 基础调色板
PALETTE = {
    'bg': '#F5F5F5',
    'fg': '#1A1A1A',
    'button_bg': '#4A90D9',
    'button_fg': '#FFFFFF',
    'entry_bg': '#FFFFFF',
    'entry_fg': '#1A1A1A',
    'label_bg': '#F5F5F5',
    'label_fg': '#1A1A1A',
    'border': '#D9D9D9',
}


class ThemeDemoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter 主题切换演示")
        self.root.geometry("600x500")

        # 存储需要动态更新的控件：[(widget, widget_type, color_key), ...]
        # type 用于区分应该设置哪些属性
        self.theme_widgets = []

        self._build_menu()
        self._build_ui()
        self.apply_theme('light')

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="主题", menu=theme_menu)

        for name in THEMES:
            theme_menu.add_command(
                label=name.capitalize(),
                command=lambda n=name: self.apply_theme(n)
            )

    def _build_ui(self):
        # 顶部主题名称标签
        self.theme_label = tk.Label(self.root, text="当前主题：Light", font=("Microsoft YaHei", 14, "bold"))
        self.theme_label.pack(pady=20)
        self.theme_widgets.append((self.theme_label, 'label', 'label'))

        # 说明标签
        desc = tk.Label(
            self.root,
            text="这是一个主题切换演示。通过菜单切换主题，所有颜色均由统一公式映射生成。",
            font=("Microsoft YaHei", 11),
            wraplength=520,
            justify="left"
        )
        desc.pack(pady=10, padx=30)
        self.theme_widgets.append((desc, 'label', 'label'))

        # 按钮
        btn = tk.Button(
            self.root,
            text="点击我",
            font=("Microsoft YaHei", 12),
            command=self._on_button_click
        )
        btn.pack(pady=15)
        self.theme_widgets.append((btn, 'button', 'button'))

        # 输入框
        entry_frame = tk.Frame(self.root, highlightthickness=1)
        entry_frame.pack(pady=15, padx=30, fill="x")
        self.theme_widgets.append((entry_frame, 'frame', 'frame'))

        entry_label = tk.Label(entry_frame, text="输入框：", font=("Microsoft YaHei", 11))
        entry_label.pack(side="left", padx=(10, 5), pady=10)
        self.theme_widgets.append((entry_label, 'label', 'label'))

        self.entry = tk.Entry(entry_frame, font=("Microsoft YaHei", 11))
        self.entry.insert(0, "在这里输入文字...")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=10)
        self.theme_widgets.append((self.entry, 'entry', 'entry'))

        # 带边框的 Frame
        info_frame = tk.Frame(self.root, highlightthickness=2, relief="solid")
        info_frame.pack(pady=20, padx=30, fill="both", expand=True)
        self.theme_widgets.append((info_frame, 'frame', 'frame'))

        info_title = tk.Label(
            info_frame,
            text="说明区域",
            font=("Microsoft YaHei", 12, "bold")
        )
        info_title.pack(pady=(15, 10))
        self.theme_widgets.append((info_title, 'label', 'label'))

        info_text = tk.Label(
            info_frame,
            text="所有颜色都来自基础调色板，通过公式映射到当前主题的黑白之间。\n"
                 "因此暗色主题会自动反转，黄色/绿色主题也会自然适配。",
            font=("Microsoft YaHei", 10),
            wraplength=480,
            justify="left"
        )
        info_text.pack(pady=10, padx=20)
        self.theme_widgets.append((info_text, 'label', 'label'))

        # 底部状态栏
        self.status = tk.Label(self.root, text="就绪", font=("Microsoft YaHei", 10), bd=1, relief="sunken")
        self.status.pack(side="bottom", fill="x")
        self.theme_widgets.append((self.status, 'label', 'label'))

    def _on_button_click(self):
        messagebox.showinfo("提示", "按钮被点击了！")

    def apply_theme(self, theme_name):
        W_hex, B_hex = THEMES[theme_name]

        # 计算映射后的颜色
        colors = {key: transform_color(value, W_hex, B_hex) for key, value in PALETTE.items()}

        # 主窗口背景
        self.root.configure(bg=colors['bg'])

        # 更新所有记录的控件
        for widget, widget_type, _ in self.theme_widgets:
            if widget_type == 'label':
                widget.configure(bg=colors['label_bg'], fg=colors['label_fg'])
            elif widget_type == 'button':
                widget.configure(bg=colors['button_bg'], fg=colors['button_fg'],
                                 activebackground=colors['button_bg'],
                                 activeforeground=colors['button_fg'])
            elif widget_type == 'entry':
                widget.configure(bg=colors['entry_bg'], fg=colors['entry_fg'],
                                 insertbackground=colors['entry_fg'])
            elif widget_type == 'frame':
                widget.configure(bg=colors['bg'], highlightbackground=colors['border'])

        # 更新当前主题名称显示
        self.theme_label.configure(text=f"当前主题：{theme_name.capitalize()}")
        self.status.configure(text=f"已切换到 {theme_name.capitalize()} 主题")


def main():
    root = tk.Tk()
    app = ThemeDemoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
