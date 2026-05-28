import yfinance as yf
from datetime import datetime
import pytz
import time

# 數據設定
FUNDS_CONFIG = {
    "yuanta_otc": {"name": "元大店頭基金", "stocks": {"旺矽": ("6223", 8.71), "信驊": ("5274", 6.66), "台積電": ("2330", 6.47), "穎崴": ("6515", 5.77), "精測": ("6510", 5.74), "聯亞": ("3081", 4.80), "華星光": ("4979", 4.31), "台燿": ("6274", 4.08), "群聯": ("8299", 3.84), "力旺": ("3529", 3.35)}},
    "shinkin_three": {"name": "新光大三通基金", "stocks": {"欣興": ("3037", 9.47), "景碩": ("3189", 7.10), "世芯-KY": ("3661", 6.93), "台積電": ("2330", 6.59), "旺矽": ("6223", 6.27), "大量": ("3167", 6.06), "台達電": ("2308", 5.37), "弘塑": ("3131", 4.95), "旺宏": ("2337", 3.94), "力旺": ("3529", 3.92)}},
    "allianz_taiwan": {"name": "安聯台灣大壩", "stocks": {"旺矽": ("6223", 11.30), "穎崴": ("6515", 10.49), "台積電": ("2330", 6.87), "台光電": ("2383", 6.44), "欣興": ("3037", 5.65), "信驊": ("5274", 5.45), "台達電": ("2308", 5.05), "台燿": ("6274", 4.97), "奇鋐": ("3017", 3.76), "智邦": ("2345", 3.34)}},
    "allianz_tech": {"name": "安聯台灣科技", "stocks": {"旺矽": ("6223", 8.54), "穎崴": ("6515", 8.38), "台積電": ("2330", 6.59), "台光電": ("2383", 6.58), "創意": ("3443", 5.34), "台燿": ("6274", 4.73), "台達電": ("2308", 4.49), "信驊": ("5274", 4.09), "金像電": ("2368", 4.07), "威剛": ("3260", 3.78)}},
    "allianz_smart": {"name": "安聯台灣智慧", "stocks": {"信驊": ("5274", 7.77), "穎崴": ("6515", 7.57), "旺矽": ("6223", 7.25), "台光電": ("2383", 6.35), "創意": ("3443", 6.11), "台積電": ("2330", 5.56), "致茂": ("2360", 4.99), "智邦": ("2345", 4.39), "台達電": ("2308", 4.36), "台燿": ("6274", 4.13)}},
    "fubon_choice": {"name": "富邦首選", "stocks": {"欣興": ("3037", 9.89), "旺矽": ("6223", 8.34), "金像電": ("2368", 7.24), "台達電": ("2308", 6.49), "群聯": ("8299", 5.94), "光聖": ("6442", 5.50), "貿聯-KY": ("3665", 5.48), "台積電": ("2330", 5.28), "華星光": ("4979", 4.76), "南電": ("8046", 4.58)}},
    "fubon_select": {"name": "富邦上選", "stocks": {"欣興": ("3037", 7.48), "穎崴": ("6515", 6.46), "南電": ("8046", 6.11), "聯亞": ("3081", 5.55), "台光電": ("2383", 5.48), "金像電": ("2368", 5.39), "奇鋐": ("3017", 4.90), "光聖": ("6442", 4.83), "台積電": ("2330", 4.72), "竹陞科技": ("6739", 3.62)}},
    "fubon_taiwan": {"name": "富邦新台商", "stocks": {"聯亞": ("3081", 5.55), "台達電": ("2308", 5.20), "台光電": ("2383", 5.07), "旺矽": ("6223", 4.97), "台積電": ("2330", 4.74), "致茂": ("2360", 4.71), "健策": ("3653", 4.34), "奇鋐": ("3017", 4.25), "南電": ("8046", 4.09), "大量": ("3167", 4.07)}},
    "nomura_prime": {"name": "野村優質", "stocks": {"健策": ("3653", 8.72), "台光電": ("2383", 8.62), "台達電": ("2308", 8.44), "台積電": ("2330", 8.03), "穎崴": ("6515", 7.42), "川湖": ("2059", 7.10), "鴻勤": ("8114", 6.70), "金像電": ("2368", 5.90), "欣興": ("3037", 5.22), "力旺": ("3529", 4.64)}},
    "hanya_tech": {"name": "瀚亞科技", "stocks": {"欣興": ("3037", 8.95), "台光電": ("2383", 8.18), "奇鋐": ("3017", 8.16), "台積電": ("2330", 7.64), "台達電": ("2308", 7.05), "台燿": ("6274", 6.84), "智邦": ("2345", 6.29), "聯亞": ("3081", 5.85), "聯發科": ("2454", 4.88), "光寶科": ("2301", 4.26)}},
    "uni_allweather": {"name": "統一全天候", "stocks": {"台光電": ("2383", 9.85), "台達電": ("2308", 8.68), "欣興": ("3037", 8.50), "奇鋐": ("3017", 7.88), "台積電": ("2330", 7.08), "貿聯-KY": ("3665", 6.23), "穎崴": ("6515", 5.44), "健策": ("3653", 4.51), "南電": ("8046", 3.75), "致茂": ("2360", 3.74)}},
    "uni_prosper": {"name": "統一奔騰", "stocks": {"台光電": ("2383", 10.16), "奇鋐": ("3017", 9.21), "健策": ("3653", 7.79), "旺矽": ("6223", 7.55), "貿聯-KY": ("3665", 7.31), "台達電": ("2308", 7.28), "南電": ("8046", 7.19), "智邦": ("2345", 7.07), "台積電": ("2330", 6.40), "金像電": ("2368", 6.05)}},
    "uni_darkhorse": {"name": "統一黑馬基金", "stocks": {"台光電": ("2383", 7.34), "台積電": ("2330", 6.94), "欣興": ("3037", 6.78), "奇鋐": ("3017", 6.65), "南電": ("8046", 6.39), "台達電": ("2308", 5.90), "金像電": ("2368", 5.27), "健策": ("3653", 4.64), "貿聯-KY": ("3665", 4.08), "穎崴": ("6515", 3.36)}},
    "nomura_fortune": {"name": "野村鴻運基金", "stocks": {"欣興": ("3037", 7.56), "奇鋐": ("3017", 6.38), "健策": ("3653", 5.97), "台達電": ("2308", 5.90), "台光電": ("2383", 5.78), "台積電": ("2330", 5.57), "旺矽": ("6223", 4.60), "穎崴": ("6515", 4.34), "貿聯-KY": ("3665", 3.70), "金像電": ("2368", 3.69)}},
    "nomura_growth": {"name": "野村成長基金", "stocks": {"台光電": ("2383", 7.24), "欣興": ("3037", 7.22), "穎崴": ("6515", 6.34), "台達電": ("2308", 5.68), "金像電": ("2368", 5.53), "台積電": ("2330", 5.40), "南電": ("8046", 5.30), "奇鋐": ("3017", 5.21), "健策": ("3653", 5.08), "旺矽": ("6223", 4.70)}},
    "nomura_hightech": {"name": "野村高科技基金", "stocks": {"南電": ("8046", 9.18), "欣興": ("3037", 8.94), "聯亞": ("3081", 7.45), "台積電": ("2330", 6.36), "奇鋐": ("3017", 6.05), "華星光": ("4979", 5.10), "聯發科": ("2454", 3.96), "景碩": ("3189", 3.79), "臻鼎-KY": ("4958", 3.65), "致茂": ("2360", 3.59)}},
    "nomura_etech": {"name": "野村 e 科技基金", "stocks": {"南電": ("8046", 8.85), "欣興": ("3037", 8.79), "聯亞": ("3081", 6.67), "台積電": ("2330", 6.57), "奇鋐": ("3017", 5.97), "華星光": ("4979", 4.84), "景碩": ("3189", 4.00), "聯發科": ("2454", 3.91), "竑騰": ("3052", 3.82), "光聖": ("6442", 3.63)}}
}

