import yfinance as yf
from datetime import datetime
import os
import pytz

# 設定僅需監測的標的
FUND_KEY = "yuanta"
FUND_NAME = "元大店頭基金"

# 數據設定
stocks_config = {
    "旺矽": ("6223.TWO", 9.70), "台積電": ("2330.TW", 7.88), "穎崴": ("6515.TWO", 6.12), 
    "精測": ("6510.TWO", 5.68), "信驊": ("5274.TWO", 5.63), "聯亞": ("3081.TWO", 4.56), 
    "群聯": ("8299.TWO", 3.95), "光聖": ("6442.TW", 3.75), "華星光": ("4979.TWO", 3.15), 
    "台燿": ("6274.TWO", 3.00)
}

def get_fund_data(stocks_dict):
    total_contribution = 0
    total_pct = 0
    table_rows = ""
    for name, data in stocks_dict.items():
        try:
            ticker_str, weight = data
            stock = yf.Ticker(ticker_str)
            hist = stock.history(period="2d")
            if len(hist) < 2: continue
            p_yesterday = round(hist['Close'].iloc[-2], 2)
            p_current = round(stock.fast_info['lastPrice'], 2)
            diff = round(p_current - p_yesterday, 2)
            
            contrib_percent = (diff / p_yesterday) * weight
            total_pct += contrib_percent
            contribution = round(diff * (weight / 100), 4)
            total_contribution += contribution
            
            color_class = "up" if diff > 0 else "down" if diff < 0 else ""
            table_rows += f"""<tr>
                <td>{name}</td>
                <td class='weight'>{weight}%</td>
                <td>{p_yesterday}</td>
                <td class='{color_class}'>{p_current}</td>
                <td class='{color_class}'>{contrib_percent:+.2f}%</td>
                <td class='{color_class}'>{contribution:+.4f}</td>
            </tr>"""
        except:
            pass
    return round(total_contribution, 4), round(total_pct, 2), table_rows

def run_monitor():
    tw_tz = pytz.timezone('Asia/Taipei')
    now_tw = datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    total_sum, total_pct, table_rows = get_fund_data(stocks_config)
    
    # 產生簡潔的 HTML 內容
    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>旗艦基金即時監測系統</title>
    <style>
        :root {{ --primary: #007bff; --bg: #f8f9fa; --card-bg: #ffffff; --text: #333333; --up-color: #ff4d4f; --down-color: #52c41a; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: var(--bg); color: var(--text); margin: 0; padding: 15px; display: flex; flex-direction: column; align-items: center; }}
        .container {{ width: 100%; max-width: 500px; background: var(--card-bg); padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); box-sizing: border-box; }}
        .header {{ text-align: center; font-size: 14px; color: #666; margin-bottom: 15px; }}
        .btn-update {{ display: block; width: 60%; margin: 0 auto 20px auto; background: var(--primary); color: white; border: none; padding: 10px; border-radius: 20px; font-weight: bold; cursor: pointer; text-align: center; text-decoration: none; font-size: 14px; }}
        .dashboard {{ background: var(--bg); border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 20px; }}
        .dashboard-row {{ margin-bottom: 10px; }}
        .dashboard-title {{ font-size: 14px; color: #666; margin-bottom: 2px; }}
        .total-sum {{ font-size: 30px; font-weight: 800; color: #333; }}
        .total-percent {{ font-size: 22px; font-weight: 700; color: #555; }}
        .table-container {{ overflow-x: auto; width: 100%; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        th, td {{ padding: 10px 6px; text-align: right; border-bottom: 1px solid #f0f0f0; }}
        th:first-child, td:first-child {{ text-align: left; }}
        th {{ color: #999; font-weight: 500; }}
        .weight {{ color: #666; font-weight: bold; }}
        .up {{ color: var(--up-color); font-weight: bold; }}
        .down {{ color: var(--down-color); font-weight: bold; }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">🕒 最後更新：<span id="update-time">{now_tw}</span></div>
    <a href="https://github.com/a0928533194-web/github.io/actions/workflows/dynamic.yml/trigger" class="btn-update" target="_blank">🚀 手動更新數據</a>
    <div class="dashboard">
        <div class="dashboard-row"><div class="dashboard-title">{FUND_NAME} - 今日預估總貢獻</div><div class="total-sum">{total_sum:+.4f}</div></div>
        <div class="dashboard-row"><div class="dashboard-title">今日預估總貢獻 %</div><div class="total-percent">{total_pct:+.2f}%</div></div>
    </div>
    <div class="table-container">
        <table>
            <thead><tr><th>成分股</th><th>權重</th><th>昨收</th><th>現價</th><th>貢獻%</th><th>貢獻度</th></tr></thead>
            <tbody>{table_rows}</tbody>
        </table>
    </div>
</div>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"【更新完成】{FUND_NAME} 數據已寫入 index.html")

if __name__ == "__main__":
    run_monitor()
