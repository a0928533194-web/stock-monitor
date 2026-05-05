import pandas as pd
import yfinance as yf
from datetime import datetime
import time

# 持股資料維持不變
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
    print(f"查詢時間 (UTC): {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    results = []
    total_contribution = 0
    
    for name, (sid, weight) in stocks_data.items():
        try:
            # 增加抓取天數到 10 天，確保一定能跨過連假或週末
            stock = yf.Ticker(sid)
            hist = stock.history(period="10d")
            
            # 清除可能存在的空值 (NaN)
            hist = hist.dropna(subset=['Close'])
            
            if len(hist) >= 2:
                p_n = hist['Close'].iloc[-1]   # 最新收盤價
                p_n1 = hist['Close'].iloc[-2]  # 前一交易日收盤價
                
                contribution = (p_n - p_n1) * (weight / 100)
                total_contribution += contribution
                
                results.append({
                    "名稱": name,
                    "昨日": round(p_n1, 1),
                    "今天": round(p_n, 1),
                    "漲跌": round(p_n - p_n1, 1),
                    "貢獻": round(contribution, 4)
                })
            else:
                print(f"無法取得足夠數據: {name} ({sid})")
            
            # 稍微停頓 0.5 秒，避免被 Yahoo 視為攻擊
            time.sleep(0.5)
            
        except Exception as e:
            print(f"處理 {name} 出錯: {e}")
            
    if results:
        df = pd.DataFrame(results)
        print("\n" + "="*60)
        print(df.to_string(index=False))
        print("="*60)
        print(f"\n🔥 預估基金總漲跌貢獻： {round(total_contribution, 4)}")
    else:
        print("\n❌ 失敗：完全抓不到任何有效的股價數據，請稍後再試。")

if __name__ == "__main__":
    run_monitor()
