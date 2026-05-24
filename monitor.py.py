import yfinance as yf
from datetime import datetime
import pytz
import time

# 數據設定：代號為純數字字串
FUNDS_CONFIG = {
    "yuanta": {
        "name": "元大店頭基金",
        "stocks": {
            "旺矽": ("6223", 9.70), "台積電": ("2330", 7.88), "穎崴": ("6515", 6.12), 
            "精測": ("6510", 5.68), "信驊": ("5274", 5.63), "聯亞": ("3081", 4.56), 
            "群聯": ("8299", 3.95), "光聖": ("6442", 3.75), "華星光": ("4979", 3.15), "台燿": ("6274", 3.00)
        }
    },
    "shinkin_three": {
        "name": "新光大三通基金",
        "stocks": {
            "欣興": ("3037", 9.47), "景碩": ("3189", 7.10), "世芯-KY": ("3661", 6.93), 
            "台積電": ("2330", 6.59), "旺矽": ("6223", 6.27), "大量": ("3167", 6.06), 
            "台達電": ("2308", 5.37), "弘塑": ("3131", 4.95), "旺宏": ("2337", 3.94), "力旺": ("3529", 3.92)
        }
    }
}

def get_fund_data(stocks_dict):
    total_contribution, total_pct = 0, 0
    table_rows = ""
    for name, (ticker_base, weight) in stocks_dict.items():
        time.sleep(0.4)
        success = False
        p_yesterday, p_current, diff = 0.0, 0.0, 0.0
        
        # 嘗試抓取
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
        
        # --- 修正後的科學計算公式 ---
        # 個股單日漲跌幅 %
        stock_change_pct = (diff / p_yesterday * 100) if p_yesterday != 0 else 0
        # 加權貢獻 % = 個股漲跌幅 * 權重比例
        contrib_pct = stock_change_pct * (weight / 100)
        # 貢獻度點數 = 價格差 * 權重比例
        contribution = diff * (weight / 100)
        
        total_pct += contrib_pct
        total_contribution += contribution
        
        color = "up" if diff > 0 else "down" if diff < 0 else ""
        table_rows += f"""<tr>
            <td>{name}</td>
            <td class='weight'>{weight}%</td>
            <td>{p_yesterday if success else 'N/A'}</td>
            <td class='{color}'>{p_current if success else 'N/A'}</td>
            <td class='{color}'>{contrib_pct:+.2f}%</td>
            <td class='{color}'>{contribution:+.4f}</td>
        </tr>"""

    return round(total_contribution, 4), round(total_pct, 2), table_rows

def run_monitor():
    now_tw = datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')
    options_html = ""
    sections_html = ""
    
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
<html lang="zh-TW"><head><meta charset="UTF-8"><title>基金監測系統</title>
<style>
    :root {{ --up: #ff4d4f; --down: #52c41a; }}
    body {{ font-family: sans-serif; background: #f8f9fa; padding: 20px; }}
    .container {{ max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
    .fund-section {{ display: none; }} .fund-section.active {{ display: block; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
    th, td {{ padding: 8px; text-align: right; border-bottom: 1px solid #eee; }}
    .up {{ color: var(--up); font-weight: bold; }} .down {{ color: var(--down); font-weight: bold; }}
</style></head>
<body>
<div class="container">
    <div style="text-align:center; margin-bottom:15px;">🕒 更新：{now_tw}</div>
    <select class="fund-select" onchange="document.querySelectorAll('.fund-section').forEach(s=>s.classList.remove('active')); document.getElementById('sector-'+this.value).classList.add('active')" style="width:100%; padding:10px;">
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
