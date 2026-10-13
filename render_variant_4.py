import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from render_helpers import (
    FONT_B, FONT_R, BG_ICE, BLUE_SIGNATURE, BLUE_DEEP, BLUE_MIST,
    TEAL_ACCENT, ORANGE_ACCENT, WHITE, ft, draw_grid, draw_xiaozhi_brand
)

def render_variant_4():
    W, H = 1080, 1440
    LAVENDER_BG = (248, 246, 255, 255) # #F8F6FF
    LAVENDER_GRID = (229, 222, 247, 160) # #E5DEF7
    PURPLE_INK = (50, 37, 94, 255) # #32255E
    VIOLET_SIGNATURE = (167, 139, 250, 255) # #A78BFA
    
    im = Image.new('RGBA', (W, H), LAVENDER_BG)
    draw_grid(im, step=54, color=LAVENDER_GRID)
    d = ImageDraw.Draw(im)

    # 1. Header Brand: X 小智
    draw_xiaozhi_brand(im, (64, 54), height=44)

    # 2. Main Title
    f_t1 = ft(FONT_B, 82)
    f_t2 = ft(FONT_B, 74)
    d.text((64, 124), "手把手捏一个", font=f_t1, fill=PURPLE_INK)
    d.text((64, 222), "物理桌面 Personal Agent", font=f_t2, fill=VIOLET_SIGNATURE)

    # 3. Subtitle Pill
    f_sub = ft(FONT_B, 26)
    sub_text = "从 ESP32 面包板到具身智能伴侣 · 全链路拆解"
    bb = d.textbbox((0, 0), sub_text, font=f_sub)
    tw, th = bb[2] - bb[0] + 32, bb[3] - bb[1] + 16
    d.rounded_rectangle((64, 320, 64 + tw, 320 + th), radius=14, fill=(240, 235, 255, 255), outline=VIOLET_SIGNATURE, width=2)
    d.text((80, 328), sub_text, font=f_sub, fill=PURPLE_INK)

    # 4. Central Visual Articulation: Clean Chibi Xiaowei
    chibi_img = Image.open('assets/chibi-clean-alpha.png').convert('RGBA')
    chibi_fit = ImageOps.contain(chibi_img, (400, 480), method=Image.Resampling.LANCZOS)

    # Chibi Showcase Glass Frame (Center-Left)
    c_card_x, c_card_y = 64, 400
    c_w, c_h = 470, 530
    d.rounded_rectangle((c_card_x, c_card_y, c_card_x + c_w, c_card_y + c_h), radius=28, fill=(255, 255, 255, 240), outline=VIOLET_SIGNATURE, width=3)
    
    # Place Chibi cleanly inside frame
    offset_x = c_card_x + (c_w - chibi_fit.width) // 2
    offset_y = c_card_y + (c_h - chibi_fit.height - 40) // 2
    im.alpha_composite(chibi_fit, (offset_x, offset_y))
    
    # Chibi Tag
    d.rounded_rectangle((c_card_x + 20, c_card_y + c_h - 60, c_card_x + 230, c_card_y + c_h - 14), radius=12, fill=PURPLE_INK)
    d.text((c_card_x + 36, c_card_y + c_h - 50), "小伟 IP 形象代言", font=ft(FONT_B, 20), fill=WHITE)

    # 5. Right Side: Architecture Flow Cards (Connecting to doc section 5)
    layers = [
        ("实体硬件终端", "ESP32-S3 + 灵动圆屏 + 麦克喇叭", TEAL_ACCENT),
        ("通信管道流", "WebSocket 双向音频 + 4G/WiFi", (24, 114, 204, 255)),
        ("智能服务端", "DeepSeek-V3 / Qwen + Mem0 记忆", VIOLET_SIGNATURE),
        ("MCP 连接中枢", "打通飞书待办/日历/电脑自动化", ORANGE_ACCENT)
    ]
    rx, ry = 566, 400
    for l_title, l_desc, col in layers:
        d.rounded_rectangle((rx, ry, rx + 450, ry + 114), radius=20, fill=(255, 255, 255, 245), outline=(225, 218, 245, 255), width=2)
        d.rounded_rectangle((rx + 8, ry + 14, rx + 16, ry + 100), radius=4, fill=col)
        d.text((rx + 30, ry + 22), l_title, font=ft(FONT_B, 24), fill=PURPLE_INK)
        d.text((rx + 30, ry + 64), l_desc, font=ft(FONT_R, 18), fill=(90, 80, 130, 255))
        ry += 138

    # 6. Lower Left: Playstyle Matrix Highlights
    mat_x, mat_y = 64, 960
    mat_w, mat_h = 470, 420
    d.rounded_rectangle((mat_x, mat_y, mat_x + mat_w, mat_y + mat_h), radius=26, fill=(255, 255, 255, 245), outline=VIOLET_SIGNATURE, width=2)
    d.rounded_rectangle((mat_x, mat_y, mat_x + mat_w, mat_y + 60), radius=26, fill=PURPLE_INK)
    d.rectangle((mat_x, mat_y + 30, mat_x + mat_w, mat_y + 60), fill=PURPLE_INK)
    d.text((mat_x + 24, mat_y + 16), "ESP32 个人智能体进化论", font=ft(FONT_B, 23), fill=WHITE)

    steps = [
        "1. 基础版：语音对话音箱（麦克+功放+喇叭）",
        "2. 具身版：灵动眼神圆屏 + 摸头触摸交互",
        "3. 动作版：微型舵机摇头点头肢体语言",
        "4. 多模态：摄像头工位识物 + 飞书 MCP 联动"
    ]
    sy = mat_y + 84
    for s in steps:
        d.text((mat_x + 20, sy), s, font=ft(FONT_R, 19), fill=PURPLE_INK)
        sy += 78

    # 7. Lower Right: Real Hardware Assembly Photo for Trust
    bb_img = Image.open('assets/breadboard-hardware.png').convert('RGBA')
    bb_crop = bb_img.crop((110, 150, bb_img.width - 60, bb_img.height - 100))
    bb_fit = ImageOps.fit(bb_crop, (450, 420), method=Image.Resampling.LANCZOS)
    
    hr_x, hr_y = 566, 960
    d.rounded_rectangle((hr_x, hr_y, hr_x + 450, hr_y + 420), radius=26, fill=(255, 255, 255, 255), outline=VIOLET_SIGNATURE, width=3)
    im.alpha_composite(bb_fit, (hr_x, hr_y))
    
    # Overlay Tag
    d.rounded_rectangle((hr_x + 16, hr_y + 16, hr_x + 180, hr_y + 56), radius=12, fill=(50, 37, 94, 230))
    d.text((hr_x + 28, hr_y + 24), "实测免焊接面包板", font=ft(FONT_B, 18), fill=WHITE)
    
    d.rounded_rectangle((hr_x + 16, hr_y + 420 - 58, hr_x + 450 - 16, hr_y + 420 - 14), radius=14, fill=(50, 37, 94, 235))
    d.text((hr_x + 28, hr_y + 420 - 48), "siuser小伟 · 具身智能探索", font=ft(FONT_B, 22), fill=WHITE)

    out_path = 'covers/variant-04-chibi-visual-3x4.png'
    im.save(out_path, quality=95)
    print(f"Saved {out_path}")

render_variant_4()
