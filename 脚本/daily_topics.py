"""
每日热点选题采集器
- 通过搜索 API 抓取当前热门的剪辑相关话题
- 结合剪映新功能、热门 BGM、热门特效等时效性内容
- 对比已发布记录去重
- 输出今日推荐选题卡（Markdown 格式）
"""

import os
import sys
from datetime import datetime

# 添加脚本目录到 path，以便导入 topic_manager
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "脚本"))

from topic_manager import (
    load_topics_db,
    load_published,
    get_published_titles,
    get_pending_topics,
    topics_to_markdown,
)

OUTPUT_DIR = os.path.join(BASE_DIR, "输出")

# ============================================================
# 搜索关键词池（用于每日热点采集）
# ============================================================

SEARCH_KEYWORDS = [
    # 剪映相关
    "剪映最新功能 2026",
    "剪映更新 新功能",
    "剪映热门教程",
    # 抖音热点
    "抖音热门剪辑教程",
    "抖音热门转场 2026",
    "抖音卡点教程",
    "抖音最新特效 怎么用",
    # 拍摄剪辑结合
    "拍摄剪辑技巧 教程",
    "手机拍视频 技巧",
    "视频剪辑 新手教程",
    # 趋势
    "CapCut trending effect",
    "视频剪辑 调色教程",
    "Vlog 剪辑 教程",
]

# 热点话题手动维护（定期更新）
TRENDING_TOPICS_MANUAL = [
    {
        "title": "抖音最新热歌BGM + 对应的卡点剪辑节奏",
        "category": "热门跟拍",
        "difficulty": 1,
        "content_type": "爆款",
        "description": "采集本周抖音热搜榜前10的BGM，匹配对应的剪辑节奏",
        "estimated_duration": "30s",
        "viral_potential": "高",
        "production_time": "1.5h",
        "materials_needed": "本周热门BGM列表+对应素材",
    },
    {
        "title": "剪映最新版本的隐藏新功能",
        "category": "热门跟拍",
        "difficulty": 2,
        "content_type": "爆款",
        "description": "升级到最新版剪映，挖掘新功能并做教程",
        "estimated_duration": "25s",
        "viral_potential": "高",
        "production_time": "1h",
        "materials_needed": "最新版剪映APP",
    },
    {
        "title": "本月抖音最火的3种剪辑风格拆解",
        "category": "热门跟拍",
        "difficulty": 2,
        "content_type": "干货",
        "description": "搜集本月抖音最火的视频风格，拆解其剪辑手法",
        "estimated_duration": "3min",
        "viral_potential": "高",
        "production_time": "2h",
        "materials_needed": "本月热门视频案例",
    },
]


# ============================================================
# 每日选题采集器核心逻辑
# ============================================================

def collect_daily_topics(count: int = 5) -> list:
    """
    采集今日推荐选题
    策略：
    1. 优先从待发布选题库中按策略选取
    2. 检查是否有手动维护的热点话题
    3. 避免与已发布内容重复
    """
    published_titles = get_published_titles()
    pending = get_pending_topics()

    candidates = []

    # 1. 从待发布库中按策略选：优先选「爆款」型和「热门跟拍」类
    viral_pending = [t for t in pending if t.get("viral_potential") == "高" and t.get("content_type") == "爆款"]
    trending_pending = [t for t in pending if t.get("category") == "热门跟拍"]
    dry_pending = [t for t in pending if t.get("content_type") == "干货"]
    deep_pending = [t for t in pending if t.get("content_type") == "深度"]

    # 按比例组合：2爆款 + 2干货 + 1深度
    for t in viral_pending[:2]:
        if t["title"] not in published_titles:
            candidates.append(t)

    for t in dry_pending[:2]:
        if t["title"] not in published_titles:
            candidates.append(t)

    for t in deep_pending[:1]:
        if t["title"] not in published_titles:
            candidates.append(t)

    # 2. 补充手动维护的热点话题
    if len(candidates) < count:
        for mt in TRENDING_TOPICS_MANUAL:
            if mt["title"] not in published_titles and mt not in candidates:
                candidates.append(mt)
            if len(candidates) >= count:
                break

    # 3. 如果还不够，从剩余待发布中补
    if len(candidates) < count:
        other_pending = [t for t in pending if t not in candidates and t["title"] not in published_titles]
        candidates.extend(other_pending[:count - len(candidates)])

    return candidates[:count]


