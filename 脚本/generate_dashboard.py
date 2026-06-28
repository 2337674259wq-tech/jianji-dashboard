# -*- coding: utf-8 -*-
"""
可视化仪表盘 — Python 预渲染 HTML，JS 仅做过滤/切换
完全避免 f-string + JS 模板字符串转义冲突
"""
import json, os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(BASE, "仪表盘.html")

# ═══════════════ 对标链接库 ═══════════════
REFS = {
    "剪映基础操作": [
        ("陆一舟剪辑 · 剪映全套入门","https://www.douyin.com/search/陆一舟剪辑","体系最完整的剪映教学，零基础首选"),
        ("三郎老师 · 唠嗑式剪映教学","https://www.douyin.com/search/三郎老师剪映","接地气，完全零基础跟练"),
        ("路过我的生活 · 0基础入门","https://www.douyin.com/search/路过我的生活剪辑","全程无废话，音乐卡点+抠像拆解"),
    ],
    "转场特效": [
        ("丝滑转场·普通人抄作业","https://post.smzdm.com/p/axkwe574/","电影级转场平替，不用特效自然到犯规"),
        ("剪映最火10个转场动作详解","https://www.php.cn/faq/2589986.html","卡点闪白/左滑推进/色彩溶解等10种"),
        ("迷核转场·梦想核滤镜卡点","https://www.douyin.com/shipin/7645123592253900863","2026抖音热款转场模板"),
    ],
    "卡点节奏": [
        ("抖音自动卡点教程","https://17golang.com/article/573954.html","卡点拍摄+自动踩点完整指南"),
        ("旅游卡点视频制作全指南","https://post.smzdm.com/p/aomkm3r7/","从参数设置到剪辑调色全流程"),
        ("四分屏卡点教程·ahyeon风","https://www.douyin.com/shipin/7641791248625567763","画面分割定格+阶梯排列"),
    ],
    "调色教程": [
        ("80万人看过·电影感调色教程","https://post.smzdm.com/p/arlvkdqz/","氛围感+电影感调色实战拆解"),
        ("达芬奇电影感调色思路","https://post.smzdm.com/p/arlx04d7/","云桥饲羽博主·无LUT调色逻辑讲解"),
        ("重启色彩卡点教程","https://www.douyin.com/shipin/7617655798461859878","红点移动+蒙版扩散+饱和度渐变恢复"),
    ],
    "文字动画": [
        ("剪映文字动画·你喜欢的人是谁","https://post.smzdm.com/p/apq7g2v2/","逐字动画+关键帧全流程拆解"),
        ("电影感Vlog片头·蒙版+文字","https://post.smzdm.com/p/a262dx3q/","遮幅开场+文字向右擦开入场"),
    ],
    "蒙版&关键帧": [
        ("手机剪映关键帧10分钟速成","https://m.toutiao.com/article/7595576252665987626/","文字/画面/蒙版动画必学核心"),
        ("剪映矩形蒙版使用教程","https://www.douyin.com/video/7562405980719140142","蒙版基础操作详解"),
        ("剪映新版关键帧正确操作","https://www.douyin.com/video/7271196668698053899","0基础学新版关键帧逻辑"),
    ],
    "抠像&合成": [
        ("抖音AI抠像特效教程","https://www.douyin.com/search/剪映智能抠像教程","一键去背景+精细边缘调整"),
        ("剪映绿幕抠像+换背景","https://www.douyin.com/search/剪映绿幕抠像","在家拍出任意背景"),
    ],
    "音频处理": [
        ("抖音热门BGM卡点剪辑","https://www.douyin.com/search/抖音热门BGM卡点","曲库+本地导入+抖音收藏全攻略"),
    ],
    "拍摄技巧": [
        ("手持拍摄防抖5个技巧","https://www.douyin.com/search/手机拍摄防抖技巧","不用稳定器拍出稳定画面"),
        ("南门录像厅·剪辑思维+叙事","https://www.douyin.com/search/南门录像厅","拉片式教学，逐帧分析镜头衔接"),
        ("百万剪辑狮·爆款逻辑拆解","https://www.douyin.com/search/百万剪辑狮","揭秘爆款节奏和镜头衔接底层规律"),
    ],
    "热门跟拍": [
        ("2026抖音一键成片全攻略","https://m.toutiao.com/article/7615130900577272370/","AI高光筛选+智能卡点+自动字幕"),
        ("2026爆款视频剪映课·朱朱老师","https://www.doutianshi.com/51035.html","剪辑+AI+运营三大板块系统课"),
    ],
    "案例实战": [
        ("80万人看过的小爆款剪辑全流程","https://post.smzdm.com/p/arlvkdqz/","音乐卡点+曲线变速+背影转场完整拆解"),
        ("用手机+剪映复刻广告片","https://www.douyin.com/search/手机拍广告级视频","低成本拍出高级感实战"),
        ("普通人Vlog从拍到剪全流程","https://www.douyin.com/search/Vlog拍摄剪辑全流程","200段素材整理+剪辑思路"),
    ],
}

# ═══════════════ 帮助函数 ═══════════════
DIFF_MAP = {1:"⭐",2:"⭐⭐",3:"⭐⭐⭐",4:"⭐⭐⭐⭐",5:"⭐⭐⭐⭐⭐"}
TYPE_EMOJI = {"爆款":"🔺","干货":"🔸","深度":"🔹"}

