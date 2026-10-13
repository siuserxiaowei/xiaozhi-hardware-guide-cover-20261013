import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from render_helpers import (
    FONT_B, FONT_R, BG_ICE, BLUE_SIGNATURE, BLUE_DEEP, BLUE_MIST,
    TEAL_ACCENT, ORANGE_ACCENT, WHITE, ft, draw_grid, draw_xiaozhi_brand
)

def render_wechat_21x9():
    W, H = 2100, 900
    im = Image.new('RGBA', (W, H), BG_ICE)
    draw_grid(im, step=70, color=(216, 234, 244, 120))
    d = ImageDraw.Draw(im)

    # 1. Header Brand
    draw_xiaozhi_brand(im, (80, 56), height=52)

    # 2. Main Title (Left Area)
    f_t1 = ft(FONT_B, 92)
    f_t2 = ft(FONT_B, 78)
    d.text((80, 136), "小智 AI 硬件复刻指南", font=f_t1, fill=BLUE_DEEP)
    d.text((80, 252), "ESP32-S3 面包板选购与 Personal Agent 进阶", font=f_t2, fill=(24, 114, 204, 255))

    # 3. Subtitle Pill
    f_sub = ft(FONT_B, 30)
    sub_text = "零基础避坑 · 乐鑫原厂模组 N16R8 · 灵动圆屏/摄像头/舵机选件"
    bb = d.textbbox((0, 0), sub_text, font=f_sub)
    tw, th = bb[2] - bb[0] + 36, bb[3] - bb[1] + 18
    d.rounded_rectangle((80, 360, 80 + tw, 360 + th), radius=16, fill=(232, 246, 255, 255), outline=BLUE_SIGNATURE, width=2)
    d.text((98, 368), sub_text, font=f_sub, fill=BLUE_DEEP)

    # 4. Feature Cards Row (Middle-Left)
    cards = [
        ("ESP32-S3 WROOM-1", "乐鑫官方原厂模组 N16R8 · 16M+8M", TEAL_ACCENT),
        ("INMP441 麦克风", "MEMS 数字音频排针版 · 免电烙铁", BLUE_SIGNATURE),
        ("MAX98357A 功放", "拒绝廉价 BGA 封装 · 稳定输出", ORANGE_ACCENT),
        ("GC9A01 表情圆屏", "解锁 Personal Agent 拟人眼球动画", (130, 80, 220, 255))
    ]
    cx = 80
    cy = 440
    card_w = 340
    card_h = 180
    for title, desc, col in cards:
        d.rounded_rectangle((cx, cy, cx + card_w, cy + card_h), radius=20, fill=(255, 255, 255, 245), outline=BLUE_MIST, width=2)
        d.rounded_rectangle((cx + 6, cy + 12, cx + 12, cy + card_h - 12), radius=3, fill=col)
        d.text((cx + 24, cy + 24), title, font=ft(FONT_B, 24), fill=BLUE_DEEP)
        d.text((cx + 24, cy + 68), desc, font=ft(FONT_R, 17), fill=(70, 95, 120, 255))
        d.rounded_rectangle((cx + 24, cy + 124, cx + 130, cy + 156), radius=10, fill=(235, 245, 255, 255))
        d.text((cx + 34, cy + 130), "实测推荐", font=ft(FONT_B, 16), fill=(24, 114, 204, 255))
        cx += card_w + 24

    # Bottom Ledger Bar
    d.rounded_rectangle((80, 650, 1490, 820), radius=22, fill=(16, 42, 67, 240))
    d.text((110, 680), "小智硬件复刻 3 大黄金避坑准则", font=ft(FONT_B, 26), fill=WHITE)
    d.text((110, 726), "① 认准乐鑫官方原厂模组 ESP32-S3-WROOM-1/1U N16R8，拒买杂牌高发热板", font=ft(FONT_R, 20), fill=(200, 230, 255, 255))
    d.text((110, 764), "② 麦克风必买焊接好排针版本；功放严禁买 BGA 封装；喇叭选用 3W 腔体", font=ft(FONT_R, 20), fill=(200, 230, 255, 255))

    # 5. Middle-Right Hardware Assembly Preview Card
    bb_img = Image.open('assets/breadboard-hardware.png').convert('RGBA')
    bb_crop = bb_img.crop((110, 150, bb_img.width - 60, bb_img.height - 100))
    bb_fit = ImageOps.fit(bb_crop, (280, 360), method=Image.Resampling.LANCZOS)
    
    hx, hy = 1520, 440
    d.rounded_rectangle((hx, hy, hx + 280, hy + 380), radius=24, fill=(255, 255, 255, 255), outline=BLUE_SIGNATURE, width=3)
    im.alpha_composite(bb_fit, (hx, hy + 10))
    d.rounded_rectangle((hx + 12, hy + 20, hx + 160, hy + 58), radius=12, fill=(16, 42, 67, 230))
    d.text((hx + 22, hy + 28), "免焊接实测试装", font=ft(FONT_B, 18), fill=WHITE)

    # 6. Far Right Xiaowei Creator Photo
    xw_src = Image.open('/Users/siuserxiaowei/self_media_design_kit/photo_main_square.png').convert('RGBA')
    xw_fit = ImageOps.fit(xw_src, (240, 380), method=Image.Resampling.LANCZOS, centering=(0.5, 0.4))
    
    xx, xy = 1820, 440
    d.rounded_rectangle((xx, xy, xx + 240, xy + 380), radius=24, fill=(255, 255, 255, 255), outline=BLUE_SIGNATURE, width=3)
    im.alpha_composite(xw_fit, (xx, xy))
    d.rounded_rectangle((xx + 10, xy + 380 - 58, xx + 230, xy + 380 - 12), radius=14, fill=(16, 42, 67, 235))
    d.text((xx + 20, xy + 380 - 48), "siuser小伟 实测", font=ft(FONT_B, 20), fill=WHITE)

    # Top Right Chip Badge
    chip_img = Image.open('assets/esp32-s3-chip.png').convert('RGBA')
    chip_fit = ImageOps.contain(chip_img, (180, 220), method=Image.Resampling.LANCZOS)
    d.rounded_rectangle((1760, 56, 2040, 380), radius=22, fill=(255, 255, 255, 245), outline=BLUE_MIST, width=2)
    im.alpha_composite(chip_fit, (1810, 80))
    d.text((1820, 320), "ESP32-S3 原厂模组", font=ft(FONT_B, 20), fill=BLUE_DEEP)

    out_path = 'covers/variant-wechat-21x9.png'
    im.save(out_path, quality=95)
    print(f"Saved {out_path}")

render_wechat_21x9()