def get_fund_data(stocks_dict):
    total_contribution, total_pct = 0, 0
    table_rows = ""
    for name, (ticker_base, weight) in stocks_dict.items():
        time.sleep(0.3)
        success = False
        p_yesterday, p_current, diff = 0.0, 0.0, 0.0
        for suffix in ["", ".TW", ".TWO"]:
            try:
                stock = yf.Ticker(f"{ticker_base}{suffix}")
                hist = stock.history(period="5d")
                if len(hist) >= 2:
                    p_yesterday = round(hist['Close'].iloc[-2], 2)
                    p_current = round(stock.fast_info.get('lastPrice', hist['Close'].iloc[-1]), 2)
                    diff = round(p_current - p_yesterday, 2)
                    success = True
                    break
            except: continue
        
        stock_change_pct = (diff / p_yesterday * 100) if p_yesterday != 0 else 0
        contrib_pct = stock_change_pct * (weight / 100)
        contribution = diff * (weight / 100)
        total_pct += contrib_pct
        total_contribution += contribution
        color = "up" if diff > 0 else "down" if diff < 0 else ""
        table_rows += f"<tr><td>{name}</td><td class='weight'>{weight}%</td><td>{p_yesterday if success else 'N/A'}</td><td class='{color}'>{p_current if success else 'N/A'}</td><td class='{color}'>{contrib_pct:+.2f}%</td><td class='{color}'>{contribution:+.4f}</td></tr>"
    return round(total_contribution, 4), round(total_pct, 2), table_rows

