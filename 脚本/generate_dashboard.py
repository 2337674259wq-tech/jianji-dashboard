# -*- coding: utf-8 -*-
"""
MG 动效版仪表盘生成器 v2
数据通过 <script type="application/json"> 嵌入，零转义风险
JS 防御式编程：DOMContentLoaded + try/catch + 传统循环
"""
import json, os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "数据", "选题库.json")
CAL_PATH = os.path.join(BASE, "数据", "200期日历.json")
PUB_PATH = os.path.join(BASE, "数据", "已发布.json")
HTML_PATH = os.path.join(BASE, "仪表盘.html")
INDEX_PATH = os.path.join(BASE, "index.html")

CSS = '''
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{
    --bg:#f6f7fa;--card:#fff;
    --text:#111318;--text2:#555a66;--text3:#8a8e9a;
    --border:#e5e7ed;--border2:#dcdde6;
    --accent:#0055e8;--accent2:#003bb5;
    --red:#d92d20;--orange:#e04f16;--green:#188038;--purple:#7a1eb8;
    --radius:16px;
    --shadow-sm:0 1px 3px rgba(0,0,0,.04);
    --shadow:0 2px 8px rgba(0,0,0,.05),0 8px 24px rgba(0,0,0,.04);
    --shadow-lg:0 8px 30px rgba(0,0,0,.07),0 20px 60px rgba(0,0,0,.04);
    --spring:cubic-bezier(0.34,1.56,0.64,1);
    --bounce:cubic-bezier(0.68,-0.55,0.27,1.55);
    --smooth:cubic-bezier(0.22,0.61,0.36,1);
    font-family:"Segoe UI Variable Text","Segoe UI","Noto Sans SC","Microsoft YaHei",sans-serif;
    background:var(--bg);color:var(--text);
    -webkit-font-smoothing:antialiased;line-height:1.55;overflow-x:hidden;
}
h1,h2,h3,h4{font-family:"Segoe UI Variable Display","Segoe UI","Noto Sans SC","Microsoft YaHei",sans-serif;letter-spacing:-.025em}

#particles-canvas{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;opacity:.4}

.geo-shapes{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden}
.geo{position:absolute;opacity:.05;animation:geoFloat 14s var(--spring) infinite}
@keyframes geoFloat{
    0%,100%{transform:translate(0,0) rotate(0deg) scale(1)}
    20%{transform:translate(25px,-40px) rotate(72deg) scale(1.3)}
    40%{transform:translate(-15px,-80px) rotate(144deg) scale(.85)}
    60%{transform:translate(-35px,-20px) rotate(216deg) scale(1.15)}
    80%{transform:translate(20px,-60px) rotate(288deg) scale(.9)}
}
.geo.circle{border-radius:50%;border:2px solid var(--accent)}
.geo.square{border-radius:4px;border:2px solid var(--purple)}
.geo.dot{border-radius:50%;background:var(--accent)!important;border:none!important}
.geo.ring{border-radius:50%;border:2px dashed var(--accent);background:none!important}
.geo.triangle{width:0!important;height:0!important;border:none!important;border-left:solid transparent;border-right:solid transparent;border-bottom:solid var(--accent);background:none!important}

@keyframes springIn{0%{opacity:0;transform:scale(.3) translateY(60px)}60%{opacity:1;transform:scale(1.08) translateY(-4px)}80%{transform:scale(.96) translateY(2px)}100%{opacity:1;transform:scale(1) translateY(0)}}
@keyframes springInUp{0%{opacity:0;transform:translateY(50px) scale(.85)}60%{opacity:1;transform:translateY(-6px) scale(1.03)}80%{transform:translateY(2px) scale(.98)}100%{opacity:1;transform:translateY(0) scale(1)}}
@keyframes fadeSlideUp{0%{opacity:0;transform:translateY(30px)}100%{opacity:1;transform:translateY(0)}}

.wrap{max-width:1240px;margin:0 auto;padding:0 28px;position:relative;z-index:1}

nav{position:sticky;top:0;z-index:100;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
    background:rgba(246,247,250,.82);border-bottom:1px solid var(--border);padding:14px 0}
nav .nav-inner{max-width:1240px;margin:0 auto;padding:0 28px;display:flex;align-items:center;justify-content:space-between}
nav .logo{font-size:18px;font-weight:800;color:var(--text);letter-spacing:-.3px;display:flex;align-items:center;gap:10px}
nav .logo .dot{width:10px;height:10px;border-radius:50%;background:var(--accent);box-shadow:0 0 14px rgba(0,85,232,.3)}
nav .tabs{display:flex;gap:4px;background:rgba(0,0,0,.03);border-radius:10px;padding:3px}
nav .tabs button{border:none;background:none;padding:7px 18px;border-radius:8px;font-size:13px;font-weight:600;color:var(--text2);cursor:pointer;transition:all .2s var(--spring);font-family:inherit}
nav .tabs button:hover{color:var(--text)}
nav .tabs button.active{background:var(--card);color:var(--accent);box-shadow:0 1px 3px rgba(0,0,0,.06)}
nav .time{font-size:11px;color:var(--text3);letter-spacing:.5px;font-feature-settings:"tnum"}
@media(max-width:768px){nav .time{display:none}nav .tabs button{padding:6px 11px;font-size:11px}}

section{display:none;animation:fadeSlideUp .45s var(--smooth);padding:0 0 60px}
section.active{display:block}

.hero{position:relative;padding:80px 0 48px;overflow:visible}
.hero-bg{position:absolute;inset:-60px -50px;pointer-events:none;z-index:0;
    background:radial-gradient(ellipse 60% 40% at 50% 0%,rgba(0,85,232,.04) 0%,transparent 60%),
    radial-gradient(ellipse 30% 40% at 85% 100%,rgba(0,85,232,.02) 0%,transparent 50%)}
.hero-glow{position:absolute;width:500px;height:500px;border-radius:50%;filter:blur(130px);opacity:.07;pointer-events:none;z-index:0;animation:glowFloat 10s var(--smooth) infinite}
.hero-glow.g1{top:-250px;left:5%;background:radial-gradient(circle,#0055e8,transparent 70%)}
.hero-glow.g2{top:10%;right:-150px;background:radial-gradient(circle,#7a1eb8,transparent 70%);animation-delay:-5s}
@keyframes glowFloat{0%,100%{transform:translate(0,0) scale(1)}33%{transform:translate(35px,-25px) scale(1.2)}66%{transform:translate(-20px,12px) scale(.85)}}

.hero-toy{position:absolute;pointer-events:none;z-index:0}
.hero-toy.t1{top:18%;left:8%;width:55px;height:55px;border:3px solid var(--accent);border-radius:50%;opacity:.05;animation:toyBounce 8s var(--spring) infinite}
.hero-toy.t2{top:35%;right:12%;width:38px;height:38px;background:var(--accent);border-radius:8px;opacity:.03;animation:toyBounce 10s var(--spring) infinite;transform:rotate(45deg);animation-delay:-4s}
.hero-toy.t3{bottom:15%;left:18%;width:45px;height:45px;border:3px dashed var(--purple);border-radius:50%;opacity:.04;animation:toySpin 12s linear infinite}
.hero-toy.t4{top:22%;right:28%;width:22px;height:22px;border-radius:50%;background:var(--purple);opacity:.03;animation:toyBounce 7s var(--spring) infinite;animation-delay:-6s}
@keyframes toyBounce{0%,100%{transform:translateY(0) rotate(0deg)}30%{transform:translateY(-45px) rotate(55deg)}60%{transform:translateY(-18px) rotate(110deg)}80%{transform:translateY(-30px) rotate(165deg)}}
@keyframes toySpin{0%{transform:rotate(0deg) scale(1)}50%{transform:rotate(180deg) scale(1.35)}100%{transform:rotate(360deg) scale(1)}}

.hero .label{position:relative;display:inline-block;padding:6px 20px;border-radius:24px;background:rgba(0,85,232,.05);color:var(--accent);font-size:12px;font-weight:700;letter-spacing:.8px;margin-bottom:22px;z-index:1;
    text-shadow:0 0 20px rgba(0,85,232,.1);box-shadow:0 2px 12px rgba(0,85,232,.04),inset 0 1px 0 rgba(255,255,255,.5);
    animation:springIn .7s var(--spring) .1s both}
.hero h1{position:relative;font-size:clamp(38px,5.5vw,68px);font-weight:800;line-height:1.08;margin-bottom:16px;z-index:1;
    text-shadow:0 2px 4px rgba(0,0,0,.03),0 8px 28px rgba(0,85,232,.05);
    animation:springIn .8s var(--spring) .2s both}
.hero h1 em{font-style:normal;
    background:linear-gradient(135deg,#0055e8 0%,#7a1eb8 40%,#e04f16 70%,#0055e8 100%);
    background-size:300% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
    display:inline-block;animation:shimmer 4s linear infinite;
    filter:drop-shadow(0 4px 8px rgba(0,85,232,.15))}
@keyframes shimmer{0%{background-position:0% center}100%{background-position:300% center}}
.hero .sub{position:relative;font-size:clamp(15px,1.8vw,18px);color:var(--text2);max-width:540px;margin-bottom:36px;z-index:1;
    text-shadow:0 1px 2px rgba(0,0,0,.02);animation:fadeSlideUp .6s var(--smooth) .3s both}
.hero-stats{position:relative;display:flex;gap:40px;flex-wrap:wrap;z-index:1}
.hero-stat{animation:springInUp .65s var(--spring) both}
.hero-stat:nth-child(1){animation-delay:.35s}.hero-stat:nth-child(2){animation-delay:.42s}.hero-stat:nth-child(3){animation-delay:.49s}.hero-stat:nth-child(4){animation-delay:.56s}
.hero-stat .num{font-size:38px;font-weight:800;font-family:"Segoe UI Variable Display","Segoe UI","Noto Sans SC",sans-serif;color:var(--accent);line-height:1;
    text-shadow:0 2px 8px rgba(0,85,232,.1);transition:transform .3s var(--spring);font-feature-settings:"tnum"}
.hero-stat:hover .num{transform:scale(1.12)}
.hero-stat .lbl{font-size:11px;color:var(--text3);margin-top:6px;text-transform:uppercase;letter-spacing:.8px;font-weight:700;
    text-shadow:0 1px 2px rgba(0,0,0,.02)}

.sec-hd{margin-bottom:24px}
.sec-hd .kicker{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.4px;color:var(--accent);margin-bottom:8px;
    text-shadow:0 0 18px rgba(0,85,232,.08)}
.sec-hd h2{font-size:clamp(24px,3.2vw,36px);font-weight:800;margin-bottom:4px;
    text-shadow:0 2px 3px rgba(0,0,0,.03),0 8px 24px rgba(0,85,232,.03)}
.sec-hd .sub{font-size:13px;color:var(--text3);text-shadow:0 1px 1px rgba(0,0,0,.01)}
.divider{width:100%;height:1px;background:var(--border);position:relative;overflow:hidden;margin:16px 0}
.divider::after{content:'';position:absolute;top:0;left:-100%;width:40%;height:100%;
    background:linear-gradient(90deg,transparent,rgba(0,85,232,.12),transparent);
    animation:dividerShine 5s var(--smooth) infinite}
@keyframes dividerShine{0%{left:-40%}100%{left:140%}}

.card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.card{
    position:relative;background:var(--card);border-radius:var(--radius);padding:28px 24px 38px;
    border:1px solid var(--border);overflow:hidden;cursor:pointer;
    transition:transform .4s var(--spring),box-shadow .4s var(--spring),border-color .3s ease;
    box-shadow:0 1px 3px rgba(0,0,0,.02),0 3px 14px rgba(0,0,0,.03);
    background-image:radial-gradient(circle at 100% 0%,rgba(0,85,232,.012) 0%,transparent 50%);
    animation:springInUp .6s var(--spring) both;
}
.card:hover{transform:translateY(-7px) scale(1.02);box-shadow:0 12px 38px rgba(0,85,232,.08),0 3px 10px rgba(0,0,0,.05);border-color:var(--accent)}
.card::after{content:'→';position:absolute;bottom:10px;right:16px;font-size:14px;color:var(--accent);opacity:0;transition:all .3s var(--spring);transform:translateX(-4px);font-weight:700}
.card:hover::after{opacity:1;transform:translateX(0)}
.card::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;
    background:radial-gradient(circle at var(--mx,50%) var(--my,50%),rgba(0,85,232,.04) 0%,transparent 50%);
    pointer-events:none;opacity:0;transition:opacity .4s ease;z-index:0}
.card:hover::before{opacity:1}
.card>*{position:relative;z-index:1}
.card-bar{position:absolute;top:0;left:0;right:0;height:3px;z-index:2;transition:height .2s var(--spring)}
.card:hover .card-bar{height:4px}
.card-bar.red{background:var(--red)}.card-bar.blue{background:var(--accent)}.card-bar.purple{background:var(--purple)}
.card-medal{font-size:26px;position:absolute;top:10px;right:14px;opacity:.1;transition:all .4s var(--spring)}
.card:hover .card-medal{opacity:.28;transform:scale(1.25) rotate(-6deg);filter:drop-shadow(0 4px 6px rgba(0,85,232,.15))}
.card .tag{display:inline-block;padding:2px 10px;border-radius:6px;font-size:10.5px;font-weight:700;letter-spacing:.3px;margin-bottom:10px}
.card .tag.red{background:rgba(217,45,32,.06);color:var(--red)}
.card .tag.blue{background:rgba(0,85,232,.06);color:var(--accent)}
.card .tag.purple{background:rgba(122,30,184,.06);color:var(--purple)}
.card .tag.gray{background:rgba(0,0,0,.03);color:var(--text3)}
.card h3{font-size:14.5px;font-weight:700;line-height:1.35;margin-bottom:8px;text-shadow:0 1px 2px rgba(0,0,0,.02)}
.card .meta{font-size:11.5px;color:var(--text2)}
.card.hidden{display:none}

.stage-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media(max-width:768px){.stage-grid{grid-template-columns:1fr}}
.stage-card{
    display:flex;gap:20px;align-items:flex-start;background:var(--card);border-radius:var(--radius);
    padding:28px 40px 28px 26px;border:1px solid var(--border);cursor:pointer;position:relative;overflow:hidden;
    transition:transform .4s var(--spring),box-shadow .4s var(--spring),border-color .3s ease;
    box-shadow:0 1px 3px rgba(0,0,0,.02),0 4px 16px rgba(0,0,0,.03);
    background-image:linear-gradient(135deg,rgba(0,85,232,.012) 0%,transparent 50%);
}
.stage-card:hover{transform:translateY(-5px) scale(1.012);box-shadow:0 12px 36px rgba(0,85,232,.08);border-color:var(--accent)}
.stage-card::after{content:'→';position:absolute;top:50%;right:16px;transform:translateY(-50%) translateX(-4px);font-size:18px;color:var(--accent);opacity:0;transition:all .3s var(--spring);font-weight:700}
.stage-card:hover::after{opacity:1;transform:translateY(-50%) translateX(0)}
.stage-num{font-size:42px;font-weight:900;color:var(--accent);opacity:.05;font-family:"Segoe UI Variable Display","Segoe UI","Noto Sans SC",sans-serif;line-height:1;flex-shrink:0;width:48px;text-align:center;transition:all .4s var(--spring);
    text-shadow:0 0 36px rgba(0,85,232,.25)}
.stage-card:hover .stage-num{opacity:.12;transform:scale(1.18)}
.stage-content h4{font-size:18px;font-weight:800;margin-bottom:4px;display:flex;align-items:center;gap:10px;text-shadow:0 1px 2px rgba(0,0,0,.03)}
.stage-content h4 span{font-size:12px;font-weight:600;color:var(--accent);letter-spacing:.2px;padding:2px 10px;border-radius:6px;background:rgba(0,85,232,.04)}
.stage-title{font-size:14px;font-weight:700;color:var(--text2);margin-bottom:6px}
.stage-desc{font-size:12.5px;color:var(--text3);line-height:1.5}
.info-row{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px}
@media(max-width:768px){.info-row{grid-template-columns:1fr}}
.info-card{background:var(--card);border-radius:var(--radius);padding:22px 26px;border:1px solid var(--border);font-size:13.5px;color:var(--text2);line-height:1.6;
    background-image:linear-gradient(135deg,rgba(0,85,232,.01) 0%,transparent 50%);
    transition:transform .3s var(--spring),box-shadow .3s var(--spring);
    box-shadow:0 1px 2px rgba(0,0,0,.02),0 3px 12px rgba(0,0,0,.02)}
.info-card:hover{transform:translateY(-2px) scale(1.01);box-shadow:0 6px 24px rgba(0,0,0,.04)}
.info-card strong{color:var(--text);font-weight:700;text-shadow:0 1px 1px rgba(0,0,0,.01)}

.tbl-wrap{border-radius:var(--radius);border:1px solid var(--border);overflow:hidden;background:var(--card);max-height:60vh;overflow-y:auto;
    box-shadow:0 1px 3px rgba(0,0,0,.02),0 4px 16px rgba(0,0,0,.03)}
.tbl-wrap table{width:100%;border-collapse:collapse;font-size:13px}
.tbl-wrap th{text-align:left;padding:12px 16px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--text3);background:var(--bg);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:5}
.tbl-wrap td{padding:12px 16px;border-bottom:1px solid rgba(0,0,0,.03)}
.tbl-wrap tr:last-child td{border-bottom:none}
.tbl-wrap tr:hover td{background:rgba(0,85,232,.02)}
.tbl-wrap .ep{font-weight:700;color:var(--accent)}
.pill{display:inline-block;padding:2px 10px;border-radius:20px;font-size:10px;font-weight:600;letter-spacing:.3px}
.pill.green{background:rgba(24,128,56,.08);color:var(--green)}
.pill.blue{background:rgba(0,85,232,.08);color:var(--accent)}
.pill.purple{background:rgba(122,30,184,.08);color:var(--purple)}
.cal-row.hidden{display:none}
.cal-row{cursor:pointer;transition:background .15s}

.filters{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;align-items:center}
.filters select,.filters input{padding:8px 14px;border-radius:8px;border:1px solid var(--border);background:var(--card);color:var(--text);font-size:13px;font-family:inherit;outline:none;transition:all .2s}
.filters select:hover,.filters input:hover{border-color:var(--border2)}
.filters select:focus,.filters input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(0,85,232,.06)}
.filters input{min-width:150px}
.filters .count{font-size:11px;color:var(--text3)}

.stats-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:768px){.stats-grid{grid-template-columns:1fr}}
.stat-panel{background:var(--card);border-radius:var(--radius);padding:28px;border:1px solid var(--border);
    transition:transform .3s var(--spring),box-shadow .3s var(--spring);
    box-shadow:0 1px 2px rgba(0,0,0,.02),0 4px 16px rgba(0,0,0,.03);
    background-image:radial-gradient(circle at 100% 0%,rgba(0,85,232,.01) 0%,transparent 50%)}
.stat-panel:hover{transform:translateY(-2px) scale(1.01);box-shadow:0 8px 28px rgba(0,0,0,.05)}
.stat-panel h3{font-size:16px;font-weight:800;margin-bottom:20px;text-shadow:0 1px 2px rgba(0,0,0,.02)}
.bar-row{display:flex;align-items:center;gap:10px;margin-bottom:9px}
.bar-label{font-size:11.5px;color:var(--text2);min-width:85px;text-align:right;font-weight:600}
.bar-track{flex:1;height:7px;background:rgba(0,0,0,.03);border-radius:4px;overflow:hidden;position:relative;box-shadow:inset 0 1px 3px rgba(0,0,0,.03)}
.bar-track::after{content:'';position:absolute;top:0;left:0;height:100%;width:0;
    background:linear-gradient(90deg,transparent,rgba(255,255,255,.6),transparent);
    animation:barShine 2.5s ease-in-out infinite}
@keyframes barShine{0%{width:0;left:0}50%{width:18%;left:30%}100%{width:0;left:100%}}
.bar-fill{height:100%;border-radius:4px;width:0;transition:width 1.4s var(--spring);
    background:linear-gradient(90deg,var(--accent),#7a1eb8);box-shadow:0 0 8px rgba(0,85,232,.15)}
.bar-fill.r{background:var(--red);box-shadow:0 0 8px rgba(217,45,32,.12)}
.bar-fill.b{background:var(--accent);box-shadow:0 0 8px rgba(0,85,232,.12)}
.bar-fill.pu{background:var(--purple);box-shadow:0 0 8px rgba(122,30,184,.12)}
.bar-num{font-size:11px;color:var(--text3);min-width:28px;font-weight:600;text-align:left}

.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:24px}
@media(max-width:768px){.kpi-row{grid-template-columns:repeat(2,1fr)}}
.kpi{background:var(--card);border-radius:var(--radius);padding:26px 18px;border:1px solid var(--border);text-align:center;position:relative;overflow:hidden;
    transition:transform .3s var(--spring),box-shadow .3s var(--spring);
    box-shadow:0 1px 2px rgba(0,0,0,.02),0 3px 12px rgba(0,0,0,.03)}
.kpi:hover{transform:translateY(-3px) scale(1.03);box-shadow:0 8px 28px rgba(0,0,0,.05)}
.kpi .val{font-size:44px;font-weight:900;font-family:"Segoe UI Variable Display","Segoe UI","Noto Sans SC",sans-serif;position:relative;z-index:1;
    text-shadow:0 2px 8px rgba(0,85,232,.08);font-feature-settings:"tnum"}
.kpi .lbl{font-size:11px;color:var(--text3);text-transform:uppercase;letter-spacing:.8px;margin-top:4px;font-weight:700;position:relative;z-index:1}
.kpi-ring{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:80px;height:80px;border-radius:50%;border:2px solid rgba(0,85,232,.04);pointer-events:none;transition:all .4s var(--spring)}
.kpi:hover .kpi-ring{transform:translate(-50%,-50%) scale(1.35);border-color:rgba(0,85,232,.1);border-width:3px}

.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center;z-index:1000;opacity:0;pointer-events:none;transition:opacity .3s ease;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)}
.modal-overlay.active{opacity:1;pointer-events:auto}
.modal-box{background:var(--card);border-radius:var(--radius);max-width:680px;width:92vw;max-height:82vh;overflow-y:auto;padding:40px 36px 32px;position:relative;transform:translateY(35px) scale(.93);transition:transform .4s var(--spring);box-shadow:0 20px 70px rgba(0,0,0,.15)}
.modal-overlay.active .modal-box{transform:translateY(0) scale(1)}
.modal-close{position:absolute;top:14px;right:18px;width:34px;height:34px;border-radius:50%;border:1px solid var(--border);background:var(--card);cursor:pointer;font-size:17px;display:flex;align-items:center;justify-content:center;color:var(--text3);transition:all .3s var(--spring);box-shadow:0 1px 3px rgba(0,0,0,.03)}
.modal-close:hover{background:var(--bg);color:var(--text);transform:rotate(90deg) scale(1.1)}
.modal-tag{display:inline-block;padding:3px 12px;border-radius:6px;font-size:11px;font-weight:700;background:rgba(0,85,232,.05);color:var(--accent);margin-bottom:14px;text-transform:uppercase;letter-spacing:.5px;
    box-shadow:0 1px 3px rgba(0,85,232,.03)}
.modal-box h2{font-size:26px;font-weight:800;margin-bottom:10px;line-height:1.2;text-shadow:0 2px 4px rgba(0,0,0,.03)}
.modal-difficulty{font-size:13px;color:var(--accent);font-weight:600;margin-bottom:20px}
.modal-box .ds{margin-bottom:22px}
.modal-box .ds h4{font-size:12px;text-transform:uppercase;letter-spacing:.9px;color:var(--accent);margin-bottom:8px;font-weight:700}
.modal-box .ds p,.modal-box .ds ul,.modal-box .ds ol{font-size:14px;color:var(--text2);line-height:1.75}
.modal-box .ds ul,.modal-box .ds ol{padding-left:18px}
.modal-box .ds li{margin-bottom:6px;font-size:14px;color:var(--text2);line-height:1.65}
.bgm-tip{margin-top:10px;padding:12px 16px;border-radius:10px;background:rgba(224,79,22,.04);color:var(--orange);font-size:13px;display:flex;align-items:center;gap:8px;border:1px solid rgba(224,79,22,.08)}
@media(max-width:768px){.modal-box{padding:26px 22px 22px;max-width:96vw}.modal-box h2{font-size:21px}}

@keyframes clickPulse{0%{box-shadow:0 0 0 0 rgba(0,85,232,.2)}70%{box-shadow:0 0 0 12px rgba(0,85,232,0)}100%{box-shadow:0 0 0 0 rgba(0,85,232,0)}}
.card:active,.stage-card:active{animation:clickPulse .5s ease-out}

footer{padding:32px 0;text-align:center;font-size:12.5px;color:var(--text3);position:relative;z-index:1}
footer span{color:var(--accent);font-weight:700}

::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:rgba(0,0,0,.08);border-radius:3px}
'''

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>🎬 剪辑选题系统</title>
<style>
{__CSS__}
</style>
</head>
<body>

