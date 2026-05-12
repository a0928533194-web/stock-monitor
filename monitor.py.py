import yfinance as yf
from datetime import datetime
import os
import re
import pytz

# 元大店頭
yuanta_stocks = {
    "旺矽": ("6223.TWO", 9.70), "台積電": ("2330.TW", 7.88), "穎崴": ("6515.TWO", 6.12),
    "精測": ("6510.TWO", 5.68), "信驊": ("5274.TWO", 5.63), "聯亞": ("3081.TWO", 4.56),
    "群聯": ("8299.TWO", 3.95), "光聖": ("6442.TW", 3.75), "華星光": ("4979.TWO", 3.15),
    "台燿": ("6274.TWO", 3.00), "力旺": ("3529.TWO", 2.94), "沛亨": ("6291.TWO", 2.94),
    "聖暉*": ("5536.TWO", 2.63), "波若威": ("3163.TWO", 2.59), "京元電子": ("2449.TW", 2.58),
    "中光電": ("5371.TWO", 2.50), "邑錡": ("7402.TWO", 2.45), "日月光投控": ("3711.TW", 2.40),
    "環球晶": ("6488.TWO", 2.21), "新應材": ("4749.TWO", 2.10), "鴻勁": ("7769.TW", 1.85),
    "世禾": ("3551.TWO", 1.79), "台特化": ("4772.TWO", 1.45), "旺宏": ("2337.TW", 1.35),
    "聯鈞": ("3450.TW", 1.07), "大江": ("8436.TWO", 1.01)
}

# 瀚亞科技 (根據 image_9c7a06.png)
eastspring_stocks = {
    "奇鋐": ("3017.TW", 8.25), "欣興": ("3037.TW", 8.07), "台積電": ("2330.TW", 7.90),
    "台光電": ("2383.TW", 6.74), "台達電": ("2308.TW", 6.47), "智邦": ("2345.TW", 6.00),
    "台燿": ("6274.TWO", 5.55), "光寶科": ("2301.TW", 5.20), "光聖": ("6442.TW", 5.17),
    "聯亞": ("3081.TWO", 5.03), "強茂": ("2481.TW", 4.51), "聯發科": ("2454.TW", 4.01),
    "華碩": ("2357.TW", 3.68), "健策": ("3653.TW", 3.38), "振樺電": ("8114.TW", 2.73),
    "旺矽": ("6223.TWO", 2.20), "致茂": ("2360.TW", 2.17), "川湖": ("2059.TW", 1.99),
    "緯創": ("3231.TW", 1.92), "南電": ("8046.TW", 1.80), "華星光": ("4979.TWO", 1.40),
    "精測": ("6510.TWO", 1.23)
}

def get_fund_data(stocks_dict):
    total_contribution = 0
    table_rows = ""
    for name, (sid, weight) in stocks_dict.items():
        try:
            stock = yf.Ticker(sid)
            hist = stock.history(period="2d")
            if len(hist) < 2: continue
            p_yesterday = round(hist['Close'].iloc[-2], 2)
            p_current = round(stock.fast_info['lastPrice'], 2)
            diff = round(p_current - p_yesterday, 2)
            contribution = round(diff * (weight / 100), 4)
            total_contribution += contribution
            color_class = "up" if diff > 0 else "down" if diff < 0 else ""
            table_rows += f"<tr><td>{name}</td><td style='color:#666'>{weight}%</td><td>{p_yesterday}</td><td class='{color_class}'>{p_current}</td><td class='{color_class}'>{contribution:+.4f}</td></tr>"
        except: pass
    return round(total_contribution, 4), table_rows

def run_monitor():
    tw_tz = pytz.timezone('Asia/Taipei')
    now_tw = datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S')
    y_res, y_rows = get_fund_data(yuanta_stocks)
    e_res, e_rows = get_fund_data(eastspring_stocks)

    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'<span id="update-time">.*?</span>', f'<span id="update-time">{now_tw}</span>', content)
        # 更新元大店頭
        content = re.sub(r'<div id="yuanta-sum">.*?</div>', f'<div id="yuanta-sum">{y_res:+.4f}</div>', content)
        content = re.sub(r'<tbody id="yuanta-details">.*?</tbody>', f'<tbody id="yuanta-details">{y_rows}</tbody>', content, flags=re.DOTALL)
        # 更新瀚亞科技
        content = re.sub(r'<div id="east-sum">.*?</div>', f'<div id="east-sum">{e_res:+.4f}</div>', content)
        content = re.sub(r'<tbody id="east-details">.*?</tbody>', f'<tbody id="east-details">{e_rows}</tbody>', content, flags=re.DOTALL)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    run_monitor()