def run_monitor():
    now_tw = datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')
    options_html, sections_html = "", ""
    for i, (key, info) in enumerate(FUNDS_CONFIG.items()):
        total_sum, total_pct, table_rows = get_fund_data(info["stocks"])
        active = "active" if i == 0 else ""
        options_html += f'<option value="{key}">{info["name"]}</option>'
        sections_html += f'''
        <div id="sector-{key}" class="fund-section {active}">
            <div class="dashboard">
                <div class="dashboard-title">{info["name"]} - 今日預估總貢獻</div>
                <div class="total-sum">{total_sum:+.4f}</div>
                <div class="dashboard-title">今日預估總貢獻 %</div>
                <div class="total-percent">{total_pct:+.2f}%</div>
            </div>
            <table><thead><tr><th>成分股</th><th>權重</th><th>昨收</th><th>現價</th><th>貢獻%</th><th>貢獻度</th></tr></thead><tbody>{table_rows}</tbody></table>
        </div>'''

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>基金監測系統</title>
<style>
    :root {{ --up: #ff4d4f; --down: #52c41a; }}
    body {{ font-family: sans-serif; background: #f0f2f5; padding: 10px; margin: 0; }}
    .container {{ max-width: 500px; margin: auto; background: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
    .fund-section {{ display: none; }} .fund-section.active {{ display: block; }}
    .dashboard {{ text-align: center; background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 15px 0; }}
    .total-sum {{ font-size: 24px; font-weight: bold; color: #333; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th {{ color: #888; font-weight: normal; padding: 8px 4px; border-bottom: 1px solid #eee; }}
    td {{ padding: 10px 4px; text-align: right; border-bottom: 1px solid #f9f9f9; }}
    .up {{ color: var(--up); font-weight: bold; }} .down {{ color: var(--down); font-weight: bold; }}
    select {{ width: 100%; padding: 12px; font-size: 16px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px; }}
    .update-box {{ text-align:center; margin: 20px 0; padding: 15px; border-top: 1px solid #eee; }}
</style></head>
<body>
<div class="container">
    <div style="text-align:center; font-size: 12px; color: #666; margin-bottom: 10px;">🕒 更新：{now_tw}</div>
    <select onchange="document.querySelectorAll('.fund-section').forEach(s=>s.classList.remove('active')); document.getElementById('sector-'+this.value).classList.add('active')">{options_html}</select>
    {sections_html}
    <div class="update-box">
        <button id="updateBtn" onclick="triggerUpdate()" style="background-color: #1890ff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">更新基金數據</button>
        <p id="status" style="font-size: 12px; color: #666; margin-top: 10px;"></p>
    </div>
</div>
<script>
async function triggerUpdate() {{
    const GITHUB_OWNER = "a0928533194-web"; 
    const REPO_NAME = "stock-monitor";
    const WORKFLOW_FILE = "run.yml"; 
    const userToken = prompt("請輸入您的 GitHub Token:");
    if (!userToken) return;
    document.getElementById('status').innerText = "正在發送請求...";
    const response = await fetch(`https://api.github.com/repos/${{GITHUB_OWNER}}/${{REPO_NAME}}/actions/workflows/${{WORKFLOW_FILE}}/dispatches`, {{
        method: "POST",
        headers: {{"Authorization": "token " + userToken, "Accept": "application/vnd.github.v3+json"}},
        body: JSON.stringify({{"ref": "main"}})
    }});
    if (response.ok) {{ document.getElementById('status').innerText = "✅ 請求已送出！"; }}
    else {{ document.getElementById('status').innerText = "❌ 請求失敗"; }}
}}
</script>
</body></html>"""

    with open("index.html", "w", encoding="utf-8") as f: f.write(html_content)
    print("【更新成功】index.html 已生成")

if __name__ == "__main__":
    run_monitor()