<canvas id="particles-canvas"></canvas>
<div class="geo-shapes">
    <div class="geo circle" style="top:8%;left:5%;width:75px;height:75px"></div>
    <div class="geo triangle" style="top:28%;right:10%;border-left:32px solid transparent;border-right:32px solid transparent;border-bottom:55px solid;animation-delay:-3s"></div>
    <div class="geo square" style="top:55%;left:3%;width:40px;height:40px;animation-delay:-7s"></div>
    <div class="geo dot" style="top:70%;right:8%;width:16px;height:16px;animation-delay:-5s"></div>
    <div class="geo ring" style="top:18%;left:55%;width:60px;height:60px;animation-delay:-9s"></div>
    <div class="geo circle" style="top:82%;left:12%;width:45px;height:45px;animation-delay:-2s"></div>
    <div class="geo triangle" style="top:58%;left:62%;border-left:22px solid transparent;border-right:22px solid transparent;border-bottom:36px solid;animation-delay:-11s"></div>
    <div class="geo dot" style="top:14%;right:32%;width:10px;height:10px;animation-delay:-6s"></div>
    <div class="geo square" style="top:38%;right:6%;width:32px;height:32px;animation-delay:-4s;border-color:var(--purple)"></div>
    <div class="geo ring" style="top:75%;left:42%;width:50px;height:50px;animation-delay:-8s"></div>
