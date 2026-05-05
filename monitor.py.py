import pandas as pd
import yfinance as yf
from datetime import datetime
import time

# 持股資料 (v15.3 版本)
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
    # 這裡顯示的是台灣時間 (UTC+8)
    now_tw = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"📊 監測時間 (TW): {now_tw}")
    
    results = []
    total_contribution = 0
    
    for name, (sid, weight) in stocks_data.items():
        try:
            stock = yf.Ticker(sid)
            
            # 1. 抓取歷史資料獲取「昨日收盤價」 (N-1)
            hist = stock.history(period="5d")
            hist = hist[hist['Close'].notna()]
            
            if len(hist) < 1:
                print(f"無法取得歷史數據: {name}")
                continue

            # N-1 天：取歷史資料中最後一筆完整的收盤價
            price_n1 = hist['Close'].iloc[-1]
            
            # 2. 抓取「最新即時價格」 (N)
            # 使用 fast_info 可以避開歷史資料未更新的問題
            price_n = stock.fast_info['lastPrice']
            
            # 如果即時價抓不到，再退而求其次用歷史最後一筆
            if price_n is None or pd.isna(price_n):
                 price_n = price_n1 

            # 計算漲跌貢獻 (N - N-1) * 比例 / 100
            change = price_n - price_n1
            contribution = change * (weight / 100)
            total_contribution += contribution
            
            results.append({
                "名稱": name,
                "昨日(N-1)": round(price_n1, 2),
                "最新(N)": round(price_n, 2),
                "漲跌": round(change, 2),
                "貢獻": round(contribution, 4)
            })
            
            time.sleep(0.2) # 稍微停頓
            
        except Exception as e:
            print(f"處理 {name} ({sid}) 出錯: {e}")
            
    if results:
        df = pd.DataFrame(results)
        print("\n" + "="*75)
        print(df.to_string(index=False))
        print("="*75)
        print(f"\n🔥 預估基金總漲跌貢獻 (N - N-1)： {round(total_contribution, 4)}")
        print("="*75)
    else:
        print("\n❌ 錯誤：未能成功抓取任何數據。")

if __name__ == "__main__":
    run_monitor()
