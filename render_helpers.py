import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

FONT_B = '/System/Library/Fonts/STHeiti Medium.ttc'
FONT_R = '/System/Library/Fonts/Hiragino Sans GB.ttc'
FONT_LAT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'

BG_ICE = (243, 250, 255, 255)         # #F3FAFF
BLUE_SIGNATURE = (121, 199, 242, 255) # #79C7F2
BLUE_DEEP = (16, 42, 67, 255)          # #102A43
BLUE_MIST = (216, 234, 244, 255)       # #D8EAF4
TEAL_ACCENT = (40, 184, 168, 255)      # #28B8A8
ORANGE_ACCENT = (255, 180, 92, 255)    # #FFB45C
WHITE = (255, 255, 255, 255)

def ft(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)

def draw_grid(im, step=54, color=(216, 234, 244, 140)):
    d = ImageDraw.Draw(im)
    W, H = im.size
    for x in range(0, W, step):
        d.line([(x, 0), (x, H)], fill=color, width=1)
    for y in range(0, H, step):
        d.line([(0, y), (W, y)], fill=color, width=1)

def draw_xiaozhi_brand(im, xy, height=44):
    brand = Image.open('assets/xiaozhi-brand-clean.png').convert('RGBA')
    scale = height / brand.height
    w, h = int(brand.width * scale), int(brand.height * scale)
    brand_resized = brand.resize((w, h), Image.Resampling.LANCZOS)
    im.alpha_composite(brand_resized, xy)
