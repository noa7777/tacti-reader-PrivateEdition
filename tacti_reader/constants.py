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
    (224, 85, 85),   # 亮红 #E05555
    (74, 143, 224),  # 亮蓝 #4A8FE0
    (168, 108, 200), # 亮紫 #A86CC8
    (240, 138, 154), # 粉红 #F08A9A
    (91, 192, 222),  # 亮青 #5BC0DE
    (230, 168, 122), # 暖杏橙 #E6A87A
    (168, 200, 154), # 浅鼠尾草绿 #A8C89A
    (212, 200, 122), # 淡米黄 #D4C87A
    (166, 139, 122), # 暖灰褐 #A68B7A
    (158, 158, 158), # 中性灰 #9E9E9E
]

RECT_COLOR_PRESETS = [
    (212, 163, 115, 128), # 金盏菊黄 #D4A373
    (217, 122, 92, 128),  # 珊瑚橙 #D97A5C
    (181, 131, 141, 128), # 玫瑰粉褐 #B5838D
    (128, 178, 145, 128), # 鼠尾草绿 #80B291
    (155, 158, 143, 128), # 橄榄灰 #9B9E8F
    (197, 139, 107, 128), # 杏色 #C58B6B
    (166, 156, 172, 128), # 薰衣草灰 #A69CAC
    (181, 107, 107, 128), # 砖红 #B56B6B
]

TEXT_COLOR_PRESETS = [
    (224, 85, 85),   # 亮红 #E05555
    (74, 143, 224),  # 亮蓝 #4A8FE0
    (168, 108, 200), # 亮紫 #A86CC8
    (139, 90, 43),   # 正棕 #8B5A2B
    (125, 168, 125), # 柔绿 #7DA87D
    (214, 154, 106), # 暖橙 #D69A6A
]
