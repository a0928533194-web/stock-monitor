import yfinance as yf
from datetime import datetime
import time
import os
import re

# 完全依照 2026/03/31 投資明細截圖，補足所有漏掉的股票 (共 26 檔)
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
    total_contribution = 0
    table_rows = "" 
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"\n🚀 啟動完整監測 (26 檔) - {now_str}")
    print("-" * 80)

    for name, (sid, weight) in stocks_data.items():
        try:
            stock = yf.Ticker(sid)
            # 抓取較長天數以確保跨週末數據正確
            hist = stock.history(period="7d")
            hist = hist[hist['Close'].notna()]
            
            if len(hist) >= 2:
                # 確保昨日價格 (N-1) 為前一交易日收盤價
                p_n1 = round(hist['Close'].iloc[-2], 2)
                # 取得最新現價 (N)
                p_n_raw = stock.fast_info['lastPrice']
                p_n = round(p_n_raw if p_n_raw and p_n_raw != 0 else hist['Close'].iloc[-1], 2)
                
                diff = round(p_n - p_n1, 2)
                contribution = round(diff * (weight / 100), 4)
                total_contribution += contribution
                
                print(f"{name:<8} {weight:>5.2f}% 昨日:{p_n1:>10.2f} 現價:{p_n:>10.2f} 貢獻:{contribution:>+10.4f}")
                
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
            time.sleep(0.1) 
        except Exception as e:
            print(f"❌ 錯誤: {name} ({sid}) - {e}")

    final_res = round(total_contribution, 4)
    print("-" * 80)
    print(f"🔥 預估總漲跌貢獻: {final_res:+.4f}")

    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'<div id="total-sum">.*?</div>', f'<div id="total-sum">{final_res:+.4f}</div>', content)
        content = re.sub(r'<tbody id="stock-details">.*?</tbody>', f'<tbody id="stock-details">{table_rows}</tbody>', content, flags=re.DOTALL)
        content = re.sub(r'<div class="update-time" id="last-update">.*?</div>', f'<div class="update-time" id="last-update">最後更新：{now_str}</div>', content)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ 網頁明細更新完成！")

if __name__ == "__main__":
    run_monitor()