</div>

<nav>
    <div class="nav-inner">
        <div class="logo"><span class="dot"></span>剪辑选题系统</div>
        <div class="tabs">
            <button class="active" data-panel="today">今日选题</button>
            <button data-panel="calendar">内容日历</button>
            <button data-panel="library">选题库</button>
            <button data-panel="stats">数据</button>
        </div>
        <div class="time">{__NOW__}</div>
    </div>
</nav>

<div class="wrap">
<main>

<section class="active" id="sec-today">
    <div class="hero">
        <div class="hero-bg"></div>
        <div class="hero-glow g1"></div><div class="hero-glow g2"></div>
        <div class="hero-toy t1"></div><div class="hero-toy t2"></div><div class="hero-toy t3"></div><div class="hero-toy t4"></div>
        <div class="label">🎬 DAILY TOPIC SYSTEM</div>
        <h1>拍摄<em>+</em>剪辑<br>选题系统</h1>
        <p class="sub">每天一个选题 · 从拍到剪全流程 · {__CAL_COUNT__} 期完整规划</p>
        <div class="hero-stats">
            <div class="hero-stat"><div class="num" style="color:var(--accent)" id="hero-total">0</div><div class="lbl">总选题</div></div>
            <div class="hero-stat"><div class="num" style="color:var(--green)" id="hero-pending">0</div><div class="lbl">待发布</div></div>
            <div class="hero-stat"><div class="num" style="color:var(--purple)" id="hero-pub">0</div><div class="lbl">已发布</div></div>
            <div class="hero-stat"><div class="num" style="color:var(--orange)" id="hero-cats">0</div><div class="lbl">大分类</div></div>
        </div>
    </div>
    <div class="divider"></div>
    <div class="sec-hd" style="margin-top:24px"><div class="kicker">Today's Picks</div><h2>🔥 今日推荐选题</h2><p class="sub">{__TODAY__} · 点击任意卡片查看完整制作指南</p></div>
    <div class="card-grid" id="today-grid"></div>
