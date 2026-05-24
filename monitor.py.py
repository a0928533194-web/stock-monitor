import yfinance as yf
from datetime import datetime
import pytz
import time

# 完整定義成分股清單
FUNDS_CONFIG = {
    "yuanta": {
        "name": "元大店頭基金",
        "stocks": {
            "旺矽": ("6223.TWO", 9.70), "台積電": ("2330.TW", 7.88), "穎崴": ("6515.TWO", 6.12), 
            "精測": ("6510.TWO", 5.68), "信驊": ("5274.TWO", 5.63), "聯亞": ("3081.TWO", 4.56), 
            "群聯": ("8299.TWO", 3.95), "光聖": ("6442.TW", 3.75), "華星光": ("4979.TWO", 3.15), "台燿": ("6274.TWO", 3.00)
        }
    },
    "shinkin_three": {
        "name": "新光大三通基金",
        "stocks": {
            "欣興": ("3037.TW", 9.47), "景碩": ("3189.TW", 7.10), "世芯-KY": ("3661.TW", 6.93), 
            "台積電": ("2330.TW", 6.59), "旺矽": ("6223.TWO", 6.27), "大量": ("3167.TW", 6.06), 
            "台達電": ("2308.TW", 5.37), "弘塑": ("3131.TW", 4.95), "旺宏": ("2337.TW", 3.94), "力旺": ("3529.TWO", 3.92)
        }
    }
}

def get_fund_data(stocks_dict):
    total_contribution, total_pct = 0, 0
    table_rows = ""
    for name, (ticker_str, weight) in stocks_dict.items():
        time.sleep(0.6) # 減緩請求速度，防止被封鎖
        found = False
        for attempt in range(3):
            try:
                stock = yf.Ticker(ticker_str)
                hist = stock.history(period="5d")
                if len(hist) < 2: continue
                
                p_yesterday = round(hist['Close'].iloc[-2], 2)
                p_current = round(stock.fast_info.get('lastPrice', hist['Close'].iloc[-1]), 2)
                
                diff = round(p_current - p_yesterday, 2)
                contrib_pct = (diff / p_yesterday) * weight
                contribution = round(diff * (weight / 100), 4)
                
                total_pct += contrib_pct
                total_contribution += contribution
                
                color = "up" if diff > 0 else "down" if diff < 0 else ""
                table_rows += f"<tr><td>{name}</td><td class='weight'>{weight}%</td><td>{p_yesterday}</td><td class='{color}'>{p_current}</td><td class='{color}'>{contrib_pct:+.2f}%</td><td class='{color}'>{contribution:+.4f}</td></tr>"
                found = True
                break
            except:
                time.sleep(1)
        if not found:
            print(f"【警告】無法抓取 {name} ({ticker_str})")
    return round(total_contribution, 4), round(total_pct, 2), table_rows

def run_monitor():
    now_tw = datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')
    options_html = ""
    sections_html = ""
    
    for i, (key, info) in enumerate(FUNDS_CONFIG.items()):
        total_sum, total_pct, table_rows = get_fund_data(info["stocks"])
        active_class = "active" if i == 0 else ""
        options_html += f'<option value="{key}">{info["name"]}</option>'
        sections_html += f'''
        <div id="sector-{key}" class="fund-section {active_class}">
            <div class="dashboard">
                <div class="dashboard-row"><div class="dashboard-title">{info["name"]} - 今日預估總貢獻</div><div class="total-sum">{total_sum:+.4f}</div></div>
                <div class="dashboard-row"><div class="dashboard-title">今日預估總貢獻 %</div><div class="total-percent">{total_pct:+.2f}%</div></div>
            </div>
            <div class="table-container"><table><thead><tr><th>成分股</th><th>權重</th><th>昨收</th><th>現價</th><th>貢獻%</th><th>貢獻度</th></tr></thead><tbody>{table_rows}</tbody></table></div>
        </div>'''

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW"><head><meta charset="UTF-8"><title>旗艦基金即時監測系統</title>
<style>
    :root {{ --up: #ff4d4f; --down: #52c41a; }}
    body {{ font-family: sans-serif; background: #f8f9fa; padding: 15px; display: flex; flex-direction: column; align-items: center; }}
    .container {{ width: 100%; max-width: 500px; background: white; padding: 20px; border-radius: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
    .fund-select {{ width: 100%; padding: 12px; margin-bottom: 20px; border-radius: 8px; border: 1px solid #ccc; font-size: 16px; font-weight: bold; }}
    .fund-section {{ display: none; }} .fund-section.active {{ display: block; }}
    .dashboard {{ text-align: center; margin-bottom: 20px; }}
    .total-sum {{ font-size: 28px; font-weight: bold; color: #333; }}
    .total-percent {{ font-size: 20px; font-weight: bold; color: #555; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ padding: 8px; text-align: right; border-bottom: 1px solid #eee; }}
    .up {{ color: var(--up); font-weight: bold; }} .down {{ color: var(--down); font-weight: bold; }}
</style></head>
<body>
<div class="container">
    <div style="text-align:center; margin-bottom:10px;">🕒 更新：{now_tw}</div>
    <select class="fund-select" onchange="document.querySelectorAll('.fund-section').forEach(s=>s.classList.remove('active')); document.getElementById('sector-'+this.value).classList.add('active')">
        {options_html}
    </select>
    {sections_html}
</div>
</body></html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("【更新成功】index.html 已生成")

if __name__ == "__main__":
    run_monitor()
