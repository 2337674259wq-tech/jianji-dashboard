"""
长期内容日历生成器
基于 11 大内容分类体系，自动生成 200+ 期选题日历
输出 JSON（供程序读取）和 Markdown（供人工阅读）
"""

import json
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "数据")
OUTPUT_DIR = os.path.join(BASE_DIR, "输出")

# ============================================================
# 内容种子库 — 11 大分类 × N 个具体选题
# ============================================================

TOPIC_SEEDS = {
    "剪映基础操作": [
        {"title": "剪映界面速览：5分钟认识所有功能区", "diff": 1, "type": "干货", "duration": "3min", "viral": "中", "time": "1h", "desc": "给纯新手的第一条视频，降低门槛", "materials": "剪映APP截图"},
        {"title": "导入素材的3种方式，第3种最方便", "diff": 1, "type": "干货", "duration": "2min", "viral": "中", "time": "40min", "desc": "解决新手最常问的问题", "materials": "手机相册素材"},
        {"title": "剪辑轨道怎么用？一节课搞懂", "diff": 1, "type": "干货", "duration": "3min", "viral": "中", "time": "1h", "desc": "剪辑的基础概念，必须讲透", "materials": "剪映截图+演示视频"},
        {"title": "分割、删除、复制：3个最常用的操作", "diff": 1, "type": "干货", "duration": "2min", "viral": "低", "time": "30min", "desc": "最基础但最重要", "materials": "示例视频片段"},
        {"title": "视频速度调整：慢动作和快进的正确用法", "diff": 1, "type": "干货", "duration": "2min", "viral": "中", "time": "40min", "desc": "变速是最容易出效果的功能", "materials": "运动镜头素材"},
        {"title": "倒放效果：让视频变魔术的秘密", "diff": 1, "type": "爆款", "duration": "20s", "viral": "高", "time": "30min", "desc": "视觉效果强，容易传播", "materials": "适合倒放的素材（倒水、跳跃等）"},
        {"title": "画面比例怎么选？9:16还是16:9？", "diff": 1, "type": "干货", "duration": "2min", "viral": "中", "time": "30min", "desc": "横竖屏选择的底层逻辑", "materials": "同内容横竖版对比"},
        {"title": "背景设置的4种方式：模糊/颜色/自定义/透明", "diff": 1, "type": "干货", "duration": "2min", "viral": "中", "time": "40min", "desc": "竖屏发横屏素材的必备技能", "materials": "横屏素材+竖屏项目"},
        {"title": "添加文字的完全指南：字体/颜色/样式/动画", "diff": 1, "type": "干货", "duration": "3min", "viral": "中", "time": "1h", "desc": "文字是视频的核心元素", "materials": "剪映文字功能截图"},
        {"title": "文字动画入门：让标题动起来", "diff": 1, "type": "干货", "duration": "2min", "viral": "中", "time": "40min", "desc": "文字动画的入门课", "materials": "标题文字示例"},
        {"title": "添加音乐全攻略：曲库+本地导入+抖音收藏", "diff": 1, "type": "干货", "duration": "3min", "viral": "中", "time": "1h", "desc": "BGM是视频的灵魂", "materials": "剪映曲库截图"},
        {"title": "音量调节与淡入淡出：让声音更自然", "diff": 1, "type": "干货", "duration": "2min", "viral": "低", "time": "30min", "desc": "音频处理的第一个技能", "materials": "含BGM的示例视频"},
        {"title": "添加音效的时机：3个音效让视频质感翻倍", "diff": 1, "type": "爆款", "duration": "25s", "viral": "高", "time": "40min", "desc": "音效用好了效果立竿见影", "materials": "转场+动作场景素材"},
        {"title": "用剪映录音给视频配音", "diff": 1, "type": "干货", "duration": "2min", "viral": "中", "time": "30min", "desc": "配音是口播类账号的必备技能", "materials": "一段需要配音的视频"},
        {"title": "画中画基础：叠加两个画面的3种玩法", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "1h", "desc": "画中画是进阶的入口", "materials": "两个相关视频片段"},
        {"title": "视频裁剪与画面调整：二次构图的技巧", "diff": 1, "type": "干货", "duration": "2min", "viral": "中", "time": "40min", "desc": "补救拍摄失误的好方法", "materials": "构图有问题的素材"},
        {"title": "滤镜的正确打开方式：别一键套用", "diff": 1, "type": "干货", "duration": "2min", "viral": "中", "time": "40min", "desc": "滤镜用不好反而减分", "materials": "同片段不同滤镜对比"},
        {"title": "导出设置怎么选？分辨率和帧率说清楚", "diff": 1, "type": "干货", "duration": "2min", "viral": "中", "time": "30min", "desc": "导出设置影响画质", "materials": "导出设置截图"},
        {"title": "草稿管理技巧：别再丢工程了", "diff": 1, "type": "干货", "duration": "1min", "viral": "低", "time": "20min", "desc": "实用小技巧", "materials": "草稿列表截图"},
        {"title": "字幕自动识别：一键加字幕的正确姿势", "diff": 1, "type": "爆款", "duration": "20s", "viral": "高", "time": "30min", "desc": "新手最需要的功能", "materials": "有人声的视频片段"},
        {"title": "贴纸和花字怎么加？让你的视频更有趣", "diff": 1, "type": "干货", "duration": "2min", "viral": "中", "time": "30min", "desc": "增加视频趣味性的基础操作", "materials": "剪映贴纸/花字素材"},
        {"title": "特效面板完全攻略：画面特效+人物特效", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "1h", "desc": "特效是剪映的核心卖点", "materials": "各种特效对比素材"},
        {"title": "转场面板详解：叠化/闪白/幻灯片/特效转场", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "1h", "desc": "转场的入门预览", "materials": "两段素材+各种转场对比"},
        {"title": "素材替换功能：换素材不换效果的神技", "diff": 1, "type": "干货", "duration": "1min", "viral": "中", "time": "20min", "desc": "提高剪辑效率的实用技巧", "materials": "剪映素材替换演示"},
        {"title": "剪映模板怎么用？一键套用+二次修改", "diff": 1, "type": "爆款", "duration": "20s", "viral": "高", "time": "30min", "desc": "模板是新手最快的入门方式", "materials": "剪映模板广场截图"},
    ],

    "转场特效": [
        {"title": "3种基础转场：叠化/闪白/滑动的正确用法", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "转场不是花里胡哨就好", "materials": "多段素材"},
        {"title": "遮罩转场：用蒙版做丝滑无缝转场", "diff": 2, "type": "爆款", "duration": "25s", "viral": "高", "time": "1h", "desc": "视觉效果极强，适合爆款", "materials": "两段运动方向一致的素材"},
        {"title": "匹配剪辑：同方向运动转场的秘密", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "拍摄时就要想到剪辑", "materials": "多段同方向运动素材"},
        {"title": "甩镜头转场：一甩就切走", "diff": 2, "type": "爆款", "duration": "20s", "viral": "高", "time": "40min", "desc": "简单但效果炸裂", "materials": "快速甩动镜头素材"},
        {"title": "遮挡转场：用手或物体遮住镜头", "diff": 2, "type": "爆款", "duration": "20s", "viral": "高", "time": "40min", "desc": "拍摄+剪辑结合的经典案例", "materials": "遮挡镜头+切换场景的素材"},
        {"title": "缩放转场：从小变大的视觉冲击", "diff": 2, "type": "爆款", "duration": "20s", "viral": "高", "time": "40min", "desc": "关键帧做缩放转场", "materials": "两段有视觉关联的素材"},
        {"title": "旋转转场：让画面转起来", "diff": 2, "type": "爆款", "duration": "20s", "viral": "高", "time": "40min", "desc": "适合旅行/运动类视频", "materials": "多段运动素材"},
        {"title": "亮度键转场：利用过曝做无缝切换", "diff": 3, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "稍微进阶的技巧", "materials": "亮色背景素材"},
        {"title": "无缝转场的拍摄要点：前期拍好后期省事", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "1.5h", "desc": "拍摄+剪辑结合", "materials": "拍摄现场+成片对比"},
        {"title": "最近爆火的3个转场模板复刻", "diff": 2, "type": "爆款", "duration": "30s", "viral": "高", "time": "1.5h", "desc": "蹭热点，涨粉利器", "materials": "抖音热门转场视频"},
    ],

    "卡点节奏": [
        {"title": "自动踩点：让剪映帮你卡点，一键到位", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "40min", "desc": "卡点入门第一课", "materials": "节奏感强的BGM+多段素材"},
        {"title": "手动卡点：精确到帧的节奏控制", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "1h", "desc": "自动踩点不够用的时候", "materials": "快节奏BGM"},
        {"title": "变速卡点：快慢交替的节奏感，帅炸了", "diff": 2, "type": "爆款", "duration": "25s", "viral": "高", "time": "1h", "desc": "视觉节奏感极强", "materials": "有快慢变化的运动素材"},
        {"title": "多镜头卡点混剪：10个镜头10个节拍", "diff": 2, "type": "爆款", "duration": "20s", "viral": "高", "time": "1.5h", "desc": "混剪是涨粉好方向", "materials": "10段以上同主题素材"},
        {"title": "音效+卡点组合拳：让节奏感翻倍", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "音效是卡点的放大器", "materials": "卡点视频+对应音效"},
        {"title": "慢歌卡点 vs 快歌卡点：不同的节奏策略", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "1h", "desc": "不同曲风的卡点逻辑", "materials": "慢歌和快歌各一段素材"},
        {"title": "画面切换频率的节奏密码", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "剪辑节奏感的底层逻辑", "materials": "不同切换频率对比"},
    ],

    "调色教程": [
        {"title": "调色基础三件套：亮度/对比度/饱和度", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "1h", "desc": "调色入门必学", "materials": "需要调色的原片"},
        {"title": "色温色调：冷调vs暖调，氛围感的关键", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "色温决定画面情绪", "materials": "同一场景不同色温对比"},
        {"title": "HSL调色：单独调整画面中某一种颜色", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "1h", "desc": "调色的进阶核心技能", "materials": "含特定颜色的素材（蓝天/绿植等）"},
        {"title": "曲线调色入门：一个工具搞定80%的调色", "diff": 3, "type": "干货", "duration": "3min", "viral": "中", "time": "1.5h", "desc": "曲线是调色的灵魂", "materials": "不同场景素材"},
        {"title": "滤镜+手动调色的组合用法：别只套滤镜", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "滤镜减半+手动微调", "materials": "套滤镜前后对比"},
        {"title": "电影感青橙色调：3步让你的视频变高级", "diff": 2, "type": "爆款", "duration": "25s", "viral": "高", "time": "1h", "desc": "最受欢迎的调色风格之一", "materials": "城市/街景素材"},
        {"title": "日系清新风格调色：干净透亮的秘诀", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "适合Vlog/生活方式类", "materials": "户外/生活场景素材"},
        {"title": "复古胶片风格调色：怀旧氛围拉满", "diff": 2, "type": "爆款", "duration": "25s", "viral": "高", "time": "1h", "desc": "胶片风一直很火", "materials": "适合复古风的素材"},
        {"title": "人像肤色还原：别把人调成黄脸婆", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "有人出镜的必备技能", "materials": "人像素材"},
        {"title": "美食调色：让食物看起来更好吃", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "美食博主必学", "materials": "美食素材"},
        {"title": "LUT导入与使用：一键套用电影级调色", "diff": 2, "type": "爆款", "duration": "25s", "viral": "高", "time": "40min", "desc": "LUT是最简单的调色方式", "materials": "LUT文件+适用素材"},
    ],

    "文字动画": [
        {"title": "文字逐个出现的效果：3种方法", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "打字机效果的前置技能", "materials": "剪映文字功能"},
        {"title": "打字机效果：文字一个一个字跳出来", "diff": 2, "type": "爆款", "duration": "20s", "viral": "高", "time": "40min", "desc": "综艺感十足", "materials": "一段需要文字展示的视频"},
        {"title": "文字跟随人物运动：跟踪文字的玩法", "diff": 3, "type": "干货", "duration": "2min", "viral": "中", "time": "1.5h", "desc": "关键帧+文字的组合", "materials": "人物运动素材"},
        {"title": "标题入场+退场动画组合：让片头更高级", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "标题是视频的门面", "materials": "不同风格标题示例"},
        {"title": "综艺花字效果：让你的视频更有趣", "diff": 2, "type": "爆款", "duration": "25s", "viral": "高", "time": "1h", "desc": "娱乐向内容必备", "materials": "有趣/搞笑的片段"},
        {"title": "歌词字幕逐字变色：KTV效果", "diff": 2, "type": "爆款", "duration": "20s", "viral": "高", "time": "40min", "desc": "音乐类账号最爱", "materials": "音乐+歌词"},
        {"title": "文字蒙版效果：让文字里有画面", "diff": 3, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "蒙版+文字的创意组合", "materials": "好看的画面+粗字体"},
    ],

    "蒙版&关键帧": [
        {"title": "什么是蒙版？5分钟彻底搞懂", "diff": 3, "type": "干货", "duration": "5min", "viral": "中", "time": "1.5h", "desc": "进阶最重要的概念", "materials": "蒙版演示素材"},
        {"title": "线性蒙版的6种创意用法", "diff": 3, "type": "干货", "duration": "3min", "viral": "中", "time": "1.5h", "desc": "一个蒙版打通关", "materials": "多种场景素材"},
        {"title": "圆形蒙版的创意玩法：画中画的进阶", "diff": 3, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "圆形蒙版做聚光灯效果", "materials": "适合圆形构图的素材"},
        {"title": "什么是关键帧？入门必看！", "diff": 3, "type": "干货", "duration": "5min", "viral": "中", "time": "1.5h", "desc": "关键帧是动画的灵魂", "materials": "剪映关键帧演示"},
        {"title": "关键帧+蒙版=无限可能", "diff": 3, "type": "干货", "duration": "3min", "viral": "中", "time": "1.5h", "desc": "两个核心工具的组合", "materials": "复杂效果演示"},
        {"title": "关键帧做画面移动：让静态图动起来", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "Ken Burns效果", "materials": "高清照片"},
        {"title": "关键帧做缩放动画：推拉镜头效果", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "让平面素材有空间感", "materials": "照片或视频"},
        {"title": "关键帧做透明度变化：若隐若现的效果", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "40min", "desc": "做回忆/梦境效果", "materials": "两段叠加的素材"},
        {"title": "蒙版+关键帧综合案例：3个效果一次学会", "diff": 3, "type": "干货", "duration": "4min", "viral": "中", "time": "2h", "desc": "综合实战演练", "materials": "多种素材"},
    ],

    "抠像&合成": [
        {"title": "智能抠像：一键去背景，太方便了", "diff": 2, "type": "爆款", "duration": "20s", "viral": "高", "time": "30min", "desc": "AI抠像效果惊艳", "materials": "有人物的素材"},
        {"title": "自定义抠像：精细调整边缘", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "智能抠像不够用的时候", "materials": "复杂轮廓的人物素材"},
        {"title": "绿幕抠像基础：在家拍出任意背景", "diff": 3, "type": "干货", "duration": "3min", "viral": "中", "time": "1.5h", "desc": "低成本特效的秘密", "materials": "绿幕素材+背景素材"},
        {"title": "人物+文字合成效果：让文字出现在人后面", "diff": 3, "type": "爆款", "duration": "25s", "viral": "高", "time": "1h", "desc": "抠像+文字的组合玩法", "materials": "人物素材+文字"},
        {"title": "分身效果：让3个自己同框出现", "diff": 3, "type": "爆款", "duration": "25s", "viral": "高", "time": "1.5h", "desc": "趣味性强，容易传播", "materials": "三脚架固定拍摄的3段素材"},
        {"title": "换背景实战：把日常场景变成大片现场", "diff": 2, "type": "爆款", "duration": "25s", "viral": "高", "time": "1h", "desc": "视觉冲击力强", "materials": "人物抠像素材+大片背景"},
    ],

    "音频处理": [
        {"title": "怎么选BGM？3个原则让你不再纠结", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "1h", "desc": "选音乐是剪辑的第一道坎", "materials": "不同风格的BGM列表"},
        {"title": "抖音热歌BGM推荐清单（本月更新）", "diff": 1, "type": "爆款", "duration": "30s", "viral": "高", "time": "1.5h", "desc": "时效性内容，定期更新", "materials": "本月抖音热歌榜"},
        {"title": "音效使用大全：100个常用音效分类整理", "diff": 1, "type": "干货", "duration": "3min", "viral": "中", "time": "2h", "desc": "工具型内容，收藏率高", "materials": "剪映音效库"},
        {"title": "音频分离与提取：把视频里的声音拿出来", "diff": 1, "type": "干货", "duration": "1min", "viral": "中", "time": "30min", "desc": "实用小技巧", "materials": "含想要音频的视频"},
        {"title": "变声效果怎么用？5种变声场景", "diff": 1, "type": "干货", "duration": "2min", "viral": "中", "time": "40min", "desc": "增加趣味性", "materials": "需要变声的配音"},
        {"title": "混音技巧：人声+BGM的黄金比例", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "让声音更专业的秘诀", "materials": "同时有人声和BGM的视频"},
        {"title": "让声音更有质感的3个技巧", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "EQ/降噪/增强", "materials": "录音素材"},
        {"title": "消除背景噪音：让声音变干净的魔法", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "40min", "desc": "降噪是最刚需的功能", "materials": "有噪音的录音"},
        {"title": "自己录音的5个注意事项", "diff": 1, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "好的录音是好的剪辑的基础", "materials": "录音设备/环境展示"},
    ],

    "拍摄技巧": [
        {"title": "手机拍视频的基础设置：4个开关一定要调", "diff": 1, "type": "干货", "duration": "2min", "viral": "中", "time": "40min", "desc": "拍摄前的准备工作", "materials": "手机设置界面截图"},
        {"title": "九宫格构图的5种用法：新手必学", "diff": 1, "type": "干货", "duration": "3min", "viral": "中", "time": "1.5h", "desc": "构图是拍摄的第一课", "materials": "5种九宫格构图示例"},
        {"title": "引导线构图：让观众视线跟着你走", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "进阶构图技巧", "materials": "含引导线的场景素材"},
        {"title": "对称构图：强迫症看了极度舒适", "diff": 1, "type": "爆款", "duration": "20s", "viral": "高", "time": "1h", "desc": "对称画面天然适合短视频", "materials": "对称场景素材"},
        {"title": "前景构图：增加画面层次感的秘诀", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "让画面不再扁平", "materials": "有前景和无前景的对比"},
        {"title": "5种基础运镜：推拉摇移跟一次学会", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "2h", "desc": "运镜是动态构图的灵魂", "materials": "5种运镜的示例素材"},
        {"title": "手持拍摄防抖的5个技巧：不用稳定器", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "1.5h", "desc": "低成本拍出稳定画面", "materials": "手持拍摄对比素材"},
        {"title": "利用自然光拍出质感：窗户光是最好的灯光", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "不花钱的打光技巧", "materials": "不同光线的对比素材"},
        {"title": "逆光拍摄技巧：让人物发光的秘密", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "逆光是最好的人像光", "materials": "逆光人像示例"},
        {"title": "B-roll拍摄技巧：让视频质感提升10倍", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "2h", "desc": "B-roll是视频质感的来源", "materials": "A-roll+B-roll对比示例"},
        {"title": "空镜怎么拍才有感觉？3个心法", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1h", "desc": "空镜是过渡和氛围的关键", "materials": "有意境的空镜素材"},
        {"title": "拍摄时的剪辑思维：给后期留余地", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "1.5h", "desc": "核心差异化内容", "materials": "拍摄现场+后期成品对比"},
        {"title": "多机位拍摄：一个场景多个角度", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1.5h", "desc": "让你的剪辑有素材可剪", "materials": "多机位同场景素材"},
        {"title": "室内打光入门：一盏灯也能拍出质感", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "1.5h", "desc": "室内拍摄的基础", "materials": "不同灯光布置对比"},
    ],

    "热门跟拍": [
        {"title": "本月最火的3个剪映模板复刻", "diff": 2, "type": "爆款", "duration": "30s", "viral": "高", "time": "1.5h", "desc": "蹭热点，每月更新", "materials": "抖音热门模板视频"},
        {"title": "最近流行的XX风格剪辑拆解", "diff": 2, "type": "干货", "duration": "2min", "viral": "中", "time": "1.5h", "desc": "拆解流行风格的底层逻辑", "materials": "当前流行的视频案例"},
        {"title": "某条500万播放的视频怎么剪的？逐帧拆解", "diff": 3, "type": "深度", "duration": "4min", "viral": "高", "time": "3h", "desc": "爆款拆解是流量密码", "materials": "爆款视频+工程文件"},
        {"title": "抖音最新特效怎么用？第一时间教你", "diff": 1, "type": "爆款", "duration": "20s", "viral": "高", "time": "40min", "desc": "新特效是流量红利期", "materials": "抖音最新特效"},
        {"title": "剪映新功能第一时间测评+教程", "diff": 2, "type": "爆款", "duration": "30s", "viral": "高", "time": "1.5h", "desc": "新功能 = 流量密码", "materials": "剪映新版本"},
        {"title": "本周抖音最火的BGM+对应的剪辑风格", "diff": 1, "type": "爆款", "duration": "25s", "viral": "高", "time": "1h", "desc": "BGM是热点的风向标", "materials": "本周热门BGM列表"},
    ],

    "案例实战": [
        {"title": "日常Vlog从拍到剪全流程：普通的一天怎么剪", "diff": 2, "type": "深度", "duration": "5min", "viral": "中", "time": "4h", "desc": "最接地气的完整案例", "materials": "一整天拍摄的Vlog素材"},
        {"title": "旅行短片：200段素材怎么整理和剪辑", "diff": 3, "type": "深度", "duration": "5min", "viral": "中", "time": "4h", "desc": "素材管理是剪辑效率的关键", "materials": "旅行拍摄的素材库"},
        {"title": "产品展示视频：用手机拍出广告级质感", "diff": 3, "type": "深度", "duration": "4min", "viral": "中", "time": "3h", "desc": "带货/产品类账号必备", "materials": "一个产品+拍摄道具"},
        {"title": "美食视频：从拍到剪让食物更有食欲", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "2.5h", "desc": "美食赛道热门方向", "materials": "美食制作过程素材"},
        {"title": "卡点混剪实战：用旅拍素材剪一条燃向视频", "diff": 2, "type": "干货", "duration": "3min", "viral": "中", "time": "2h", "desc": "混剪的全流程", "materials": "多段旅行/运动素材"},
        {"title": "情绪短片：让人看完起鸡皮疙瘩的剪辑手法", "diff": 3, "type": "深度", "duration": "4min", "viral": "中", "time": "3h", "desc": "情感共鸣类内容", "materials": "情绪向素材+BGM"},
        {"title": "低成本拍出高级感：200块预算的拍摄挑战", "diff": 3, "type": "爆款", "duration": "4min", "viral": "高", "time": "4h", "desc": "反差感强，容易传播", "materials": "低成本道具+创意拍摄"},
        {"title": "用手机+剪映复刻一条品牌广告", "diff": 4, "type": "深度", "duration": "5min", "viral": "高", "time": "5h", "desc": "展示技术上限的标杆内容", "materials": "品牌广告原片+仿拍素材"},
        {"title": "一条视频从0到发布的全过程（含脚本/拍摄/剪辑）", "diff": 3, "type": "深度", "duration": "5min", "viral": "中", "time": "4h", "desc": "最完整的创作流程展示", "materials": "完整创作过程记录"},
        {"title": "普通人拍视频最容易犯的10个错误（合集修正）", "diff": 2, "type": "干货", "duration": "4min", "viral": "高", "time": "3h", "desc": "错误合集容易引发共鸣和讨论", "materials": "常见错误案例+正确示范"},
    ],
}


# ============================================================
# 日历生成逻辑
# ============================================================

def generate_calendar(total_episodes: int = 200) -> list:
    """
    生成内容日历
    策略：
    - 第1-30期：基础操作+拍摄为主，小白友好
    - 第31-100期：转场/卡点/调色/音频，技能进阶
    - 第101-200期：蒙版/关键帧/抠像/合成/案例实战，深度内容
    - 同时穿插爆款层、干货层、深度层维持30/50/20比例
    """
    calendar = []

    # 按阶段规划分类权重
    stage_1_cats = {  # 第1-30期：基础为主
        "剪映基础操作": 12,
        "拍摄技巧": 6,
        "热门跟拍": 3,
        "卡点节奏": 2,
        "转场特效": 2,
        "音频处理": 2,
        "调色教程": 2,
        "文字动画": 1,
    }

    stage_2_cats = {  # 第31-100期：进阶为主
        "转场特效": 10,
        "卡点节奏": 8,
        "调色教程": 12,
        "文字动画": 8,
        "音频处理": 8,
        "蒙版&关键帧": 6,
        "拍摄技巧": 8,
        "热门跟拍": 5,
        "抠像&合成": 3,
        "案例实战": 2,
    }

    stage_3_cats = {  # 第101-200期：深度为主
        "蒙版&关键帧": 15,
        "抠像&合成": 12,
        "调色教程": 10,
        "案例实战": 20,
        "拍摄技巧": 15,
        "转场特效": 8,
        "文字动画": 6,
        "卡点节奏": 5,
        "热门跟拍": 5,
        "音频处理": 4,
    }

    def pick_topics_from_category(category: str, count: int, used_titles: set) -> list:
        """从指定分类中选取未使用的选题，不足时自动衍生"""
        seeds = TOPIC_SEEDS.get(category, [])
        available = [dict(s) for s in seeds if s["title"] not in used_titles]
        result = available[:count]

        # 如果种子不足，从已有种子衍生变体
        if len(result) < count:
            variants = [
                ("进阶版", "进阶技巧+实战", 1),
                ("实战篇", "实际案例演示", 1),
                ("3种方法", "多种方法对比", 0),
                ("新手必看", "面向零基础", -1),
                ("避坑指南", "常见错误+正确做法", 0),
                ("效率技巧", "提高剪辑效率", 0),
                ("创意玩法", "创意效果演示", 1),
            ]
            base_idx = 0
            while len(result) < count:
                seed = seeds[base_idx % len(seeds)]
                for prefix, desc_mod, diff_mod in variants:
                    if len(result) >= count:
                        break
                    new_title = f"{prefix}：{seed['title'].split('：')[-1] if '：' in seed['title'] else seed['title']}"
                    if new_title not in used_titles:
                        new_topic = dict(seed)
                        new_topic["title"] = new_title
                        new_topic["desc"] = seed.get("desc", "") + " | " + desc_mod
                        new_topic["diff"] = min(5, max(1, seed.get("diff", 2) + diff_mod))
                        result.append(new_topic)
                base_idx += 1

        return result[:count]

    def build_stage_calendar(
        cat_weights: dict,
        start_num: int,
        used_titles: set,
    ) -> list:
        """按分类权重构建一个阶段的日历"""
        stage_topics = []
        for cat, count in cat_weights.items():
            picked = pick_topics_from_category(cat, count, used_titles)
            for t in picked:
                used_titles.add(t["title"])
                stage_topics.append({**t, "category": cat})
        return stage_topics

    used_titles = set()

    # 构建三个阶段
    stage1 = build_stage_calendar(stage_1_cats, 1, used_titles)
    stage2 = build_stage_calendar(stage_2_cats, 31, used_titles)
    stage3 = build_stage_calendar(stage_3_cats, 101, used_titles)

    all_topics = stage1 + stage2 + stage3

    # 控制内容类型比例（30%爆款/50%干货/20%深度）
    # 在阶段内做类型穿插
    def interleave_types(topics: list) -> list:
        """按类型穿插排列，保持节奏感"""
        viral = [t for t in topics if t.get("type") == "爆款"]
        dry = [t for t in topics if t.get("type") == "干货"]
        deep = [t for t in topics if t.get("type") == "深度"]

        result = []
        vi, di, dei = 0, 0, 0

        while vi < len(viral) or di < len(dry) or dei < len(deep):
            # 每3条插入1条爆款
            if dei < len(deep) and len(result) % 8 == 0:
                result.append(deep[dei])
                dei += 1
            elif vi < len(viral) and len(result) % 3 == 0:
                result.append(viral[vi])
                vi += 1
            elif di < len(dry):
                result.append(dry[di])
                di += 1
            elif vi < len(viral):
                result.append(viral[vi])
                vi += 1
            elif dei < len(deep):
                result.append(deep[dei])
                dei += 1

        return result

    all_topics = interleave_types(all_topics)

    # 构建最终的日历列表
    for i, topic in enumerate(all_topics[:total_episodes]):
        episode_num = i + 1

        # 确定阶段
        if episode_num <= 30:
            stage = "冷启动期"
        elif episode_num <= 100:
            stage = "增长期"
        else:
            stage = "成熟期"

        entry = {
            "episode": episode_num,
            "title": topic["title"],
            "category": topic.get("category", ""),
            "difficulty": topic.get("diff", 2),
            "content_type": topic.get("type", "干货"),
            "estimated_duration": topic.get("duration", "2min"),
            "viral_potential": topic.get("viral", "中"),
            "production_time": topic.get("time", "1h"),
            "description": topic.get("desc", ""),
            "materials_needed": topic.get("materials", ""),
            "stage": stage,
            "status": "待发布",
        }
        calendar.append(entry)

    return calendar


def calendar_to_markdown(calendar: list) -> str:
    """将日历转为可读的 Markdown"""
    difficulty_map = {1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐", 4: "⭐⭐⭐⭐", 5: "⭐⭐⭐⭐⭐"}

    lines = [
        f"# 🎬 拍摄+剪辑教学 — {len(calendar)}期完整内容日历",
        "",
        "> 按难度梯度：前30期小白友好 → 31-100期进阶 → 101+高级深度",
        "> 内容节奏：每3-4条干货穿插1条爆款，每8条穿插1条深度案例",
        "",
        "---",
        "",
    ]

    # 按阶段分组输出
    stages = {"冷启动期": [], "增长期": [], "成熟期": []}
    for entry in calendar:
        stages[entry["stage"]].append(entry)

    for stage_name, entries in stages.items():
        if not entries:
            continue
        lines.append(f"## {stage_name}（第{entries[0]['episode']}-{entries[-1]['episode']}期）")
        lines.append("")

        for e in entries:
            diff = difficulty_map.get(e["difficulty"], "⭐⭐")
            type_emoji = {"爆款": "🔺", "干货": "🔸", "深度": "🔹"}.get(e["content_type"], "")
            lines.append(f"### 第{e['episode']}期 {type_emoji} {e['title']}")
            lines.append(f"- **分类**：{e['category']} | **难度**：{diff} | **时长**：{e['estimated_duration']}")
            lines.append(f"- **涨粉潜力**：{e['viral_potential']} | **制作耗时**：{e['production_time']}")
            if e.get("description"):
                lines.append(f"- **说明**：{e['description']}")
            if e.get("materials_needed"):
                lines.append(f"- **所需素材**：{e['materials_needed']}")
            lines.append("")

    lines.append("---")
    lines.append(f"*日历生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    lines.append(f"*总计 {len(calendar)} 期，覆盖 11 大分类*")
    lines.append("")
    lines.append("## 分类覆盖统计")
    lines.append("")

    cat_counts = {}
    for e in calendar:
        cat = e["category"]
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- **{cat}**：{count} 期")

    return "\n".join(lines)


def save_calendar(calendar: list):
    """保存日历到 JSON 和 Markdown"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # JSON 格式
    json_path = os.path.join(DATA_DIR, "200期日历.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(calendar, f, ensure_ascii=False, indent=2)

    # Markdown 格式
    md_path = os.path.join(OUTPUT_DIR, "200期日历.md")
    md_content = calendar_to_markdown(calendar)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"✅ 日历已保存：")
    print(f"   JSON → {json_path}")
    print(f"   MD   → {md_path}")


def populate_topics_db(calendar: list):
    """将日历选题批量写入 topics_db.json"""
    # 使用 topic_manager 的接口
    import sys
    sys.path.insert(0, os.path.join(BASE_DIR, "脚本"))
    from topic_manager import load_topics_db, save_topics_db

    db = load_topics_db()
    existing_titles = {t["title"] for t in db["topics"]}

    new_count = 0
    for entry in calendar:
        if entry["title"] not in existing_titles:
            topic = {
                "id": f"topic_{len(db['topics']) + new_count + 1:04d}",
                "title": entry["title"],
                "category": entry["category"],
                "difficulty": entry["difficulty"],
                "content_type": entry["content_type"],
                "description": entry.get("description", ""),
                "estimated_duration": entry.get("estimated_duration", ""),
                "materials_needed": entry.get("materials_needed", ""),
                "viral_potential": entry.get("viral_potential", "中"),
                "production_time": entry.get("production_time", ""),
                "status": "待发布",
                "created_at": datetime.now().strftime("%Y-%m-%d"),
                "published_at": None,
                "douyin_url": None,
                "performance": None,
            }
            db["topics"].append(topic)
            existing_titles.add(entry["title"])
            new_count += 1

    save_topics_db(db)
    print(f"✅ 选题数据库已更新：新增 {new_count} 条选题")


# ============================================================
# 主入口
# ============================================================

if __name__ == "__main__":
    print("🎬 正在生成 200 期内容日历...")
    print(f"   种子库共 {sum(len(v) for v in TOPIC_SEEDS.values())} 条种子选题")
    print()

    calendar = generate_calendar(total_episodes=200)

    print(f"📅 已生成 {len(calendar)} 期选题")
    print()

    # 统计
    cat_counts = {}
    type_counts = {}
    for e in calendar:
        cat_counts[e["category"]] = cat_counts.get(e["category"], 0) + 1
        type_counts[e["content_type"]] = type_counts.get(e["content_type"], 0) + 1

    print("📊 分类分布：")
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f"   {cat}: {count}期")

    print()
    print("📊 内容类型分布：")
    for t, count in type_counts.items():
        pct = count / len(calendar) * 100
        print(f"   {t}: {count}期 ({pct:.0f}%)")

    print()
    save_calendar(calendar)

    print()
    populate_topics_db(calendar)

    print()
    print("🎉 内容日历生成完毕！")
