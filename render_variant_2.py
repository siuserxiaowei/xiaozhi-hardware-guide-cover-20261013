import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from render_helpers import (
    FONT_B, FONT_R, BG_ICE, BLUE_SIGNATURE, BLUE_DEEP, BLUE_MIST,
    TEAL_ACCENT, ORANGE_ACCENT, WHITE, ft, draw_grid, draw_xiaozhi_brand
)

def render_variant_2():
    W, H = 1080, 1440
    im = Image.new('RGBA', (W, H), BG_ICE)
    draw_grid(im, step=54, color=(216, 234, 244, 130))
    d = ImageDraw.Draw(im)

    # 1. Header Brand: X 小智
    draw_xiaozhi_brand(im, (64, 54), height=44)

    # 2. Main Title (Two compact lines)
    f_t1 = ft(FONT_B, 76)
    f_t2 = ft(FONT_B, 68)
    d.text((64, 118), "小智 AI 进阶硬件选件", font=f_t1, fill=BLUE_DEEP)
    d.text((64, 208), "解锁 Personal Agent 实体形态", font=f_t2, fill=(24, 114, 204, 255))

    # 3. Subtitle Tag
    f_sub = ft(FONT_B, 26)
    sub_text = "灵动圆屏 · 视觉摄像头 · 微动舵机 · 触摸与移动供电"
    bb = d.textbbox((0, 0), sub_text, font=f_sub)
    tw, th = bb[2] - bb[0] + 32, bb[3] - bb[1] + 16
    d.rounded_rectangle((64, 298, 64 + tw, 298 + th), radius=14, fill=(232, 246, 255, 255), outline=BLUE_SIGNATURE, width=2)
    d.text((80, 306), sub_text, font=f_sub, fill=BLUE_DEEP)

    # 4. Core 4 Agent Upgrades Grid (Center Area)
    modules = [
        ("灵动表情圆屏", "GC9A01 1.28寸圆形彩屏", "动态眼球动效 · 多维拟人眼神反馈", "12~18元", TEAL_ACCENT),
        ("视觉摄像头", "OV2640 / OV5640 模组", "多模态桌面识物 · 手势识别与排错", "10~18元", BLUE_SIGNATURE),
        ("微动舵机体态", "SG90 9g 微型舵机", "实体身体动作 · 点头/摇头/转头寻人", "4~7元", ORANGE_ACCENT),
        ("触控与移动供电", "TTP223触摸 + TP4056锂电", "摸头唤醒交互 · 解锁便携 AI Pin", "11~17元", (130, 80, 220, 255))
    ]
    
    gx, gy = 64, 380
    cw, ch = 460, 250
    for idx, (title, model, desc, price, color) in enumerate(modules):
        col = idx % 2
        row = idx // 2
        x = gx + col * (cw + 32)
        y = gy + row * (ch + 24)
        
        d.rounded_rectangle((x, y, x + cw, y + ch), radius=22, fill=(255, 255, 255, 245), outline=BLUE_MIST, width=2)
        # Top color banner
        d.rounded_rectangle((x, y, x + cw, y + 54), radius=22, fill=color)
        d.rectangle((x, y + 30, x + cw, y + 54), fill=color)
        d.text((x + 20, y + 14), title, font=ft(FONT_B, 24), fill=WHITE)
        # Price pill
        d.rounded_rectangle((x + cw - 120, y + 10, x + cw - 16, y + 44), radius=12, fill=(0, 0, 0, 50))
        d.text((x + cw - 110, y + 15), price, font=ft(FONT_B, 20), fill=WHITE)
        
        d.text((x + 20, y + 78), model, font=ft(FONT_B, 22), fill=BLUE_DEEP)
        d.text((x + 20, y + 124), desc, font=ft(FONT_R, 18), fill=(70, 95, 120, 255))
        d.text((x + 20, y + 176), "Personal Agent 具身模组", font=ft(FONT_B, 18), fill=color)

    # 5. Lower Left: Playstyle Matrix Highlights
    mat_x, mat_y = 64, 936
    mat_w, mat_h = 490, 444
    d.rounded_rectangle((mat_x, mat_y, mat_x + mat_w, mat_y + mat_h), radius=26, fill=(255, 255, 255, 245), outline=BLUE_SIGNATURE, width=2)
    d.rounded_rectangle((mat_x, mat_y, mat_x + mat_w, mat_y + 64), radius=26, fill=BLUE_DEEP)
    d.rectangle((mat_x, mat_y + 36, mat_x + mat_w, mat_y + 64), fill=BLUE_DEEP)
    d.text((mat_x + 24, mat_y + 17), "Personal Agent 四大前沿玩法", font=ft(FONT_B, 24), fill=WHITE)

    plays = [
        ("玩法1 · 工位效率物理副驾", "飞书日历/待办 MCP 联动 · CI/CD 语音实体告警"),
        ("玩法2 · 具身情感桌面宠物", "长期记忆 Mem0 · 声音克隆人设 · 动态眼神打盹"),
        ("玩法3 · 桌面多模态探针", "VLM 看懂电路阻值与走线 · 专注与健康提醒"),
        ("玩法4 · 随身实体 AI Pin", "ML307R 4G 模组 · 随身灵感速记与多语种翻译")
    ]
    py = mat_y + 86
    for p_title, p_desc in plays:
        d.text((mat_x + 22, py), p_title, font=ft(FONT_B, 21), fill=(24, 114, 204, 255))
        d.text((mat_x + 22, py + 30), p_desc, font=ft(FONT_R, 17), fill=(70, 95, 120, 255))
        py += 82

    # 6. Lower Right: Xiaowei Discussion Photo Anchor
    xw_src = Image.open('/Users/siuserxiaowei/self_media_design_kit/photo_main_square.png').convert('RGBA')
    xw_w, xw_h = 430, 444
    xw_fit = ImageOps.fit(xw_src, (xw_w, xw_h), method=Image.Resampling.LANCZOS, centering=(0.5, 0.4))
    
    xw_card_x, xw_card_y = 586, 936
    d.rounded_rectangle((xw_card_x, xw_card_y, xw_card_x + xw_w + 16, xw_card_y + xw_h), radius=26, fill=(255, 255, 255, 255), outline=BLUE_SIGNATURE, width=3)
    im.alpha_composite(xw_fit, (xw_card_x + 8, xw_card_y + 8))
    
    # Creator Badge
    d.rounded_rectangle((xw_card_x + 20, xw_card_y + xw_h - 64, xw_card_x + xw_w - 4, xw_card_y + xw_h - 4), radius=16, fill=(16, 42, 67, 235))
    d.text((xw_card_x + 36, xw_card_y + xw_h - 52), "siuser小伟 · 具身智能实测", font=ft(FONT_B, 23), fill=WHITE)
    d.ellipse((xw_card_x + xw_w - 36, xw_card_y + xw_h - 42, xw_card_x + xw_w - 20, xw_card_y + xw_h - 26), fill=ORANGE_ACCENT)

    out_path = 'covers/variant-02-agent-upgrades-3x4.png'
    im.save(out_path, quality=95)
    print(f"Saved {out_path}")

render_variant_2()