def diff_badge(d):
    if d <= 2: return "green"
    if d <= 3: return "orange"
    return "red"

def type_badge(t):
    if t == "爆款": return "red"
    if t == "干货": return "blue"
    return "purple"

def stage_pill(stage):
    if "冷" in stage: return "green"
    if "增" in stage: return "blue"
    return "purple"

def make_script(t):
    """生成脚本文案"""
    title = t.get("title","")
    ctype = t.get("content_type","干货")
    if ctype == "爆款":
        core = title.split("：")[-1] if "：" in title else title
        return {
            "hook": f"「{core}」——你是不是也刷到过这种效果？今天30秒教会你。",
            "steps": ["📱 打开剪映，导入素材",f"⚡ 关键操作：{core}的核心步骤","🎯 微调参数到最佳效果","✨ 对比展示：Before → After"],
            "ending": "学会了点个赞收藏，下期见！",
            "bgm": "节奏卡点BGM（Phut Hon / 病变 Remix）"
        }
    elif ctype == "深度":
        return {
            "hook": f"今天不教单个技巧，带你完整拆解「{title}」的全过程。",
            "steps": ["📋 前期构思与策划思路","🎥 拍摄现场还原与要点","✂️ 剪辑全流程逐步拆解","📊 成片展示 + 关键技巧复盘"],
            "ending": "觉得有用的话点个关注，我会持续更新这样的深度拆解。",
            "bgm": "叙事感配乐（Epidemic Sound 风格）"
        }
    else:
        return {
            "hook": f"为什么别人的视频那么高级？问题就出在这一步——",
            "steps": [f"🔍 常见错误：90%的人都做错了",f"🛠️ 正确方法：{title}的核心要点","📐 具体操作演示","✅ 效果对比 + 避坑提醒"],
            "ending": "收藏起来慢慢练，关注我每天一个剪辑技巧。",
            "bgm": "轻量氛围BGM（Lo-Fi / Jazz Hop）"
        }

# ═══════════════ HTML 组件生成器 ═══════════════
def card_html(t, medal=""):
    """单张选题卡片 HTML（纯 Python 生成）"""
    cat = t.get("category","")
    ctype = t.get("content_type","干货")
    diff = t.get("difficulty",2)
    title = t.get("title","")
    dur = t.get("estimated_duration","?")
    viral = t.get("viral_potential","中")
    prod = t.get("production_time","?")
    desc = t.get("description","")
    mats = t.get("materials_needed","")
    tid = t.get("id","")

    tb = type_badge(ctype)
    db = diff_badge(diff)
    te = TYPE_EMOJI.get(ctype,"")

    # 素材标签
    mat_tags = ""
    if mats:
        for m in mats.replace("，",",").replace("、",",").split(","):
            m = m.strip()
            if m:
                mat_tags += f'<span class="mat-tag">{m}</span>'

    # 脚本
    scr = make_script(t)

    # 对标链接
    ref_list = REFS.get(cat, [])[:3]
    ref_html = ""
    if ref_list:
        for rtitle, rurl, rnote in ref_list:
            ref_html += f'<a class="ref-link" href="{rurl}" target="_blank" rel="noopener">{rtitle} <span class="arrow">↗</span><span class="ref-note">{rnote}</span></a>'
    else:
        ref_html = f'<div class="empty-note">🔍 建议在抖音搜索「{title}」找参考</div>'

    steps_html = ""
    for s in scr["steps"]:
        steps_html += f"<li>{s}</li>"

    return f"""<div class="card" data-id="{tid}" data-cat="{cat}" data-type="{ctype}" data-diff="{diff}" data-title="{title}" onclick="openDetail(this)" tabindex="0">
    <div class="card-body">
        <div class="tags">
            <span class="tag tag-{tb}">{te} {ctype}</span>
            <span class="tag tag-{db}">{DIFF_MAP.get(diff,'⭐⭐')}</span>
            <span class="tag tag-gray">{cat}</span>
        </div>
        <h3>{medal} {title}</h3>
        <div class="meta">
            <span>{dur}</span><span>涨粉{viral}</span><span>{prod}</span>
        </div>
    </div>
    <div class="chevron">→</div>
    <!-- hidden detail data -->
    <div class="detail-data" style="display:none">
        <div class="detail-title">{title}</div>
        <div class="detail-cat">{cat}</div>
        <div class="detail-type">{ctype}</div>
        <div class="detail-diff">{diff}</div>
        <div class="detail-dur">{dur}</div>
        <div class="detail-viral">{viral}</div>
        <div class="detail-prod">{prod}</div>
        <div class="detail-desc">{desc}</div>
        <div class="detail-hook">{scr['hook']}</div>
        <div class="detail-steps">{''.join(steps_html)}</div>
        <div class="detail-ending">{scr['ending']}</div>
        <div class="detail-bgm">{scr['bgm']}</div>
        <div class="detail-refs">{ref_html}</div>
        <div class="detail-mats">{mat_tags}</div>
    </div>
</div>"""


