import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from render_helpers import (
    FONT_B, FONT_R, BG_ICE, BLUE_SIGNATURE, BLUE_DEEP, BLUE_MIST,
    TEAL_ACCENT, ORANGE_ACCENT, WHITE, ft, draw_grid, draw_xiaozhi_brand
)

def render_variant_3():
    W, H = 1280, 720
    im = Image.new('RGBA', (W, H), BG_ICE)
    draw_grid(im, step=50, color=(216, 234, 244, 120))
    d = ImageDraw.Draw(im)

    # 1. Header Brand: X 小智
    draw_xiaozhi_brand(im, (56, 44), height=40)

    # 2. Left Title Area
    f_t1 = ft(FONT_B, 64)
    f_t2 = ft(FONT_B, 56)
    d.text((56, 102), "小智 AI ESP32-S3", font=f_t1, fill=BLUE_DEEP)
    d.text((56, 182), "硬件开发板+面包板选购大全", font=f_t2, fill=(24, 114, 204, 255))

    # 3. Subtitle Pill
    f_sub = ft(FONT_B, 22)
    sub_text = "零基础 DIY 避坑指南 · 乐鑫原厂模组 · 核心元件清单"
    bb = d.textbbox((0, 0), sub_text, font=f_sub)
    tw, th = bb[2] - bb[0] + 28, bb[3] - bb[1] + 14
    d.rounded_rectangle((56, 264, 56 + tw, 264 + th), radius=12, fill=(232, 246, 255, 255), outline=BLUE_SIGNATURE, width=2)
    d.text((70, 271), sub_text, font=f_sub, fill=BLUE_DEEP)

    # 4. Left Hardware Spec Comparison Card
    card_x, card_y = 56, 330
    card_w, card_h = 490, 340
    d.rounded_rectangle((card_x, card_y, card_x + card_w, card_y + card_h), radius=22, fill=(255, 255, 255, 245), outline=BLUE_MIST, width=2)
    d.rounded_rectangle((card_x, card_y, card_x + card_w, card_y + 50), radius=22, fill=BLUE_DEEP)
    d.rectangle((card_x, card_y + 28, card_x + card_w, card_y + 50), fill=BLUE_DEEP)
    d.text((card_x + 20, card_y + 12), "核心主控与音频链路必看", font=ft(FONT_B, 22), fill=WHITE)

    specs = [
        ("ESP32-S3 WROOM-1", "乐鑫官方原厂模组 / N16R8 (16M+8M)"),
        ("果云版 / 乐鑫标准版", "42/44 引脚均支持 · 信号稳定"),
        ("INMP441 麦克风", "MEMS 数字音频 · 必买焊接排针版"),
        ("MAX98357A 功放", "严禁买廉价 BGA 封装 · 选支持型号"),
        ("腔体喇叭 / 0.91\"屏", "4Ω/8Ω 3W 喇叭 · I2C 实时状态屏")
    ]
    sy = card_y + 68
    for name, desc in specs:
        d.text((card_x + 18, sy), name, font=ft(FONT_B, 18), fill=(24, 114, 204, 255))
        d.text((card_x + 18, sy + 24), desc, font=ft(FONT_R, 15), fill=(70, 95, 120, 255))
        sy += 52

    # 5. Middle Real Breadboard Photo Card
    bb_img = Image.open('assets/breadboard-hardware.png').convert('RGBA')
    bb_crop = bb_img.crop((120, 150, bb_img.width - 60, bb_img.height - 100))
    bb_resized = ImageOps.fit(bb_crop, (330, 330), method=Image.Resampling.LANCZOS)
    
    mid_x, mid_y = 570, 330
    d.rounded_rectangle((mid_x, mid_y, mid_x + 346, mid_y + 340), radius=22, fill=(255, 255, 255, 255), outline=BLUE_SIGNATURE, width=3)
    im.alpha_composite(bb_resized, (mid_x + 8, mid_y + 5))
    
    # Label badge on photo
    d.rounded_rectangle((mid_x + 16, mid_y + 14, mid_x + 150, mid_y + 48), radius=10, fill=(16, 42, 67, 230))
    d.text((mid_x + 26, mid_y + 20), "免焊接实测试装", font=ft(FONT_B, 18), fill=WHITE)

    # 6. Right Xiaowei Creator Authority Card
    xw_src = Image.open('/Users/siuserxiaowei/self_media_design_kit/photo_discussion_16x9.png').convert('RGBA')
    xw_w, xw_h = 320, 340
    xw_fit = ImageOps.fit(xw_src, (xw_w, xw_h), method=Image.Resampling.LANCZOS, centering=(0.55, 0.5))
    
    rx, ry = 936, 330
    d.rounded_rectangle((rx, ry, rx + xw_w, ry + xw_h), radius=22, fill=(255, 255, 255, 255), outline=BLUE_SIGNATURE, width=3)
    im.alpha_composite(xw_fit, (rx, ry))
    
    # Author tag banner
    d.rounded_rectangle((rx + 12, ry + xw_h - 56, rx + xw_w - 12, ry + xw_h - 10), radius=14, fill=(16, 42, 67, 235))
    d.text((rx + 24, ry + xw_h - 46), "siuser小伟 · 硬件实测", font=ft(FONT_B, 20), fill=WHITE)
    d.ellipse((rx + xw_w - 32, ry + xw_h - 38, rx + xw_w - 20, ry + xw_h - 26), fill=ORANGE_ACCENT)

    # 7. Top Right Mini Chip Badge
    chip_img = Image.open('assets/esp32-s3-chip.png').convert('RGBA')
    chip_fit = ImageOps.contain(chip_img, (140, 160), method=Image.Resampling.LANCZOS)
    cx, cy = 970, 44
    d.rounded_rectangle((cx, cy, cx + 286, cy + 180), radius=18, fill=(255, 255, 255, 245), outline=BLUE_MIST, width=2)
    im.alpha_composite(chip_fit, (cx + 10, cy + 10))
    d.text((cx + 140, cy + 40), "ESP32-S3", font=ft(FONT_B, 22), fill=BLUE_DEEP)
    d.text((cx + 140, cy + 74), "WROOM-1", font=ft(FONT_B, 20), fill=(24, 114, 204, 255))
    d.text((cx + 140, cy + 108), "官方原厂模组", font=ft(FONT_R, 17), fill=TEAL_ACCENT)

    out_path = 'covers/variant-03-video-field-16x9.png'
    im.save(out_path, quality=95)
    print(f"Saved {out_path}")

render_variant_3()
