import yfinance as yf
from datetime import datetime
import time
import os
import re

# 您的 26 檔成分股比例資料 (v15.3 權重)
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
    table_rows = "" 
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"\n🚀 啟動台股成分股監測 - {now_str}")
    print("-" * 70)
    print(f"{'股票':<8} {'比例':<8} {'昨日(N-1)':<10} {'現價(N)':<10} {'貢獻值':<10}")
    print("-" * 70)

    for name, (sid, weight) in stocks_data.items():
        try:
            stock = yf.Ticker(sid)
            # 抓取 5 天內的資料過濾 NaN，確保 N-1 永遠是正確的前一交易日
            hist = stock.history(period="5d")
            hist = hist[hist['Close'].notna()]
            
            if len(hist) >= 1:
                # 取得昨日收盤 (N-1)
                p_n1 = round(hist['Close'].iloc[-1], 2)
                # 取得即時現價 (N)
                p_n = stock.fast_info['lastPrice']
                if p_n is None or p_n == 0:
                    p_n = p_n1
                p_n = round(p_n, 2)
                
                diff = round(p_n - p_n1, 2)
                contribution = round(diff * (weight / 100), 4)
                total_contribution += contribution
                
                # 1. 在 GitHub Actions 日誌印出詳細資料
                print(f"{name:<8} {weight:>5.2f}% {p_n1:>12.2f} {p_n:>10.2f} {contribution:>+10.4f}")
                
                # 2. 生成網頁用的 HTML 表格列 (加入比例欄位)
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
            time.sleep(0.1) # 稍微延遲避免頻繁抓取
        except Exception as e:
            print(f"❌ 處理 {name} 時出錯: {e}")

    final_res = round(total_contribution, 4)
    print("-" * 70)
    print(f"🔥 預估基金總漲跌貢獻: {final_res:+.4f}")
    print("-" * 70)

    # --- 關鍵修復：將數據填入 index.html ---
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 替換總額
        content = re.sub(r'<div id="total-sum">.*?</div>', f'<div id="total-sum">{final_res:+.4f}</div>', content)
        # 替換表格詳細內容
        content = re.sub(r'<tbody id="stock-details">.*?</tbody>', f'<tbody id="stock-details">{table_rows}</tbody>', content, flags=re.DOTALL)
        # 替換更新時間
        content = re.sub(r'<div class="update-time" id="last-update">.*?</div>', f'<div class="update-time" id="last-update">最後更新：{now_str} (TW)</div>', content)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ 網頁明細更新完畢！")

if __name__ == "__main__":
    run_monitor()