def cal_row_html(e):
    """日历表格行"""
    ep = e.get("episode","")
    title = e.get("title","")
    cat = e.get("category","")
    diff = e.get("difficulty",2)
    ctype = e.get("content_type","")
    dur = e.get("estimated_duration","")
    stage = e.get("stage","")
    sp = stage_pill(stage)
    return f"""<tr data-cat="{cat}" data-stage="{stage}" data-title="{title}" class="cal-row" onclick="openDetailByTitle('{title}')">
        <td class="ep">#{ep}</td>
        <td>{title}</td>
        <td>{cat}</td>
        <td>{DIFF_MAP.get(diff,'⭐⭐')}</td>
        <td>{ctype}</td>
        <td>{dur}</td>
        <td><span class="pill pill-{sp}">{stage}</span></td>
    </tr>"""


# ═══════════════ 主生成 ═══════════════
def build():
    db = json.load(open(os.path.join(BASE,"数据","选题库.json"),encoding="utf-8"))
    cal = json.load(open(os.path.join(BASE,"数据","200期日历.json"),encoding="utf-8"))
    pub = json.load(open(os.path.join(BASE,"数据","已发布.json"),encoding="utf-8"))

    topics = db["topics"]
    pending = [t for t in topics if t["status"]=="待发布"]
    published = [t for t in topics if t["status"]=="已发布"]
    skipped = [t for t in topics if t["status"]=="已跳过"]
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── 今日推荐 ──
    viral_p = [t for t in pending if t.get("content_type")=="爆款"]
    dry_p   = [t for t in pending if t.get("content_type")=="干货"]
    deep_p  = [t for t in pending if t.get("content_type")=="深度"]
    picks = viral_p[:2] + dry_p[:2] + deep_p[:1]
    if len(picks) < 5:
        rest = [t for t in pending if t not in picks]
        picks += rest[:5-len(picks)]
    medals = ["🥇","🥈","🥉","4️⃣","5️⃣"]
    today_cards = "".join(card_html(t, medals[i] if i<len(medals) else "") for i,t in enumerate(picks[:5]))

    # ── 选题库卡片 ──
    all_cards = "".join(card_html(t) for t in topics)

    # ── 日历行 ──
    cal_rows = "".join(cal_row_html(e) for e in cal)

    # ── 分类下拉 ──
    cats = sorted(set(t.get("category","") for t in topics))
    cat_opts = "".join(f'<option value="{c}">{c}</option>' for c in cats)

    # ── 统计 ──
    cat_counts = {}
    for t in topics:
        c = t.get("category","")
        cat_counts[c] = cat_counts.get(c,0)+1
    cat_bars = ""
    for c, n in sorted(cat_counts.items(), key=lambda x:-x[1]):
        pct = n/len(topics)*100
        cat_bars += f'<div class="bar"><div class="row"><span>{c}</span><span>{n}期 ({pct:.1f}%)</span></div><div class="track"><div class="fill" style="width:{pct}%"></div></div></div>'

    tc = {}
    for t in topics:
        ty = t.get("content_type","?")
        tc[ty] = tc.get(ty,0)+1
    ty_colors = {"爆款":"var(--red)","干货":"var(--accent)","深度":"var(--purple)"}
    type_bars = ""
    for ty, n in tc.items():
        pct = n/len(topics)*100
        c = ty_colors.get(ty,"var(--text2)")
        type_bars += f'<div class="bar"><div class="row"><span>{TYPE_EMOJI.get(ty,"")} {ty}</span><span>{n}期 ({pct:.1f}%)</span></div><div class="track"><div class="fill" style="width:{pct}%;background:{c}"></div></div></div>'

    # ═══════════════ 完整 HTML ═══════════════
    page = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>剪辑选题系统</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
/* ========== 全局配色变量 ========== */
:root {{
  --bg-main: #080c16;
  --bg-card: rgba(16, 22, 36, 0.65);
  --text-primary: #f0f4fc;
  --text-secondary: #8a94a6;
  --text-tertiary: #4a5268;
  --tech-color: #00d0ff;
  --tech-light: rgba(0, 208, 255, 0.18);
  --tech-glow: 0 0 18px rgba(0, 208, 255, 0.35);
  --red: #ff5e5e;
  --orange: #ffa94d;
  --green: #4ade80;
  --purple: #c084fc;
  --grid-opacity: 0.04;
  --radius: 12px;
  --radius-lg: 16px;
  --ease-smooth: cubic-bezier(0.22, 1, 0.36, 1);
  --anim-fast: 0.25s var(--ease-smooth);
  --anim-normal: 0.4s var(--ease-smooth);
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: 'Inter', system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
  background-color: var(--bg-main);
  color: var(--text-secondary);
  line-height: 1.6;
  overflow-x: hidden;
  background-image:
    linear-gradient(rgba(0, 208, 255, var(--grid-opacity)) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 208, 255, var(--grid-opacity)) 1px, transparent 1px);
  background-size: 40px 40px;
  min-height: 100vh;
}}

/* ========== Scroll progress ========== */
.scroll-progress {{
  position: fixed; top: 0; left: 0; height: 2px;
  background: var(--tech-color); box-shadow: 0 0 10px var(--tech-color);
  z-index: 200; width: 0%; transition: width 0.1s linear;
}}

/* ========== Particle canvas ========== */
#particle-canvas {{
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  z-index: -1; pointer-events: none; opacity: 0.25;
}}

/* ========== Cursor glow (desktop only) ========== */
.cursor-glow {{
  position: fixed; width: 400px; height: 400px; border-radius: 50%;
  background: radial-gradient(circle, rgba(0,208,255,0.10) 0%, transparent 70%);
  pointer-events: none; z-index: 0; transform: translate(-50%, -50%); opacity: 0.12;
}}
@media (max-width: 768px) {{ .cursor-glow {{ display: none; }} }}

