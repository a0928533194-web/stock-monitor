import pandas as pd
import yfinance as yf
from datetime import datetime

# 完整成分股對照表 (依據您的 v15.3 版本數據)
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
    print(f"查詢時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("正在抓取 Yahoo Finance 數據並計算貢獻度...")
    
    results = []
    total_contribution = 0
    
    for name, (sid, weight) in stocks_data.items():
        try:
            stock = yf.Ticker(sid)
            # 抓取 5 天數據確保能拿到昨收與今收
            hist = stock.history(period="5d")
            
            if len(hist) >= 2:
                p_n = hist['Close'].iloc[-1]   # 當天 (n)
                p_n1 = hist['Close'].iloc[-2]  # 昨日 (n-1)
                
                # 計算邏輯：(當天 - 昨天) * 比例 / 100
                contribution = (p_n - p_n1) * (weight / 100)
                total_contribution += contribution
                
                results.append({
                    "投資名稱": name,
                    "代號": sid,
                    "比例": f"{weight}%",
                    "昨日(n-1)": round(p_n1, 2),
                    "當天(n)": round(p_n, 2),
                    "漲跌貢獻": round(contribution, 4)
                })
        except Exception as e:
            print(f"無法取得 {name}({sid}) 數據: {e}")
            
    # 輸出結果表格
    df = pd.DataFrame(results)
    print("\n" + "="*70)
    print(df.to_string(index=False))
    print("="*70)
    
    # 輸出總結
    print(f"\n🔥 預估基金總漲跌貢獻： {round(total_contribution, 4)}")
    print("="*70)

if __name__ == "__main__":
    run_monitor()
