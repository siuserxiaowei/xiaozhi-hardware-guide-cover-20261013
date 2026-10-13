import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from render_helpers import (
    FONT_B, FONT_R, BG_ICE, BLUE_SIGNATURE, BLUE_DEEP, BLUE_MIST,
    TEAL_ACCENT, ORANGE_ACCENT, WHITE, ft, draw_grid, draw_xiaozhi_brand
)

def render_variant_1():
    W, H = 1080, 1440
    im = Image.new('RGBA', (W, H), BG_ICE)
    draw_grid(im, step=54, color=(216, 234, 244, 130))
    d = ImageDraw.Draw(im)

    # 1. Header Brand: X 小智
    draw_xiaozhi_brand(im, (64, 60), height=48)

    # 2. Main Title
    f_t1 = ft(FONT_B, 86)
    f_t2 = ft(FONT_B, 80)
    d.text((64, 132), "小智 AI 硬件复刻", font=f_t1, fill=BLUE_DEEP)
    d.text((64, 234), "ESP32-S3 购买大全", font=f_t2, fill=(24, 114, 204, 255))

    # 3. Subtitle Tag
    f_sub = ft(FONT_B, 28)
    sub_text = "面包板方案 · 避坑选型 · 散件与集成套件清单"
    bb = d.textbbox((0, 0), sub_text, font=f_sub)
    tw, th = bb[2] - bb[0] + 36, bb[3] - bb[1] + 18
    d.rounded_rectangle((64, 342, 64 + tw, 342 + th), radius=16, fill=(232, 246, 255, 255), outline=BLUE_SIGNATURE, width=2)
    d.text((82, 350), sub_text, font=f_sub, fill=BLUE_DEEP)

    # 4. Hardware Real Preview Showcase (Left-Middle)
    bb_img = Image.open('assets/breadboard-hardware.png').convert('RGBA')
    bb_crop = bb_img.crop((100, 150, bb_img.width - 60, bb_img.height - 100))
    bb_resized = ImageOps.fit(bb_crop, (460, 460), method=Image.Resampling.LANCZOS)
    
    card_x, card_y = 64, 420
    d.rounded_rectangle((card_x, card_y, card_x + 480, card_y + 480), radius=28, fill=(255, 255, 255, 250), outline=BLUE_SIGNATURE, width=3)
    im.alpha_composite(bb_resized, (card_x + 10, card_y + 10))
    
    # Badge on top of hardware photo
    f_badge = ft(FONT_B, 22)
    d.rounded_rectangle((card_x + 20, card_y + 20, card_x + 175, card_y + 60), radius=12, fill=(16, 42, 67, 230))
    d.text((card_x + 32, card_y + 27), "实测免焊接样机", font=f_badge, fill=WHITE)

    # 5. Component checklist pills / nodes (Right-Middle)
    pills = [
        ("ESP32-S3 WROOM-1", "乐鑫官方原厂模组 N16R8", TEAL_ACCENT),
        ("INMP441 麦克风", "MEMS 数字音频排针版", BLUE_SIGNATURE),
        ("MAX98357A 功放", "拒绝BGA封装 · 避坑推荐", ORANGE_ACCENT),
        ("腔体喇叭 3W", "4Ω/8Ω 高保真音频", BLUE_SIGNATURE),
        ("0.91寸 OLED 屏", "I2C 实时状态反馈", TEAL_ACCENT)
    ]
    px, py = 570, 420
    for name, desc, color in pills:
        d.rounded_rectangle((px, py, px + 446, py + 86), radius=18, fill=(255, 255, 255, 240), outline=BLUE_MIST, width=2)
        d.rounded_rectangle((px + 6, py + 12, px + 12, py + 74), radius=3, fill=color)
        d.text((px + 24, py + 14), name, font=ft(FONT_B, 24), fill=BLUE_DEEP)
        d.text((px + 24, py + 48), desc, font=ft(FONT_R, 19), fill=(80, 110, 135, 255))
        py += 98

    # 6. Xiaowei Authority Portrait Anchor (Bottom-Right)
    xw_src = Image.open('/Users/siuserxiaowei/self_media_design_kit/photo_main_square.png').convert('RGBA')
    xw_w, xw_h = 430, 430
    xw_fit = ImageOps.fit(xw_src, (xw_w, xw_h), method=Image.Resampling.LANCZOS, centering=(0.5, 0.4))
    
    xw_card_x, xw_card_y = 586, 940
    d.rounded_rectangle((xw_card_x, xw_card_y, xw_card_x + xw_w + 16, xw_card_y + xw_h + 16), radius=28, fill=(255, 255, 255, 255), outline=BLUE_SIGNATURE, width=3)
    im.alpha_composite(xw_fit, (xw_card_x + 8, xw_card_y + 8))
    
    # Creator Badge
    d.rounded_rectangle((xw_card_x + 20, xw_card_y + xw_h - 60, xw_card_x + xw_w - 4, xw_card_y + xw_h + 4), radius=16, fill=(16, 42, 67, 235))
    d.text((xw_card_x + 36, xw_card_y + xw_h - 50), "siuser小伟 · 硬件实测", font=ft(FONT_B, 24), fill=WHITE)
    d.ellipse((xw_card_x + xw_w - 36, xw_card_y + xw_h - 40, xw_card_x + xw_w - 20, xw_card_y + xw_h - 24), fill=ORANGE_ACCENT)

    # 7. Left-Bottom High-Value Summary Card
    sum_x, sum_y = 64, 940
    d.rounded_rectangle((sum_x, sum_y, sum_x + 490, sum_y + 446), radius=28, fill=(255, 255, 255, 240), outline=BLUE_MIST, width=2)
    # Header inside card
    d.rounded_rectangle((sum_x, sum_y, sum_x + 490, sum_y + 70), radius=28, fill=(24, 114, 204, 255))
    d.rectangle((sum_x, sum_y + 40, sum_x + 490, sum_y + 70), fill=(24, 114, 204, 255))
    d.text((sum_x + 28, sum_y + 18), "新手 DIY 关键避坑要点", font=ft(FONT_B, 26), fill=WHITE)

    points = [
        "1. 认准官方模组 ESP32-S3-WROOM-1 N16R8",
        "2. 果云版与乐鑫原厂版均为 16MB Flash + 8MB PSRAM",
        "3. 麦克风必买焊接排针版，免手焊直接插面包板",
        "4. 避坑警告：严禁买 BGA 封装音频芯片！",
        "5. 进阶升级：可拓展圆形彩屏、摄像头与舵机"
    ]
    pt_y = sum_y + 92
    for pt in points:
        color = (210, 45, 45, 255) if "避坑警告" in pt else BLUE_DEEP
        d.text((sum_x + 24, pt_y), pt, font=ft(FONT_R, 20), fill=color)
        pt_y += 66

    out_path = 'covers/variant-01-hardware-diy-3x4.png'
    im.save(out_path, quality=95)
    print(f"Saved {out_path}")

render_variant_1()