/* ========== Nav ========== */
nav {{
  position: fixed; top: 0; left: 0; width: 100%; padding: 18px 64px;
  display: flex; justify-content: space-between; align-items: center;
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  background: rgba(8, 12, 22, 0.35); border-bottom: 1px solid var(--tech-light);
  z-index: 100; transition: background var(--anim-normal);
}}
nav .logo {{
  font-size: 20px; color: var(--text-primary); letter-spacing: 2px;
  font-weight: 700; display: flex; align-items: center; gap: 12px;
}}
nav .logo .dot {{
  width: 10px; height: 10px; border-radius: 50%;
  background: var(--tech-color); box-shadow: 0 0 14px var(--tech-color);
}}
nav .nav-links {{ display: flex; gap: 6px; background: rgba(255,255,255,0.03); border-radius: 10px; padding: 3px; }}
nav .nav-links button {{
  border: none; background: none; padding: 7px 20px; border-radius: 8px;
  font-size: 13px; font-weight: 500; color: var(--text-secondary);
  cursor: pointer; transition: all var(--anim-fast); font-family: inherit; letter-spacing: -0.1px;
}}
nav .nav-links button:hover {{ color: var(--text-primary); }}
nav .nav-links button.active {{ background: rgba(0, 208, 255, 0.1); color: var(--tech-color); }}
nav .time {{ font-size: 11px; color: var(--text-tertiary); letter-spacing: 0.5px; font-feature-settings: "tnum"; }}
@media (max-width: 768px) {{
  nav {{ padding: 14px 20px; }}
  nav .nav-links {{ gap: 2px; }}
  nav .nav-links button {{ padding: 6px 12px; font-size: 11px; }}
  nav .time {{ display: none; }}
}}

/* ========== Main ========== */
main {{
  position: relative; z-index: 1; max-width: 1280px; margin: 0 auto;
  padding: 100px 28px 60px;
}}
@media (max-width: 768px) {{ main {{ padding: 90px 16px 40px; }} }}
section {{ display: none; animation: fadeSlide 0.4s var(--ease-smooth); }}
section.active {{ display: block; }}
@keyframes fadeSlide {{
  from {{ opacity: 0; transform: translateY(16px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

/* ========== Stats ========== */
.stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 40px; }}
@media (max-width: 768px) {{ .stats {{ grid-template-columns: repeat(2, 1fr); }} }}
.stat {{
  position: relative; background: var(--bg-card); border-radius: var(--radius-lg);
  padding: 28px 30px; border: 1px solid var(--tech-light);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  transition: all var(--anim-normal); overflow: hidden;
}}
.stat::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,208,255,0.3), transparent);
  opacity: 0; transition: opacity var(--anim-normal);
}}
.stat:hover {{ transform: translateY(-4px); border-color: rgba(0,208,255,0.3); box-shadow: var(--tech-glow); }}
.stat:hover::before {{ opacity: 1; }}
.stat .val {{
  font-size: 48px; font-weight: 700; letter-spacing: -2px; line-height: 1;
  font-feature-settings: "tnum"; transition: color var(--anim-normal);
}}
.stat .lbl {{
  font-size: 11px; color: var(--text-tertiary); margin-top: 8px;
  font-weight: 500; text-transform: uppercase; letter-spacing: 1px;
}}

/* ========== Section headers ========== */
.sec-head {{ display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 22px; }}
.sec-head h2 {{ font-size: 22px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.4px; }}
.sec-head .sub {{ font-size: 13px; color: var(--text-tertiary); }}