</section>

<section id="sec-calendar">
    <div class="sec-hd" style="padding-top:90px"><div class="kicker">Content Calendar</div><h2>🗓️ 200期内容日历</h2></div>
    <div class="stage-grid">
        <div class="stage-card" data-stage="冷启动期" onclick="var s=this.dataset.stage;document.querySelector('[data-panel=calendar]').click();document.getElementById('f-stage').value=s;filterCal()">
            <div class="stage-num">01</div><div class="stage-content"><h4>冷启动期<span>第 1–30 期</span></h4><p class="stage-title">剪映基础 + 拍摄入门</p><p class="stage-desc">面向零基础 · 快速上手</p></div>
        </div>
        <div class="stage-card" data-stage="增长期" onclick="var s=this.dataset.stage;document.querySelector('[data-panel=calendar]').click();document.getElementById('f-stage').value=s;filterCal()">
            <div class="stage-num">02</div><div class="stage-content"><h4>增长期<span>第 31–100 期</span></h4><p class="stage-title">转场 · 卡点 · 调色 · 蒙版</p><p class="stage-desc">系统技能进阶 · 建立专业度</p></div>
        </div>
        <div class="stage-card" data-stage="成熟期" onclick="var s=this.dataset.stage;document.querySelector('[data-panel=calendar]').click();document.getElementById('f-stage').value=s;filterCal()">
            <div class="stage-num">03</div><div class="stage-content"><h4>成熟期<span>第 101–200 期</span></h4><p class="stage-title">案例实战 + 抠像合成</p><p class="stage-desc">深度壁垒 · IP护城河</p></div>
        </div>
    </div>
    <div class="info-row">
        <div class="info-card"><strong>📐 内容节奏</strong><br>30% 爆款 · 50% 干货 · 20% 深度</div>
        <div class="info-card"><strong>⚡ 更新建议</strong><br>前期日更 · 稳定期隔日更 · 提前储备1–2周选题</div>
    </div>
    <div class="divider"></div>
    <div class="filters">
        <select id="f-stage" onchange="filterCal()"><option value="all">全部阶段</option><option value="冷启动期">冷启动期 1-30</option><option value="增长期">增长期 31-100</option><option value="成熟期">成熟期 101-200</option></select>
        <select id="f-cal-cat" onchange="filterCal()"><option value="all">全部分类</option></select>
        <input type="text" id="f-cal-search" placeholder="搜索标题…" oninput="filterCal()">
        <span class="count" id="cal-num">{__CAL_COUNT__} 期</span>
    </div>
    <div class="tbl-wrap"><table><thead><tr><th>#</th><th>标题</th><th>分类</th><th>难度</th><th>类型</th><th>时长</th><th>阶段</th></tr></thead>
    <tbody id="cal-tbody"></tbody></table></div>