def score_topic(topic: dict) -> int:
    """给选题打分（越高越推荐今天做）"""
    score = 0

    # 类型分
    type_scores = {"爆款": 3, "干货": 2, "深度": 1}
    score += type_scores.get(topic.get("content_type", ""), 0)

    # 涨粉潜力分
    viral_scores = {"高": 3, "中": 2, "低": 1}
    score += viral_scores.get(topic.get("viral_potential", ""), 0)

    # 难度惩罚（太难的不急）
    difficulty = topic.get("difficulty", 2)
    score -= max(0, difficulty - 3)  # 4-5星难度扣分

    # 热门跟拍加分（时效性）
    if topic.get("category") == "热门跟拍":
        score += 2

    return score


def generate_daily_pick(candidates: list, date_str: str = None) -> str:
    """生成每日选题卡（Markdown）"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    difficulty_map = {1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐", 4: "⭐⭐⭐⭐", 5: "⭐⭐⭐⭐⭐"}
    type_emoji = {"爆款": "🔺", "干货": "🔸", "深度": "🔹"}
    medal_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    lines = [
        f"# 🎬 今日选题推荐 — {date_str}",
        "",
        f"> 共 {len(candidates)} 个推荐选题，按推荐优先级排列",
        "> 建议今天制作第1-2条，其余备选",
        "",
        "---",
        "",
    ]

    # 按分数排序
    scored = [(score_topic(t), t) for t in candidates]
    scored.sort(key=lambda x: -x[0])

    for rank, (score, topic) in enumerate(scored):
        diff = difficulty_map.get(topic.get("difficulty", 2), "⭐⭐")
        emoji = type_emoji.get(topic.get("content_type", ""), "")
        medal = medal_emoji[rank] if rank < len(medal_emoji) else "▶️"

        lines.append(f"## {medal} {emoji} {topic['title']}")
        lines.append("")
        lines.append(f"| 维度 | 详情 |")
        lines.append(f"|------|------|")
        lines.append(f"| **分类** | {topic.get('category', '')} |")
        lines.append(f"| **难度** | {diff} |")
        lines.append(f"| **类型** | {topic.get('content_type', '')} |")
        lines.append(f"| **预计时长** | {topic.get('estimated_duration', '')} |")
        lines.append(f"| **涨粉潜力** | {topic.get('viral_potential', '')} |")
        lines.append(f"| **制作耗时** | {topic.get('production_time', '')} |")
        lines.append(f"| **推荐指数** | {'🔥' * min(5, max(1, score))} ({score}分) |")
        lines.append("")

        if topic.get("description"):
            lines.append(f"### 📝 内容说明")
            lines.append(f"{topic['description']}")
            lines.append("")

        if topic.get("materials_needed"):
            lines.append(f"### 📦 所需素材")
            lines.append(f"{topic['materials_needed']}")
            lines.append("")

        # 脚本大纲建议
        lines.append(f"### ✍️ 脚本大纲建议")
        lines.append(f"1. **开场（3-5秒）**：抛出问题或展示效果 → 钩住观众")
        lines.append(f"2. **教学/展示（主体）**：分步骤演示，每步配文字说明")
        lines.append(f"3. **效果对比**：Before/After 对比，强化价值感")
        lines.append(f"4. **结尾引导**：引导点赞/收藏/关注 + 下期预告")
        lines.append("")

        lines.append("---")
        lines.append("")

    # 今日拍摄清单
    lines.append("## 📋 今日拍摄清单")
    lines.append("")
    lines.append("| 序号 | 选题 | 类型 | 预计耗时 | 所需素材 |")
    lines.append("|------|------|------|---------|---------|")
    for rank, (score, topic) in enumerate(scored):
        lines.append(
            f"| {rank+1} | {topic['title']} | "
            f"{topic.get('content_type', '')} | "
            f"{topic.get('production_time', '')} | "
            f"{topic.get('materials_needed', '')[:30]}... |"
        )
    lines.append("")

    # 今日剪辑清单
    lines.append("## 🎥 今日剪辑清单")
    lines.append("")
    lines.append("- [ ] 录制剪映操作过程（屏幕录制）")
    lines.append("- [ ] 拍摄实拍演示素材（如需）")
    lines.append("- [ ] 剪辑成片（目标时长：见上表）")
    lines.append("- [ ] 制作封面图")
    lines.append("- [ ] 写标题文案（含关键词：剪映/剪辑教程/拍摄技巧）")
    lines.append("- [ ] 发布到抖音")
    lines.append("")

    # 发布后数据追踪建议
    lines.append("## 📊 发布后追踪（24小时后回看）")
    lines.append("")
    lines.append("| 指标 | 目标 | 实际 |")
    lines.append("|------|------|------|")
    lines.append("| 播放量 | 5000+ | _ |")
    lines.append("| 完播率 | 30%+ | _ |")
    lines.append("| 点赞数 | 100+ | _ |")
    lines.append("| 收藏数 | 50+ | _ |")
    lines.append("| 评论数 | 20+ | _ |")
    lines.append("| 涨粉数 | 20+ | _ |")
    lines.append("")
    lines.append(f"---")
    lines.append(f"*选题卡生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    lines.append(f"*数据来源：选题数据库 + 热点关键词匹配*")

    return "\n".join(lines)


def save_daily_pick(md_content: str, date_str: str = None):
    """保存每日选题卡到文件"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"每日选题_{date_str}.md")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"✅ 今日选题卡已保存：{filepath}")
    return filepath


