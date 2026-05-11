import yfinance as yf
from datetime import datetime
import os
import re
import pytz  # 處理時區的核心套件

# 完全依照您的投資明細 (共 26 檔)
stocks_data = {
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

def run_monitor():
    # 取得台灣時間
    tw_tz = pytz.timezone('Asia/Taipei')
    now_tw = datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    total_contribution = 0
    table_rows = "" 
    print(f"\n🚀 執行數據更新: {now_tw}")

    for name, (sid, weight) in stocks_data.items():
        try:
            stock = yf.Ticker(sid)
            hist = stock.history(period="7d")
            hist = hist[hist['Close'].notna()]
            if len(hist) >= 2:
                p_n1 = round(hist['Close'].iloc[-2], 2) # 昨日收盤
                p_n_raw = stock.fast_info['lastPrice']
                p_n = round(p_n_raw if p_n_raw and p_n_raw != 0 else hist['Close'].iloc[-1], 2)
                
                diff = round(p_n - p_n1, 2)
                contribution = round(diff * (weight / 100), 4)
                total_contribution += contribution
                
                color_class = "up" if diff > 0 else "down" if diff < 0 else ""
                table_rows += f"""
                <tr>
                    <td>{name}</td>
                    <td style="color:#666">{weight}%</td>
                    <td>{p_n1}</td>
                    <td class="{color_class}">{p_n}</td>
                    <td class="{color_class}">{contribution:+.4f}</td>
                </tr>
                """
        except Exception as e:
            print(f"❌ 錯誤: {name} - {e}")

    final_res = round(total_contribution, 4)
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 更新總分、更新表格
        content = re.sub(r'<div id="total-sum">.*?</div>', f'<div id="total-sum">{final_res:+.4f}</div>', content)
        content = re.sub(r'<tbody id="stock-details">.*?</tbody>', f'<tbody id="stock-details">{table_rows}</tbody>', content, flags=re.DOTALL)
        
        # 更新 HTML 畫面上的時間 (確保 index.html 裡有 id="update-time")
        content = re.sub(r'<span id="update-time">.*?</span>', f'<span id="update-time">{now_tw}</span>', content)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
    print(f"✅ 更新完成，時間：{now_tw}")

if __name__ == "__main__":
    run_monitor()