</section>

<section id="sec-library">
    <div class="sec-hd" style="padding-top:90px"><div class="kicker">Full Library</div><h2>📚 全部选题</h2></div>
    <div class="filters">
        <select id="f-cat" onchange="filterLib()"><option value="all">全部分类</option></select>
        <select id="f-type" onchange="filterLib()"><option value="all">全部类型</option><option value="爆款">🔺 爆款</option><option value="干货">🔸 干货</option><option value="深度">🔹 深度</option></select>
        <select id="f-diff" onchange="filterLib()"><option value="all">全部难度</option><option value="1">⭐ 入门</option><option value="2">⭐⭐ 基础</option><option value="3">⭐⭐⭐ 进阶</option><option value="4">⭐⭐⭐⭐ 高级</option><option value="5">⭐⭐⭐⭐⭐ 专家</option></select>
        <input type="text" id="f-search" placeholder="搜索选题…" oninput="filterLib()">
        <span class="count" id="lib-num">{__TOTAL__} 条</span>
    </div>
    <div class="card-grid" id="lib-grid"></div>
</section>

<section id="sec-stats">
    <div class="sec-hd" style="padding-top:90px"><div class="kicker">Statistics</div><h2>📊 数据概览</h2></div>
    <div class="kpi-row">
        <div class="kpi"><div class="kpi-ring"></div><div class="val" style="color:var(--accent)" id="kpi-total">0</div><div class="lbl">总选题</div></div>
        <div class="kpi"><div class="kpi-ring"></div><div class="val" style="color:var(--green)" id="kpi-pending">0</div><div class="lbl">待发布</div></div>
        <div class="kpi"><div class="kpi-ring"></div><div class="val" style="color:var(--purple)" id="kpi-pub">0</div><div class="lbl">已发布</div></div>
        <div class="kpi"><div class="kpi-ring"></div><div class="val" style="color:var(--orange)" id="kpi-cal">0</div><div class="lbl">日历期数</div></div>
    </div>
    <div class="stats-grid" style="margin-top:24px">
        <div class="stat-panel"><h3>📂 分类覆盖</h3><div id="cat-bars"></div></div>
        <div class="stat-panel"><h3>📈 内容类型</h3><div id="type-bars"></div></div>
    </div>
</section>

</main>
</div>

<footer><p>数据截止 {__TODAY__} · 每日 <span>8:57</span> 自动刷新 · 数据驱动 · 点击卡片查看完整指南</p></footer>

<div class="modal-overlay" id="modal-overlay" onclick="if(event.target===this)closeModal()">
    <div class="modal-box" id="modal-box"></div>
</div>

<!-- Data blocks: safe JSON embedding -->
<script id="data-topics" type="application/json">{__TOPICS_JSON__}</script>
<script id="data-calendar" type="application/json">{__CAL_JSON__}</script>
<script id="data-picks" type="application/json">{__PICKS_JSON__}</script>
<script id="data-stats" type="application/json">{__STATS_JSON__}</script>

