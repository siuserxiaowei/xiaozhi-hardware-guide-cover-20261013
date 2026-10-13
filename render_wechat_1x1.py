import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from render_helpers import (
    FONT_B, FONT_R, BG_ICE, BLUE_SIGNATURE, BLUE_DEEP, BLUE_MIST,
    TEAL_ACCENT, ORANGE_ACCENT, WHITE, ft, draw_grid, draw_xiaozhi_brand
)

def render_wechat_1x1():
    W, H = 1080, 1080
    im = Image.new('RGBA', (W, H), BG_ICE)
    draw_grid(im, step=54, color=(216, 234, 244, 130))
    d = ImageDraw.Draw(im)

    # 1. Header Brand
    draw_xiaozhi_brand(im, (64, 56), height=48)

    # 2. Main Title
    f_t1 = ft(FONT_B, 84)
    f_t2 = ft(FONT_B, 72)
    d.text((64, 128), "小智 AI 硬件复刻", font=f_t1, fill=BLUE_DEEP)
    d.text((64, 230), "ESP32-S3 选购大全", font=f_t2, fill=(24, 114, 204, 255))

    # 3. Subtitle Pill
    f_sub = ft(FONT_B, 26)
    sub_text = "面包板方案 · 避坑选型 · Personal Agent 选件"
    bb = d.textbbox((0, 0), sub_text, font=f_sub)
    tw, th = bb[2] - bb[0] + 32, bb[3] - bb[1] + 16
    d.rounded_rectangle((64, 330, 64 + tw, 330 + th), radius=14, fill=(232, 246, 255, 255), outline=BLUE_SIGNATURE, width=2)
    d.text((80, 338), sub_text, font=f_sub, fill=BLUE_DEEP)

    # 4. Left Side Real Breadboard Assembly Card
    bb_img = Image.open('assets/breadboard-hardware.png').convert('RGBA')
    bb_crop = bb_img.crop((110, 150, bb_img.width - 60, bb_img.height - 100))
    bb_fit = ImageOps.fit(bb_crop, (440, 480), method=Image.Resampling.LANCZOS)
    
    bx, by = 64, 420
    d.rounded_rectangle((bx, by, bx + 440, by + 480), radius=24, fill=(255, 255, 255, 255), outline=BLUE_SIGNATURE, width=3)
    im.alpha_composite(bb_fit, (bx, by))
    
    # Tag
    d.rounded_rectangle((bx + 16, by + 16, bx + 160, by + 56), radius=12, fill=(16, 42, 67, 230))
    d.text((bx + 26, by + 24), "免焊接实测试装", font=ft(FONT_B, 18), fill=WHITE)

    # 5. Right Side Xiaowei Creator Authority Card
    xw_src = Image.open('/Users/siuserxiaowei/self_media_design_kit/photo_main_square.png').convert('RGBA')
    xw_fit = ImageOps.fit(xw_src, (470, 480), method=Image.Resampling.LANCZOS, centering=(0.5, 0.4))
    
    xx, xy = 546, 420
    d.rounded_rectangle((xx, xy, xx + 470, xy + 480), radius=24, fill=(255, 255, 255, 255), outline=BLUE_SIGNATURE, width=3)
    im.alpha_composite(xw_fit, (xx, xy))
    
    # Author tag
    d.rounded_rectangle((xx + 16, xy + 480 - 64, xx + 450, xy + 480 - 14), radius=16, fill=(16, 42, 67, 235))
    d.text((xx + 32, xy + 480 - 52), "siuser小伟 · 硬件实测", font=ft(FONT_B, 24), fill=WHITE)
    d.ellipse((xx + 410, xy + 480 - 42, xx + 426, xy + 480 - 26), fill=ORANGE_ACCENT)

    # 6. Bottom Clean Status Pill
    d.rounded_rectangle((64, 940, 1016, 1020), radius=18, fill=(16, 42, 67, 245))
    d.text((90, 962), "乐鑫原厂模组 N16R8 · 拒绝 BGA 封装音频 · 支持飞书 MCP 联动", font=ft(FONT_R, 20), fill=WHITE)

    out_path = 'covers/variant-wechat-1x1.png'
    im.save(out_path, quality=95)
    print(f"Saved {out_path}")

render_wechat_1x1()
