"""
选题数据库管理工具
- 管理 topics_db.json（候选选题库）
- 管理 published.json（已发布追踪）
- 支持增删改查、避免重复选题
"""

import json
import os
from datetime import datetime
from typing import Optional

# 数据文件路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "数据")
TOPICS_DB_PATH = os.path.join(DATA_DIR, "选题库.json")
PUBLISHED_PATH = os.path.join(DATA_DIR, "已发布.json")

# ============================================================
# 数据加载/保存
# ============================================================

def load_json(path: str) -> dict | list:
    """加载 JSON 文件，不存在则返回空结构"""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return [] if "published" in path else {"topics": [], "categories": []}


def save_json(path: str, data):
    """保存 JSON 文件"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============================================================
# 选题数据库操作
# ============================================================

def load_topics_db() -> dict:
    """加载选题数据库"""
    data = load_json(TOPICS_DB_PATH)
    if isinstance(data, list):
        # 兼容旧格式
        data = {"topics": data, "categories": []}
    return data


def save_topics_db(db: dict):
    """保存选题数据库"""
    save_json(TOPICS_DB_PATH, db)


def add_topic(
    title: str,
    category: str,
    difficulty: int,
    content_type: str,
    description: str = "",
    estimated_duration: str = "",
    materials_needed: str = "",
    viral_potential: str = "中",
    production_time: str = "",
) -> dict:
    """添加一个新选题"""
    db = load_topics_db()

    # 检查重复
    for t in db["topics"]:
        if t["title"] == title:
            print(f"⚠️ 选题已存在: {title}")
            return t

    topic = {
        "id": f"topic_{len(db['topics']) + 1:04d}",
        "title": title,
        "category": category,
        "difficulty": difficulty,  # 1-5 星
        "content_type": content_type,  # 爆款/干货/深度
        "description": description,
        "estimated_duration": estimated_duration,
        "materials_needed": materials_needed,
        "viral_potential": viral_potential,  # 高/中/低
        "production_time": production_time,
        "status": "待发布",  # 待发布 / 已发布 / 已跳过
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "published_at": None,
        "douyin_url": None,
        "performance": None,  # {plays, likes, comments, shares, saves}
    }
    db["topics"].append(topic)
    save_topics_db(db)
    print(f"✅ 选题已添加: {title}")
    return topic


def get_topics_by_category(category: str, status: str = None) -> list:
    """按分类筛选选题"""
    db = load_topics_db()
    result = [t for t in db["topics"] if t["category"] == category]
    if status:
        result = [t for t in result if t["status"] == status]
    return result


def get_topics_by_difficulty(difficulty: int, status: str = None) -> list:
    """按难度筛选选题"""
    db = load_topics_db()
    result = [t for t in db["topics"] if t["difficulty"] == difficulty]
    if status:
        result = [t for t in result if t["status"] == status]
    return result


def get_pending_topics() -> list:
    """获取所有待发布选题"""
    db = load_topics_db()
    return [t for t in db["topics"] if t["status"] == "待发布"]


def get_next_topics(n: int = 5) -> list:
    """获取接下来建议发布的 N 个选题（按创建顺序）"""
    pending = get_pending_topics()
    return pending[:n]


def mark_as_published(
    topic_id: str,
    douyin_url: str = "",
    performance: dict = None,
):
    """标记选题为已发布"""
    db = load_topics_db()
    for t in db["topics"]:
        if t["id"] == topic_id:
            t["status"] = "已发布"
            t["published_at"] = datetime.now().strftime("%Y-%m-%d")
            t["douyin_url"] = douyin_url
            if performance:
                t["performance"] = performance
            save_topics_db(db)

            # 同步记录到 published.json
            record_published(t, douyin_url, performance)
            print(f"✅ 已标记发布: {t['title']}")
            return
    print(f"⚠️ 未找到选题: {topic_id}")


def mark_as_skipped(topic_id: str, reason: str = ""):
    """标记选题为跳过"""
    db = load_topics_db()
    for t in db["topics"]:
        if t["id"] == topic_id:
            t["status"] = "已跳过"
            t["skip_reason"] = reason
            save_topics_db(db)
            print(f"⏭️ 已跳过: {t['title']}（原因: {reason}）")
            return
    print(f"⚠️ 未找到选题: {topic_id}")


def get_stats() -> dict:
    """获取选题库统计信息"""
    db = load_topics_db()
    topics = db["topics"]
    total = len(topics)
    published = sum(1 for t in topics if t["status"] == "已发布")
    pending = sum(1 for t in topics if t["status"] == "待发布")
    skipped = sum(1 for t in topics if t["status"] == "已跳过")

    categories = {}
    for t in topics:
        cat = t["category"]
        categories[cat] = categories.get(cat, 0) + 1

    return {
        "总数": total,
        "已发布": published,
        "待发布": pending,
        "已跳过": skipped,
        "分类统计": categories,
    }


def topics_to_markdown(topics: list, title: str = "选题列表") -> str:
    """将选题列表转为 Markdown 格式"""
    lines = [f"# {title}", f"共 {len(topics)} 个选题", ""]

    difficulty_map = {1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐", 4: "⭐⭐⭐⭐", 5: "⭐⭐⭐⭐⭐"}

    for i, t in enumerate(topics, 1):
        diff = difficulty_map.get(t.get("difficulty", 1), "⭐")
        lines.append(f"## {i}. {t['title']}")
        lines.append(f"- **分类**：{t.get('category', '')} | **难度**：{diff} | **类型**：{t.get('content_type', '')}")
        lines.append(f"- **时长**：{t.get('estimated_duration', '')} | **涨粉潜力**：{t.get('viral_potential', '')} | **制作耗时**：{t.get('production_time', '')}")
        if t.get("description"):
            lines.append(f"- **说明**：{t['description']}")
        if t.get("materials_needed"):
            lines.append(f"- **所需素材**：{t['materials_needed']}")
        lines.append("")

    return "\n".join(lines)


# ============================================================
# 已发布追踪
# ============================================================

def load_published() -> list:
    """加载已发布记录"""
    return load_json(PUBLISHED_PATH)


def record_published(topic: dict, douyin_url: str = "", performance: dict = None):
    """记录一条已发布"""
    published = load_published()
    record = {
        "id": topic["id"],
        "title": topic["title"],
        "category": topic.get("category", ""),
        "published_at": datetime.now().strftime("%Y-%m-%d"),
        "douyin_url": douyin_url,
        "performance": performance or {},
    }
    published.append(record)
    save_json(PUBLISHED_PATH, record)


def get_published_titles() -> set:
    """获取所有已发布选题标题（用于去重）"""
    published = load_published()
    return {r["title"] for r in published}


def get_recent_published(n: int = 10) -> list:
    """获取最近发布的 N 条"""
    published = load_published()
    return published[-n:][::-1]  # 最新的在前


# ============================================================
# 初始化
# ============================================================

def init_database():
    """初始化数据库（如果不存在则创建）"""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(TOPICS_DB_PATH):
        save_topics_db({"topics": [], "categories": [
            "剪映基础操作", "转场特效", "卡点节奏", "调色教程",
            "文字动画", "蒙版&关键帧", "抠像&合成", "音频处理",
            "拍摄技巧", "热门跟拍", "案例实战",
            "AE动效制作", "视听语言&蒙太奇", "Vlog实战"
        ]})
        print("✅ 选题数据库已初始化")
    else:
        print("📂 选题数据库已存在")

    if not os.path.exists(PUBLISHED_PATH):
        save_json(PUBLISHED_PATH, [])
        print("✅ 已发布追踪已初始化")
    else:
        print("📂 已发布追踪已存在")


if __name__ == "__main__":
    init_database()
    stats = get_stats()
    print("\n📊 选题库统计：")
    for k, v in stats.items():
        if k != "分类统计":
            print(f"  {k}: {v}")
    print("  分类统计:")
    for cat, count in stats.get("分类统计", {}).items():
        print(f"    {cat}: {count}")