<script>
/* ═══════════════════ SAFE INIT ON DOM READY ═══════════════════ */
document.addEventListener('DOMContentLoaded', function() {
    try {
        /* ── Load data from safe script tags ── */
        var TOPICS = JSON.parse(document.getElementById('data-topics').textContent);
        var CALENDAR = JSON.parse(document.getElementById('data-calendar').textContent);
        var PICKS = JSON.parse(document.getElementById('data-picks').textContent);
        var STATS = JSON.parse(document.getElementById('data-stats').textContent);

        /* ── Animate numbers ── */
        setTimeout(function() {
            countUp(document.getElementById('hero-total'), STATS.total, 1600);
            countUp(document.getElementById('hero-pending'), STATS.pending, 1600);
            countUp(document.getElementById('hero-pub'), STATS.published, 1600);
            countUp(document.getElementById('hero-cats'), STATS.categories, 1600);
            countUp(document.getElementById('kpi-total'), STATS.total, 1600);
            countUp(document.getElementById('kpi-pending'), STATS.pending, 1600);
            countUp(document.getElementById('kpi-pub'), STATS.published, 1600);
            countUp(document.getElementById('kpi-cal'), STATS.calendar, 1600);
        }, 300);

        /* ── Render today picks ── */
        var todayGrid = document.getElementById('today-grid');
        var MEDALS = ['🥇','🥈','🥉','4️⃣','5️⃣'];
        for (var i = 0; i < PICKS.length; i++) {
            todayGrid.innerHTML += renderCard(PICKS[i], MEDALS[i] || '');
        }

        /* ── Render calendar ── */
        var calTbody = document.getElementById('cal-tbody');
        for (var i = 0; i < CALENDAR.length; i++) {
            calTbody.innerHTML += renderCalRow(CALENDAR[i]);
        }

        /* ── Render library ── */
        var libGrid = document.getElementById('lib-grid');
        for (var i = 0; i < TOPICS.length; i++) {
            libGrid.innerHTML += renderCard(TOPICS[i], '');
        }

        /* ── Fill category dropdowns ── */
        var cats = [];
        for (var i = 0; i < TOPICS.length; i++) {
            var c = TOPICS[i].category || '';
            if (cats.indexOf(c) < 0) cats.push(c);
        }
        cats.sort();
        var catOpts = '';
        for (var i = 0; i < cats.length; i++) {
            catOpts += '<option value="' + cats[i] + '">' + cats[i] + '</option>';
        }
        document.getElementById('f-cal-cat').innerHTML += catOpts;
        document.getElementById('f-cat').innerHTML += catOpts;

        /* ── Stats bars ── */
        var catCounts = {};
        for (var i = 0; i < TOPICS.length; i++) {
            var c = TOPICS[i].category || '';
            catCounts[c] = (catCounts[c] || 0) + 1;
        }
        var catNames = Object.keys(catCounts).sort(function(a,b){ return catCounts[b] - catCounts[a]; });
        var catBarsHtml = '';
        for (var i = 0; i < catNames.length; i++) {
            var pct = catCounts[catNames[i]] / TOPICS.length * 100;
            catBarsHtml += '<div class="bar-row"><span class="bar-label">' + catNames[i] + '</span>' +
                '<div class="bar-track"><div class="bar-fill" data-w="' + pct.toFixed(1) + '"></div></div>' +
                '<span class="bar-num">' + catCounts[catNames[i]] + '</span></div>';
        }
        document.getElementById('cat-bars').innerHTML = catBarsHtml;

        var typeCounts = {};
        for (var i = 0; i < TOPICS.length; i++) {
            var ty = TOPICS[i].content_type || '?';
            typeCounts[ty] = (typeCounts[ty] || 0) + 1;
        }
        var TE = { '爆款': '🔺', '干货': '🔸', '深度': '🔹' };
        var BC = { '爆款': 'r', '干货': 'b', '深度': 'pu' };
        var typeKeys = Object.keys(typeCounts);
        var typeBarsHtml = '';
        for (var i = 0; i < typeKeys.length; i++) {
            var ty = typeKeys[i];
            var pct = typeCounts[ty] / TOPICS.length * 100;
            var klass = BC[ty] || '';
            typeBarsHtml += '<div class="bar-row"><span class="bar-label">' + (TE[ty]||'') + ' ' + ty + '</span>' +
                '<div class="bar-track"><div class="bar-fill ' + klass + '" data-w="' + pct.toFixed(1) + '"></div></div>' +
                '<span class="bar-num">' + typeCounts[ty] + '</span></div>';
        }
        document.getElementById('type-bars').innerHTML = typeBarsHtml;

        /* ── Animate bars on scroll ── */
        var barObserver = new IntersectionObserver(function(entries) {
            for (var i = 0; i < entries.length; i++) {
                if (entries[i].isIntersecting) {
                    var bars = entries[i].target.querySelectorAll('[data-w]');
                    for (var j = 0; j < bars.length; j++) {
                        (function(b, delay) {
                            setTimeout(function() { b.style.width = b.getAttribute('data-w') + '%'; }, delay);
                        })(bars[j], j * 50);
                    }
                }
            }
        }, { threshold: 0.05 });
        var panels = document.querySelectorAll('.stat-panel');
        for (var i = 0; i < panels.length; i++) { barObserver.observe(panels[i]); }

        /* ── Also trigger on stats tab switch ── */
        var allBars = document.querySelectorAll('[data-w]');
        var barsTriggered = false;
        document.querySelectorAll('.tabs button').forEach(function(btn) {
            btn.addEventListener('click', function() {
                if (btn.dataset.panel === 'stats' && !barsTriggered) {
                    barsTriggered = true;
                    setTimeout(function() {
                        for (var i = 0; i < allBars.length; i++) {
                            (function(b, d) {
                                setTimeout(function() { b.style.width = b.getAttribute('data-w') + '%'; }, d);
                            })(allBars[i], i * 50);
                        }
                    }, 400);
                }
            });
        });

        console.log('✅ Dashboard initialized: ' + TOPICS.length + ' topics, ' + CALENDAR.length + ' calendar entries');
    } catch(e) {
        console.error('Dashboard init failed:', e);
        document.body.innerHTML += '<div style="position:fixed;top:10px;left:10px;background:red;color:#fff;padding:10px;z-index:9999;border-radius:8px;font-size:12px">Init Error: ' + e.message + '</div>';
    }
});

/* ═══════════════════ RENDER FUNCTIONS ═══════════════════ */
var DIFF_MAP = { 1: '⭐', 2: '⭐⭐', 3: '⭐⭐⭐', 4: '⭐⭐⭐⭐', 5: '⭐⭐⭐⭐⭐' };
var TYPE_EMOJI = { '爆款': '🔺', '干货': '🔸', '深度': '🔹' };
var TYPE_COLORS = { '爆款': 'red', '干货': 'blue', '深度': 'purple' };
var STAGE_COLORS = { '冷启动期': 'green', '增长期': 'blue', '成熟期': 'purple' };

