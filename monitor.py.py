import yfinance as yf
from datetime import datetime
import time
import os
import re

# 你的 26 檔成分股與比例
stocks_data = {
    "旺矽": ("6223.TW", 9.70), "台積電": ("2330.TW", 7.88), "穎崴": ("6515.TW", 6.12),
    "精測": ("6510.TW", 5.68), "信驊": ("5274.TW", 5.63), "聯亞": ("3081.TWO", 4.56),
    "群聯": ("8299.TWO", 3.95), "光聖": ("6442.TW", 3.75), "華星光": ("4979.TWO", 3.15),
    "台燿": ("6274.TWO", 3.00), "沛亨": ("6291.TWO", 2.94), "力旺": ("3529.TWO", 2.94),
    "聖暉*": ("5536.TWO", 2.63), "波若威": ("3163.TWO", 2.59), "京元電子": ("2449.TW", 2.58),
    "中光電": ("5371.TWO", 2.50), "邑錡": ("7402.TWO", 2.45), "日月光投控": ("3711.TW", 2.40),
    "環球晶": ("6488.TWO", 2.21), "新應材": ("4749.TWO", 2.10), "鴻勁": ("7769.TW", 1.85),
    "世禾": ("3551.TWO", 1.79), "台特化": ("4772.TWO", 1.45), "旺宏": ("2337.TW", 1.35),
    "聯鈞": ("3450.TW", 1.07), "大江": ("8436.TWO", 1.01)
}

def run_monitor():
    total_contribution = 0
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for name, (sid, weight) in stocks_data.items():
        try:
            stock = yf.Ticker(sid)
            hist = stock.history(period="5d")
            hist = hist[hist['Close'].notna()]
            if len(hist) >= 1:
                p_n1 = hist['Close'].iloc[-1]
                p_n = stock.fast_info['lastPrice'] or p_n1
                total_contribution += (p_n - p_n1) * (weight / 100)
            time.sleep(0.1)
        except: pass

    final_res = round(total_contribution, 4)
    print(f"計算完成: {final_res}")

    # --- 自動尋找並更新 index.html ---
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 替換數字
        content = re.sub(r'<div id="total-sum">.*?</div>', f'<div id="total-sum">{final_res}</div>', content)
        # 替換更新時間
        content = re.sub(r'<div class="update-time" id="last-update">.*?</div>', f'<div class="update-time" id="last-update">更新時間：{now_str} (TW)</div>', content)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("網頁檔案已在地端完成更新")

if __name__ == "__main__":
    run_monitor()