/* ========== Glass cards ========== */
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 12px; }}
@media (max-width: 768px) {{ .grid {{ grid-template-columns: 1fr; }} }}
.card {{
  background: var(--bg-card); border-radius: var(--radius-lg);
  border: 1px solid var(--tech-light); backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px); cursor: pointer;
  transition: all var(--anim-normal); position: relative; overflow: hidden;
}}
.card:hover {{
  transform: translateY(-4px);
  border-color: rgba(0,208,255,0.35); box-shadow: var(--tech-glow);
}}
.card:active {{ transform: scale(0.985); }}
.card-body {{ padding: 22px 28px 20px; position: relative; z-index: 1; }}
.card .tags {{ display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px; }}
.tag {{
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 10px; border-radius: 6px; font-size: 10.5px;
  font-weight: 600; letter-spacing: 0.3px; font-feature-settings: "tnum";
}}
.tag-red {{ background: rgba(255, 94, 94, 0.12); color: var(--red); }}
.tag-blue {{ background: rgba(0, 208, 255, 0.12); color: var(--tech-color); }}
.tag-purple {{ background: rgba(192, 132, 252, 0.12); color: var(--purple); }}
.tag-green {{ background: rgba(74, 222, 128, 0.12); color: var(--green); }}
.tag-orange {{ background: rgba(255, 169, 77, 0.12); color: var(--orange); }}
.tag-gray {{ background: rgba(255, 255, 255, 0.04); color: var(--text-secondary); }}
.card h3 {{ font-size: 15.5px; font-weight: 600; line-height: 1.4; margin-bottom: 10px; color: var(--text-primary); letter-spacing: -0.3px; }}
.card .meta {{ font-size: 12px; color: var(--text-tertiary); display: flex; gap: 16px; align-items: center; }}
.card .chevron {{
  position: absolute; right: 20px; top: 50%; transform: translateY(-50%);
  width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.03);
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; color: var(--text-tertiary); transition: all var(--anim-fast);
}}
.card:hover .chevron {{ background: var(--tech-color); color: #080c16; box-shadow: 0 0 18px rgba(0,208,255,0.4); }}
.card.hidden {{ display: none; }}

/* Card entrance stagger */
@keyframes cardIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
.card {{ animation: cardIn 0.5s var(--ease-smooth) both; }}
.card:nth-child(1) {{ animation-delay: 0s; }}
.card:nth-child(2) {{ animation-delay: 0.06s; }}
.card:nth-child(3) {{ animation-delay: 0.12s; }}
.card:nth-child(4) {{ animation-delay: 0.18s; }}
.card:nth-child(5) {{ animation-delay: 0.24s; }}

/* ========== Modal overlay ========== */
.overlay {{
  position: fixed; inset: 0; z-index: 999;
  background: rgba(0,0,0,0.55); backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  display: flex; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
}}
.overlay.show {{ opacity: 1; pointer-events: auto; }}
.modal {{
  background: rgba(14, 20, 34, 0.88); border-radius: 24px;
  width: min(720px, 94vw); max-height: 86vh; overflow-y: auto;
  border: 1px solid rgba(0,208,255,0.2);
  box-shadow: 0 0 0 1px rgba(0,208,255,0.04), 0 32px 80px rgba(0,0,0,0.55);
  transform: translateY(24px) scale(0.96);
  transition: transform 0.35s var(--ease-smooth);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
}}
.overlay.show .modal {{ transform: translateY(0) scale(1); }}
.modal-header {{ padding: 30px 34px 0; display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; }}
.modal-header h2 {{ font-size: 21px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.4px; line-height: 1.3; }}
.modal-close {{
  width: 34px; height: 34px; border-radius: 50%; border: 1px solid rgba(255,255,255,0.08);
  background: rgba(255,255,255,0.03); font-size: 15px; cursor: pointer;
  color: var(--text-secondary); flex-shrink: 0; transition: all 0.2s;
  display: flex; align-items: center; justify-content: center;
}}
.modal-close:hover {{ background: rgba(255,255,255,0.08); color: var(--text-primary); border-color: var(--tech-color); }}
.modal-body {{ padding: 24px 34px 36px; }}
.modal-body .sec {{ margin-bottom: 26px; }}
.modal-body .sec h4 {{
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 1.5px; color: var(--text-tertiary); margin-bottom: 12px;
}}
.modal-body .steps {{
  background: rgba(255,255,255,0.02); border-radius: 12px;
  padding: 16px 20px; list-style: none; border: 1px solid rgba(255,255,255,0.04);
}}
.modal-body .steps li {{
  padding: 10px 0; font-size: 14px; line-height: 1.65;
  border-bottom: 1px solid rgba(255,255,255,0.04); display: flex; gap: 8px;
}}
.modal-body .steps li:last-child {{ border-bottom: none; }}
.ref-link {{
  display: flex; align-items: center; gap: 12px; padding: 12px 16px;
  border-radius: 10px; background: rgba(255,255,255,0.02);
  margin-bottom: 6px; text-decoration: none; color: var(--text-primary);
  transition: all 0.2s; font-size: 13px; border: 1px solid transparent;
}}
.ref-link:hover {{ background: rgba(0,208,255,0.06); color: var(--tech-color); border-color: rgba(0,208,255,0.15); }}
.ref-link .arrow {{ color: var(--text-tertiary); font-size: 13px; transition: all 0.2s; }}
.ref-link:hover .arrow {{ color: var(--tech-color); transform: translateX(3px); }}
.ref-note {{ font-size: 11px; color: var(--text-tertiary); margin-left: auto; }}
.mat-tag {{
  display: inline-block; padding: 6px 14px; border-radius: 8px;
  background: rgba(0,208,255,0.08); color: var(--tech-color);
  font-size: 12px; font-weight: 500; margin: 3px; letter-spacing: -0.1px;
}}
.bgm-tip {{
  margin-top: 12px; padding: 14px 18px; border-radius: 10px;
  background: rgba(255,169,77,0.06); color: var(--orange);
  font-size: 13px; display: flex; align-items: center; gap: 8px;
  border: 1px solid rgba(255,169,77,0.1);
}}
.empty-note {{ text-align: center; padding: 24px; color: var(--text-tertiary); font-size: 13px; }}

/* ========== Filters ========== */
.filters {{ display: flex; gap: 8px; margin-bottom: 18px; flex-wrap: wrap; align-items: center; }}
.filters select, .filters input {{
  padding: 9px 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);
  background: var(--bg-card); color: var(--text-primary); font-size: 13px;
  font-family: inherit; outline: none; transition: all 0.2s;
  backdrop-filter: blur(8px);
}}
.filters select:hover, .filters input:hover {{ border-color: rgba(0,208,255,0.2); }}
.filters select:focus, .filters input:focus {{ border-color: var(--tech-color); box-shadow: 0 0 0 3px rgba(0,208,255,0.1); }}
.filters input {{ min-width: 170px; }}
.filters .count {{ font-size: 11px; color: var(--text-tertiary); }}
.filters select option {{ background: #101622; color: var(--text-primary); }}

/* ========== Table ========== */
.tbl-wrap {{
  border-radius: var(--radius-lg); border: 1px solid rgba(255,255,255,0.06);
  overflow: hidden; background: var(--bg-card); max-height: 70vh; overflow-y: auto;
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
}}
.tbl-wrap table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
.tbl-wrap th {{
  text-align: left; padding: 13px 18px; font-size: 10px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1px; color: var(--text-tertiary);
  background: rgba(0,0,0,0.2); border-bottom: 1px solid rgba(0,208,255,0.1);
  position: sticky; top: 0; z-index: 5;
}}
.tbl-wrap td {{ padding: 13px 18px; border-bottom: 1px solid rgba(255,255,255,0.03); }}
.tbl-wrap tr:last-child td {{ border-bottom: none; }}
.tbl-wrap tr:hover td {{ background: rgba(0,208,255,0.03); }}
.tbl-wrap .ep {{ font-weight: 700; color: var(--tech-color); }}
.cal-row {{ cursor: pointer; }}
.cal-row.hidden {{ display: none; }}
.pill {{ display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 10.5px; font-weight: 600; letter-spacing: 0.3px; }}
.pill-green {{ background: rgba(74,222,128,0.1); color: var(--green); }}
.pill-blue {{ background: rgba(0,208,255,0.1); color: var(--tech-color); }}
.pill-purple {{ background: rgba(192,132,252,0.1); color: var(--purple); }}

/* ========== Stats page ========== */
.stats-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
@media (max-width: 768px) {{ .stats-grid {{ grid-template-columns: 1fr; }} }}
.stat-panel {{
  background: var(--bg-card); border-radius: var(--radius-lg);
  border: 1px solid var(--tech-light); padding: 28px 30px;
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
}}
.stat-panel h3 {{ font-size: 14px; font-weight: 600; color: var(--text-primary); margin-bottom: 20px; }}
.bar {{ margin-bottom: 10px; }}
.bar .row {{ display: flex; justify-content: space-between; font-size: 12px; color: var(--text-secondary); margin-bottom: 4px; }}
.bar .track {{ height: 5px; background: rgba(255,255,255,0.04); border-radius: 3px; overflow: hidden; }}
.bar .fill {{
  height: 100%; border-radius: 3px;
  transition: width 0.8s var(--ease-smooth);
  background: linear-gradient(90deg, var(--tech-color), var(--purple));
}}

/* ========== Scrollbar ========== */
.modal::-webkit-scrollbar, .tbl-wrap::-webkit-scrollbar {{ width: 5px; }}
.modal::-webkit-scrollbar-track, .tbl-wrap::-webkit-scrollbar-track {{ background: transparent; }}
.modal::-webkit-scrollbar-thumb, .tbl-wrap::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.06); border-radius: 3px; }}
.modal::-webkit-scrollbar-thumb:hover {{ background: rgba(255,255,255,0.12); }}