function esc(s) {
    if (!s) return '';
    return ('' + s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function renderCard(t, medal) {
    var cat = esc(t.category || '');
    var ctype = esc(t.content_type || '干货');
    var diff = t.difficulty || 2;
    var title = esc(t.title || '');
    var dur = esc(t.estimated_duration || '?');
    var viral = esc(t.viral_potential || '中');
    var tc = TYPE_COLORS[t.content_type] || 'blue';
    var dc = diff <= 2 ? 'red' : (diff <= 3 ? 'blue' : 'purple');
    var m = medal ? '<span class="card-medal">' + medal + '</span>' : '';
    var delay = (Math.random() * 0.15).toFixed(3);
    var id = esc(t.id || '');
    var te = TYPE_EMOJI[t.content_type] || '';
    var dm = DIFF_MAP[diff] || '⭐⭐';

    return '<div class="card" data-id="' + id + '" data-cat="' + cat + '" data-type="' + ctype +
        '" data-diff="' + diff + '" data-title="' + title + '" style="animation-delay:' + delay + 's">' +
        '<div class="card-bar ' + dc + '"></div>' + m +
        '<span class="tag ' + tc + '">' + te + ' ' + ctype + '</span>' +
        '<h3>' + title + '</h3>' +
        '<div class="meta">' + dm + ' · ' + dur + ' · 涨粉' + viral + '</div>' +
        '</div>';
}

function renderCalRow(e) {
    var ep = e.episode || '';
    var title = esc(e.title || '');
    var cat = esc(e.category || '');
    var diff = e.difficulty || 2;
    var ctype = esc(e.content_type || '');
    var dur = esc(e.estimated_duration || '');
    var stage = esc(e.stage || '');
    var sc = STAGE_COLORS[e.stage] || 'blue';
    return '<tr class="cal-row" data-cat="' + cat + '" data-stage="' + stage +
        '" data-title="' + title + '">' +
        '<td class="ep">#' + ep + '</td><td>' + title + '</td><td>' + cat + '</td>' +
        '<td>' + (DIFF_MAP[diff] || '⭐⭐') + '</td><td>' + ctype + '</td><td>' + dur + '</td>' +
        '<td><span class="pill ' + sc + '">' + stage + '</span></td></tr>';
}

/* ═══════════════════ COUNT-UP ═══════════════════ */
function countUp(el, target, dur) {
    if (!el || !target) return;
    var start = 0;
    var startTime = null;
    function step(ts) {
        if (!startTime) startTime = ts;
        var p = Math.min((ts - startTime) / dur, 1);
        var e = 1 - Math.pow(1 - p, 4);
        el.textContent = Math.round(start + (target - start) * e);
        if (p < 1) requestAnimationFrame(step);
        else el.textContent = target;
    }
    requestAnimationFrame(step);
}

/* ═══════════════════ NAVIGATION ═══════════════════ */
document.querySelectorAll('.tabs button').forEach(function(b) {
    b.onclick = function() {
        document.querySelectorAll('.tabs button').forEach(function(x) { x.classList.remove('active'); });
        document.querySelectorAll('section').forEach(function(s) { s.classList.remove('active'); });
        b.classList.add('active');
        document.getElementById('sec-' + b.dataset.panel).classList.add('active');
    };
});

/* ═══════════════════ FILTERS ═══════════════════ */
function filterCal() {
    var stage = document.getElementById('f-stage').value;
    var cat = document.getElementById('f-cal-cat').value;
    var q = (document.getElementById('f-cal-search').value || '').toLowerCase();
    var rows = document.querySelectorAll('#cal-tbody .cal-row');
    var count = 0;
    for (var i = 0; i < rows.length; i++) {
        var r = rows[i];
        var show = true;
        if (stage !== 'all' && r.dataset.stage !== stage) show = false;
        if (cat !== 'all' && r.dataset.cat !== cat) show = false;
        if (q && r.dataset.title.toLowerCase().indexOf(q) === -1) show = false;
        if (show) { r.classList.remove('hidden'); count++; }
        else { r.classList.add('hidden'); }
    }
    document.getElementById('cal-num').textContent = count + ' 期';
}

function filterLib() {
    var cat = document.getElementById('f-cat').value;
    var type = document.getElementById('f-type').value;
    var diff = document.getElementById('f-diff').value;
    var q = (document.getElementById('f-search').value || '').toLowerCase();
    var cards = document.querySelectorAll('#lib-grid .card');
    var count = 0;
    for (var i = 0; i < cards.length; i++) {
        var c = cards[i];
        var show = true;
        if (cat !== 'all' && c.dataset.cat !== cat) show = false;
        if (type !== 'all' && c.dataset.type !== type) show = false;
        if (diff !== 'all' && c.dataset.diff !== diff) show = false;
        if (q && c.dataset.title.toLowerCase().indexOf(q) === -1) show = false;
        if (show) { c.classList.remove('hidden'); count++; }
        else { c.classList.add('hidden'); }
    }
    document.getElementById('lib-num').textContent = count + ' 条';
}

/* ═══════════════════ MODAL ═══════════════════ */
/* Use event delegation on card-grid containers */
document.addEventListener('click', function(e) {
    var card = e.target.closest('.card');
    if (card) openDetail(card);
    var calRow = e.target.closest('.cal-row');
    if (calRow) openDetailByTitle(calRow.dataset.title);
});

function openDetail(card) {
    var title = card.dataset.title;
    var t = null;

    /* Find topic by title */
    try {
        var allTopics = JSON.parse(document.getElementById('data-topics').textContent);
        for (var i = 0; i < allTopics.length; i++) {
            if (allTopics[i].title === title) { t = allTopics[i]; break; }
        }
    } catch(e) { console.error(e); }

    if (!t) return;

    var cat = esc(t.category || '');
    var ctype = t.content_type || '干货';
    var diff = t.difficulty || 2;
    var dur = esc(t.estimated_duration || '?');
    var viral = esc(t.viral_potential || '中');
    var prod = esc(t.production_time || '?');
    var desc = esc(t.description || '');
    var mats = t.materials_needed || '';
    var titleEsc = esc(t.title || '');

    var hook, stepsHtml, ending, bgm;
    var core = titleEsc.split('：')[1] || titleEsc;

    if (ctype === '爆款') {
        hook = '「' + core + '」——你是不是也刷到过这种效果？今天30秒教会你。';
        var s1 = ['📱 打开剪映，导入素材', '⚡ 关键操作：' + core + '的核心步骤', '🎯 微调参数到最佳效果', '✨ 对比展示：Before → After'];
        stepsHtml = s1.map(function(s) { return '<li>' + s + '</li>'; }).join('');
        ending = '学会了点个赞收藏，下期见！'; bgm = '节奏卡点BGM（Phut Hon / 病变 Remix）';
    } else if (ctype === '深度') {
        hook = '今天不教单个技巧，带你完整拆解「' + titleEsc + '」的全过程。';
        var s2 = ['📋 前期构思与策划思路', '🎥 拍摄现场还原与要点', '✂️ 剪辑全流程逐步拆解', '📊 成片展示 + 关键技巧复盘'];
        stepsHtml = s2.map(function(s) { return '<li>' + s + '</li>'; }).join('');
        ending = '觉得有用的话点个关注，我会持续更新这样的深度拆解。'; bgm = '叙事感配乐（Epidemic Sound 风格）';
    } else {
        hook = '为什么别人的视频那么高级？问题就出在这一步——';
        var s3 = ['🔍 常见错误：90%的人都做错了', '🛠️ 正确方法：' + titleEsc + '的核心要点', '📐 具体操作演示', '✅ 效果对比 + 避坑提醒'];
        stepsHtml = s3.map(function(s) { return '<li>' + s + '</li>'; }).join('');
        ending = '收藏起来慢慢练，关注我每天一个剪辑技巧。'; bgm = '轻量氛围BGM（Lo-Fi / Jazz Hop）';
    }

    var descBlock = desc ? '<div class="ds"><h4>💡 内容说明</h4><p>' + desc + '</p></div>' : '';

    var matTags = '';
    if (mats) {
        var parts = mats.replace(/，/g, ',').replace(/、/g, ',').split(',');
        for (var i = 0; i < parts.length; i++) {
            var m = parts[i].trim();
            if (m) matTags += '<span style="display:inline-block;padding:5px 12px;border-radius:7px;background:rgba(0,85,232,.04);color:var(--accent);font-size:12px;font-weight:600;margin:2px">' + esc(m) + '</span>';
        }
    }
    if (!matTags) matTags = '<span style="font-size:13px;color:var(--text3)">无特殊要求</span>';

    var tc = TYPE_COLORS[ctype] || 'blue';
    var te = TYPE_EMOJI[ctype] || '';
    var dm = DIFF_MAP[diff] || '⭐⭐';

    document.getElementById('modal-box').innerHTML =
        '<button class="modal-close" onclick="closeModal()">✕</button>' +
        '<div class="modal-tag">' + cat + ' · ' + ctype + '</div>' +
        '<h2>' + titleEsc + '</h2>' +
        '<div class="modal-difficulty">' + dm + ' · ' + dur + ' · 涨粉' + viral + ' · 制作' + prod + '</div>' +
        descBlock +
        '<div class="ds"><h4>✍️ 脚本文案</h4>' +
        '<p style="font-size:15px;font-weight:600;margin-bottom:10px;color:var(--text)">💬 ' + hook + '</p>' +
        '<ol style="padding-left:18px">' + stepsHtml + '</ol>' +
        '<p style="font-size:14px;color:var(--text2);margin-top:8px">' + ending + '</p>' +
        '<div class="bgm-tip">🎵 推荐BGM：' + bgm + '</div></div>' +
        '<div class="ds"><h4>📦 所需素材</h4>' + matTags + '</div>';

    document.getElementById('modal-overlay').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function openDetailByTitle(title) {
    if (!title) return;
    var cards = document.querySelectorAll('.card');
    for (var i = 0; i < cards.length; i++) {
        if (cards[i].dataset.title === title) { openDetail(cards[i]); return; }
    }
    /* Try to find by cal-row */
    var rows = document.querySelectorAll('.cal-row');
    for (var i = 0; i < rows.length; i++) {
        if (rows[i].dataset.title === title) { openDetail(rows[i]); return; }
    }
}

function closeModal() {
    document.getElementById('modal-overlay').classList.remove('active');
    document.body.style.overflow = '';
}
document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeModal(); });

/* ═══════════════════ PARTICLES ═══════════════════ */
(function(){
    var cv = document.getElementById('particles-canvas');
    if (!cv) return;
    var ctx = cv.getContext('2d'), W, H, pts = [];
    function rs() { W = cv.width = window.innerWidth; H = cv.height = document.documentElement.scrollHeight; }
    rs();
    window.addEventListener('resize', rs);
    for (var i = 0; i < 45; i++) {
        pts.push({ x: Math.random()*W, y: Math.random()*H, r: Math.random()*1.5+0.5,
            vx: (Math.random()-0.5)*0.3, vy: (Math.random()-0.5)*0.3, a: Math.random()*0.4+0.12 });
    }
    function draw() {
        ctx.clearRect(0, 0, W, H);
        for (var i = 0; i < pts.length; i++) {
            var p = pts[i]; p.x += p.vx; p.y += p.vy;
            if (p.x < 0 || p.x > W) p.vx *= -1; if (p.y < 0 || p.y > H) p.vy *= -1;
            ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
            ctx.fillStyle = 'rgba(0,85,232,' + p.a + ')'; ctx.fill();
        }
        for (var i = 0; i < pts.length; i++) {
            for (var j = i + 1; j < pts.length; j++) {
                var dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y, d = Math.sqrt(dx*dx + dy*dy);
                if (d < 110) {
                    ctx.beginPath(); ctx.moveTo(pts[i].x, pts[i].y); ctx.lineTo(pts[j].x, pts[j].y);
                    ctx.strokeStyle = 'rgba(0,85,232,' + (1-d/110)*0.04 + ')'; ctx.lineWidth = 0.5; ctx.stroke();
                }
            }
        }
        requestAnimationFrame(draw);
    }
    draw();
    var rt;
    window.addEventListener('scroll', function() {
        clearTimeout(rt);
        rt = setTimeout(function() { H = cv.height = document.documentElement.scrollHeight; }, 300);
    });
})();

/* ═══════════════════ MOUSE GLOW ═══════════════════ */
document.addEventListener('mousemove', function(e) {
    var hovered = document.querySelectorAll('.card:hover');
    for (var i = 0; i < hovered.length; i++) {
        var r = hovered[i].getBoundingClientRect();
        hovered[i].style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
        hovered[i].style.setProperty('--my', ((e.clientY - r.top) / r.height * 100) + '%');
    }
});
</script>
</body>
</html>'''


def build():
    # ── 读取数据 ──
    db = json.load(open(DB_PATH, encoding="utf-8"))
    cal = json.load(open(CAL_PATH, encoding="utf-8"))
    pub = json.load(open(PUB_PATH, encoding="utf-8"))

    topics = db["topics"]
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    pending = [t for t in topics if t["status"] == "待发布"]
    published = [t for t in topics if t["status"] == "已发布"]
    skipped = [t for t in topics if t["status"] == "已跳过"]

    # ── 今日推荐 ──
    viral_p = [t for t in pending if t.get("content_type") == "爆款"]
    dry_p   = [t for t in pending if t.get("content_type") == "干货"]
    deep_p  = [t for t in pending if t.get("content_type") == "深度"]
    picks = viral_p[:2] + dry_p[:2] + deep_p[:1]
    if len(picks) < 5:
        rest = [t for t in pending if t not in picks]
        picks += rest[:5 - len(picks)]

    # ── 分类数量 ──
    cat_set = set()
    for t in topics:
        if t.get("category"):
            cat_set.add(t["category"])

    # ── 统计数据 ──
    stats = {
        "total": len(topics),
        "pending": len(pending),
        "published": len(published),
        "skipped": len(skipped),
        "calendar": len(cal),
        "categories": len(cat_set)
    }

    # ── 构建 HTML ──
    html = HTML_TEMPLATE
    html = html.replace("{__CSS__}", CSS)
    html = html.replace("{__NOW__}", now)
    html = html.replace("{__TODAY__}", today)
    html = html.replace("{__TOTAL__}", str(len(topics)))
    html = html.replace("{__CAL_COUNT__}", str(len(cal)))
    html = html.replace("{__TOPICS_JSON__}", json.dumps(topics, ensure_ascii=False))
    html = html.replace("{__CAL_JSON__}", json.dumps(cal, ensure_ascii=False))
    html = html.replace("{__PICKS_JSON__}", json.dumps(picks, ensure_ascii=False))
    html = html.replace("{__STATS_JSON__}", json.dumps(stats, ensure_ascii=False))

    # ── 写入 ──
    for path in [HTML_PATH, INDEX_PATH]:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    size_kb = len(html.encode("utf-8")) / 1024
    print(f"✅ MG 动效仪表盘 v2 已生成")
    print(f"   📊 {HTML_PATH}")
    print(f"   🌐 {INDEX_PATH}")
    print(f"   大小：{size_kb:.1f} KB")
    print(f"   今日推荐 {len(picks)} 条 | 题库 {len(topics)} 条 | 日历 {len(cal)} 期 | {len(cat_set)} 分类")


if __name__ == "__main__":
    build()