def get_search_suggestions() -> list:
    """
    返回一组搜索建议 —— 这些是「建议你去抖音/搜索引擎搜一下看看
    现在最火的是什么」的关键词组合。用于人工辅助验证。
    """
    today = datetime.now()
    suggestions = [
        f"剪映 {'新功能' if today.day % 3 == 0 else '教程'} {today.year}",
        f"抖音热门{'转场' if today.day % 2 == 0 else '卡点'}",
        f"视频剪辑 {'新手' if today.weekday() < 3 else '进阶'} 技巧",
    ]

    # 周末推荐轻松内容
    if today.weekday() >= 5:
        suggestions.append("Vlog 剪辑 日常 拍摄技巧")

    # 月初推荐热点追踪
    if today.day <= 5:
        suggestions.append(f"{today.month}月 抖音热门 BGM 卡点")

    return suggestions


# ============================================================
# 主入口
# ============================================================

def run_daily():
    """每日运行入口"""
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"🎬 每日选题采集器启动 — {today}")
    print()

    # 统计当前状态
    published = load_published()
    pending = get_pending_topics()
    print(f"📊 当前状态：已发布 {len(published)} 条 | 待发布 {len(pending)} 条")
    print()

    # 采集今日选题
    candidates = collect_daily_topics(count=5)
    print(f"🔍 已筛选 {len(candidates)} 个今日推荐选题：")
    print()

    for i, t in enumerate(candidates, 1):
        print(f"   {i}. [{t.get('content_type', '')}] {t['title']}")
        print(f"      分类：{t.get('category', '')} | 难度：{'⭐'*t.get('difficulty', 2)} | 涨粉：{t.get('viral_potential', '')}")
    print()

    # 生成选题卡
    md_content = generate_daily_pick(candidates, today)
    filepath = save_daily_pick(md_content, today)

    # 输出搜索建议
    print()
    print("🔍 建议同步搜索以下关键词验证热点：")
    for s in get_search_suggestions():
        print(f"   → {s}")

    print()

    # 自动刷新仪表盘 HTML
    print("🎨 正在刷新可视化仪表盘...")
    try:
        import generate_dashboard
        generate_dashboard.build()
        dashboard_path = os.path.join(BASE_DIR, "仪表盘.html")
        print(f"   📊 仪表盘：{dashboard_path}")
    except Exception as e:
        print(f"   ⚠️ 仪表盘刷新失败: {e}")

    print()
    print("✅ 每日选题采集完成！")
    print(f"   📄 选题卡：{filepath}")

    return filepath


if __name__ == "__main__":
    run_daily()
