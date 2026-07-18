import os
import sys


APP_NAME = "TactiReader"
BOOKMARK_DIR_NAME = "tactireader_bookmarks"


def _get_app_dir():
    """获取程序根目录（exe 所在目录 或 开发模式的项目根目录）"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 便携模式：配置始终存放在程序根目录的 data 下，换电脑直接拷走
CONFIG_DIR = os.path.join(_get_app_dir(), "data", BOOKMARK_DIR_NAME)
os.makedirs(CONFIG_DIR, exist_ok=True)

GLOBAL_CONFIG_FILE = os.path.join(CONFIG_DIR, "global_settings.json")
RENDER_SCALE = 2.0

PEN_COLOR_PRESETS = [
    (255, 0, 0),       # 1 纯正红 #FF0000
    (245, 124, 0),     # 2 琥珀橙 #F57C00
    (230, 74, 25),     # 3 朱红 #E64A19
    (0, 137, 123),     # 4 青绿 #00897B
    (30, 136, 229),    # 5 蔚蓝 #1E88E5
    (67, 160, 71),     # 6 翠绿 #43A047
    (156, 39, 176),    # 7 紫罗兰 #9C27B0
    (69, 90, 100),     # 8 蓝灰色 #455A64
    (109, 76, 65),     # 9 巧克力棕 #6D4C41
]

PEN_COLOR_NAMES = [
    "纯正红",
    "琥珀橙",
    "朱红",
    "青绿",
    "蔚蓝",
    "翠绿",
    "紫罗兰",
    "蓝灰色",
    "巧克力棕",
]

RECT_COLOR_PRESETS = [
    (255, 0, 0, 128),       # 1 纯正红 #FF0000
    (245, 124, 0, 128),     # 2 琥珀橙 #F57C00
    (230, 74, 25, 128),     # 3 朱红 #E64A19
    (0, 137, 123, 128),     # 4 青绿 #00897B
    (30, 136, 229, 128),    # 5 蔚蓝 #1E88E5
    (67, 160, 71, 128),     # 6 翠绿 #43A047
    (156, 39, 176, 128),    # 7 紫罗兰 #9C27B0
    (69, 90, 100, 128),     # 8 蓝灰色 #455A64
    (109, 76, 65, 128),     # 9 巧克力棕 #6D4C41
]

RECT_COLOR_NAMES = [
    "纯正红",
    "琥珀橙",
    "朱红",
    "青绿",
    "蔚蓝",
    "翠绿",
    "紫罗兰",
    "蓝灰色",
    "巧克力棕",
]

TEXT_COLOR_PRESETS = [
    (255, 0, 0),       # 1 纯正红 #FF0000
    (245, 124, 0),     # 2 琥珀橙 #F57C00
    (230, 74, 25),     # 3 朱红 #E64A19
    (0, 137, 123),     # 4 青绿 #00897B
    (30, 136, 229),    # 5 蔚蓝 #1E88E5
    (67, 160, 71),     # 6 翠绿 #43A047
    (156, 39, 176),    # 7 紫罗兰 #9C27B0
    (69, 90, 100),     # 8 蓝灰色 #455A64
    (109, 76, 65),     # 9 巧克力棕 #6D4C41
]

TEXT_COLOR_NAMES = [
    "纯正红",
    "琥珀橙",
    "朱红",
    "青绿",
    "蔚蓝",
    "翠绿",
    "紫罗兰",
    "蓝灰色",
    "巧克力棕",
]