::selection {{ background: rgba(0,208,255,0.3); color: #fff; }}
</style>
</head>
<body>
<div class="scroll-progress"></div>
<canvas id="particle-canvas"></canvas>
<div class="cursor-glow"></div>

<nav>
    <div class="logo"><span class="dot"></span>剪辑选题系统</div>
    <div class="nav-links">
        <button class="active" data-panel="today">今日选题</button>
        <button data-panel="calendar">内容日历</button>
        <button data-panel="library">选题库</button>
        <button data-panel="stats">数据</button>
    </div>
    <div class="time">{now}</div>
</nav>

<main>

<!-- ═══ 今日选题 ═══ -->
<section class="active" id="sec-today">
    <div class="stats">
        <div class="stat"><div class="val" style="color:var(--tech-color)">{len(topics)}</div><div class="lbl">总选题</div></div>
        <div class="stat"><div class="val" style="color:var(--green)">{len(pending)}</div><div class="lbl">待发布</div></div>
        <div class="stat"><div class="val" style="color:var(--purple)">{len(published)}</div><div class="lbl">已发布</div></div>
        <div class="stat"><div class="val" style="color:var(--orange)">{len(cal)}</div><div class="lbl">日历规划</div></div>
    </div>
    <div class="sec-head"><h2>🔥 今日推荐</h2><span class="sub">{today}</span></div>
    <div class="grid" id="today-grid">
        {today_cards}
    </div>
</section>

<!-- ═══ 内容日历 ═══ -->
<section id="sec-calendar">
    <div class="sec-head"><h2>🗓️ 200期内容日历</h2></div>
    <div class="filters">
        <select id="f-stage" onchange="filterCal()">
            <option value="all">全部阶段</option>
            <option value="冷启动期">冷启动期 1-30</option>
            <option value="增长期">增长期 31-100</option>
            <option value="成熟期">成熟期 101-200</option>
        </select>
        <select id="f-cal-cat" onchange="filterCal()">
            <option value="all">全部分类</option>
            {cat_opts}
        </select>
        <input type="text" id="f-cal-search" placeholder="搜索标题…" oninput="filterCal()">
        <span class="count" id="cal-num">{len(cal)} 期</span>
    </div>
    <div class="tbl-wrap">
    <table><thead><tr><th>#</th><th>标题</th><th>分类</th><th>难度</th><th>类型</th><th>时长</th><th>阶段</th></tr></thead>
    <tbody id="cal-tbody">{cal_rows}</tbody></table>
    </div>
</section>

<!-- ═══ 选题库 ═══ -->
<section id="sec-library">
    <div class="sec-head"><h2>📚 全部选题</h2></div>
    <div class="filters">
        <select id="f-cat" onchange="filterLib()"><option value="all">全部分类</option>{cat_opts}</select>
        <select id="f-type" onchange="filterLib()">
            <option value="all">全部类型</option><option value="爆款">🔺 爆款</option><option value="干货">🔸 干货</option><option value="深度">🔹 深度</option>
        </select>
        <select id="f-diff" onchange="filterLib()">
            <option value="all">全部难度</option><option value="1">⭐ 入门</option><option value="2">⭐⭐ 基础</option><option value="3">⭐⭐⭐ 进阶</option><option value="4">⭐⭐⭐⭐ 高级</option><option value="5">⭐⭐⭐⭐⭐ 专家</option>
        </select>
        <input type="text" id="f-search" placeholder="搜索选题…" oninput="filterLib()">
        <span class="count" id="lib-num">{len(topics)} 条</span>
    </div>
    <div class="grid" id="lib-grid">
        {all_cards}
    </div>
</section>

<!-- ═══ 数据统计 ═══ -->
<section id="sec-stats">
    <div class="sec-head"><h2>📊 数据概览</h2></div>
    <div class="stats">
        <div class="stat"><div class="val" style="color:var(--tech-color)">{len(topics)}</div><div class="lbl">总选题</div></div>
        <div class="stat"><div class="val" style="color:var(--green)">{len(pending)}</div><div class="lbl">待发布</div></div>
        <div class="stat"><div class="val" style="color:var(--purple)">{len(published)}</div><div class="lbl">已发布</div></div>
        <div class="stat"><div class="val" style="color:var(--red)">{len(skipped)}</div><div class="lbl">已跳过</div></div>
    </div>
    <div class="stats-grid">
        <div class="stat-panel"><h3>📂 分类覆盖</h3>{cat_bars}</div>
        <div class="stat-panel"><h3>📈 内容类型</h3>{type_bars}</div>
    </div>
</section>

</main>

<!-- ═══ Modal ═══ -->
<div class="overlay" id="overlay" onclick="if(event.target===this)closeDetail()">
    <div class="modal" id="modal"></div>
</div>

<script>
// ═══ Scroll progress ═══
window.addEventListener('scroll', function(){{
    var p = (document.documentElement.scrollTop / (document.documentElement.scrollHeight - document.documentElement.clientHeight)) * 100;
    document.querySelector('.scroll-progress').style.width = p + '%';
}});

// ═══ Cursor glow ═══
if(window.innerWidth > 768) {{
    document.addEventListener('mousemove', function(e){{
        var g = document.querySelector('.cursor-glow');
        g.style.left = e.clientX + 'px';
        g.style.top = e.clientY + 'px';
    }});
}}

// ═══ Particle background ═══
(function(){{
    var c = document.getElementById('particle-canvas');
    var ctx = c.getContext('2d');
    var w, h, particles = [];
    function resize() {{ w = c.width = window.innerWidth; h = c.height = window.innerHeight; }}
    window.addEventListener('resize', resize); resize();
    var N = window.innerWidth < 768 ? 25 : 55;
    for(var i=0; i<N; i++) {{
        particles.push({{
            x: Math.random()*w, y: Math.random()*h,
            r: Math.random()*1.2+0.3,
            sx: (Math.random()-0.5)*0.35,
            sy: (Math.random()-0.5)*0.35,
            o: Math.random()*0.35+0.08
        }});
    }}
    function anim() {{
        ctx.clearRect(0,0,w,h);
        for(var i=0; i<particles.length; i++) {{
            var p = particles[i];
            p.x += p.sx; p.y += p.sy;
            if(p.x<0||p.x>w) p.sx *= -1;
            if(p.y<0||p.y>h) p.sy *= -1;
            ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
            ctx.fillStyle = 'rgba(0,208,255,'+p.o+')'; ctx.fill();
        }}
        requestAnimationFrame(anim);
    }}
    anim();
}})();

// ═══ Navigation ═══
document.querySelectorAll(".nav-links button").forEach(function(b){{
    b.onclick=function(){{
        document.querySelectorAll(".nav-links button").forEach(function(x){{x.classList.remove("active")}});
        document.querySelectorAll("section").forEach(function(s){{s.classList.remove("active")}});
        b.classList.add("active");
        document.getElementById("sec-"+b.dataset.panel).classList.add("active");
    }};
}});

// ═══ Calendar Filter ═══
function filterCal(){{
    var stage=document.getElementById("f-stage").value;
    var cat=document.getElementById("f-cal-cat").value;
    var q=(document.getElementById("f-cal-search").value||"").toLowerCase();
    var rows=document.querySelectorAll("#cal-tbody .cal-row");
    var count=0;
    rows.forEach(function(r){{
        var show=true;
        if(stage!=="all" && r.dataset.stage!==stage) show=false;
        if(cat!=="all" && r.dataset.cat!==cat) show=false;
        if(q && r.dataset.title.toLowerCase().indexOf(q)===-1) show=false;
        r.classList.toggle("hidden",!show);
        if(show) count++;
    }});
    document.getElementById("cal-num").textContent=count+" 期";
}}

// ═══ Library Filter ═══
function filterLib(){{
    var cat=document.getElementById("f-cat").value;
    var type=document.getElementById("f-type").value;
    var diff=document.getElementById("f-diff").value;
    var q=(document.getElementById("f-search").value||"").toLowerCase();
    var cards=document.querySelectorAll("#lib-grid .card");
    var count=0;
    cards.forEach(function(c){{
        var show=true;
        if(cat!=="all" && c.dataset.cat!==cat) show=false;
        if(type!=="all" && c.dataset.type!==type) show=false;
        if(diff!=="all" && c.dataset.diff!==diff) show=false;
        if(q && c.dataset.title.toLowerCase().indexOf(q)===-1) show=false;
        c.classList.toggle("hidden",!show);
        if(show) count++;
    }});
    document.getElementById("lib-num").textContent=count+" 条";
}}

// ═══ Detail Modal ═══
function openDetail(card){{
    var t=card.querySelector(".detail-data");
    if(!t) return;
    var title=t.querySelector(".detail-title").textContent;
    var cat=t.querySelector(".detail-cat").textContent;
    var ctype=t.querySelector(".detail-type").textContent;
    var diff=parseInt(t.querySelector(".detail-diff").textContent);
    var dur=t.querySelector(".detail-dur").textContent;
    var viral=t.querySelector(".detail-viral").textContent;
    var prod=t.querySelector(".detail-prod").textContent;
    var desc=t.querySelector(".detail-desc").textContent;
    var hook=t.querySelector(".detail-hook").textContent;
    var steps=t.querySelector(".detail-steps").innerHTML;
    var ending=t.querySelector(".detail-ending").textContent;
    var bgm=t.querySelector(".detail-bgm").textContent;
    var refs=t.querySelector(".detail-refs").innerHTML;
    var mats=t.querySelector(".detail-mats").innerHTML;

    var DM={{1:"⭐",2:"⭐⭐",3:"⭐⭐⭐",4:"⭐⭐⭐⭐",5:"⭐⭐⭐⭐⭐"}};
    var TE={{"爆款":"🔺","干货":"🔸","深度":"🔹"}};
    var tcl=ctype==="爆款"?"tag-red":(ctype==="干货"?"tag-blue":"tag-purple");
    var dcl=diff<=2?"tag-green":(diff<=3?"tag-orange":"tag-red");
    var descBlock=desc?'<div class="sec"><h4>💡 内容说明</h4><p style="font-size:14px;color:var(--text-secondary)">'+desc+'</p></div>':'';

    document.getElementById("modal").innerHTML=
        '<div class="modal-header"><div><div class="tags" style="margin-bottom:8px">'+
        '<span class="tag '+tcl+'">'+(TE[ctype]||"")+" "+ctype+'</span>'+
        '<span class="tag '+dcl+'">'+(DM[diff]||"⭐⭐")+'</span>'+
        '<span class="tag tag-gray">'+cat+'</span></div>'+
        '<h2>'+title+'</h2></div>'+
        '<button class="modal-close" onclick="closeDetail()">✕</button></div>'+
        '<div class="modal-body">'+descBlock+
        '<div class="sec"><h4>✍️ 脚本文案</h4>'+
        '<div style="font-size:15px;font-weight:500;margin-bottom:12px;line-height:1.5;color:var(--text-primary)">💬 '+hook+'</div>'+
        '<ol class="steps">'+steps+'</ol>'+
        '<div style="font-size:14px;color:var(--text-secondary);margin-top:8px">'+ending+'</div>'+
        '<div class="bgm-tip">🎵 推荐BGM：'+bgm+'</div></div>'+
        '<div class="sec"><h4>📦 所需素材</h4>'+(mats||'<span style="color:var(--text-tertiary);font-size:13px">无特殊要求</span>')+'</div>'+
        '<div class="sec"><h4>🔗 对标参考</h4><p style="font-size:12px;color:var(--text-tertiary);margin-bottom:8px">以下链接来自真实热门教程，点击可跳转参考</p>'+(refs||'<div class="empty-note">🔍 建议在抖音搜索「'+title+'」找参考</div>')+'</div>'+
        '<div class="sec"><h4>📋 基本信息</h4>'+
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:13px">'+
        '<div>⏱ 时长：'+dur+'</div><div>🔥 涨粉潜力：'+viral+'</div>'+
        '<div>⏳ 制作耗时：'+prod+'</div></div></div></div>';

    document.getElementById("overlay").classList.add("show");
    document.body.style.overflow="hidden";
}}

function openDetailByTitle(title){{
    var cards=document.querySelectorAll(".card");
    for(var i=0;i<cards.length;i++){{
        if(cards[i].dataset.title===title){{openDetail(cards[i]);return;}}
    }}
}}

function closeDetail(){{
    document.getElementById("overlay").classList.remove("show");
    document.body.style.overflow="";
}}
document.addEventListener("keydown",function(e){{if(e.key==="Escape")closeDetail()}});
</script>
</body>
</html>'''



    with open(HTML,"w",encoding="utf-8") as f:
        f.write(page)

    print(f"✅ 仪表盘已生成：{HTML}")
    print(f"   大小：{len(page.encode('utf-8'))/1024:.1f} KB")
    print(f"   今日推荐 {len(picks)} 条 | 题库 {len(topics)} 条 | 日历 {len(cal)} 期")


if __name__ == "__main__":
    build()
