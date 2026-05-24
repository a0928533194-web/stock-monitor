import yfinance as yf
from datetime import datetime
import pytz
import time

# 數據設定 (確保代號正確：上市用 .TW，上櫃用 .TWO)
FUNDS_CONFIG = {
    "yuanta": {
        "name": "元大店頭基金",
        "stocks": {
            "旺矽": ("6223.TWO", 9.70), "台積電": ("2330.TW", 7.88), "穎崴": ("6515.TWO", 6.12), 
            "精測": ("6510.TWO", 5.68), "信驊": ("5274.TWO", 5.63), "聯亞": ("3081.TWO", 4.56), 
            "群聯": ("8299.TWO", 3.95), "光聖": ("6442.TW", 3.75), "華星光": ("4979.TWO", 3.15), "台燿": ("6274.TWO", 3.00)
        }
    },
    "shinkin_three": {
        "name": "新光大三通基金",
        "stocks": {
            "欣興": ("3037.TW", 9.47), "景碩": ("3189.TW", 7.10), "世芯-KY": ("3661.TW", 6.93), 
            "台積電": ("2330.TW", 6.59), "旺矽": ("6223.TWO", 6.27), "大量": ("3167.TW", 6.06), 
            "台達電": ("2308.TW", 5.37), "弘塑": ("3131.TW", 4.95), "旺宏": ("2337.TW", 3.94), "力旺": ("3529.TWO", 3.92)
        }
    }
}

def get_fund_data(stocks_dict):
    total_contribution, total_pct = 0, 0
    table_rows = ""
    for name, (ticker_str, weight) in stocks_dict.items():
        # 增加強制緩衝時間，避免被API擋掉
        time.sleep(0.5) 
        
        success = False
        for attempt in range(3):
            try:
                stock = yf.Ticker(ticker_str)
                hist = stock.history(period="5d")
                if len(hist) < 2:
                    continue
                
                p_yesterday = round(hist['Close'].iloc[-2], 2)
                p_current = round(stock.fast_info.get('lastPrice', hist['Close'].iloc[-1]), 2)
                
                diff = round(p_current - p_yesterday, 2)
                contrib_pct = (diff / p_yesterday) * weight
                contribution = round(diff * (weight / 100), 4)
                
                total_pct += contrib_pct
                total_contribution += contribution
                
                color = "up" if diff > 0 else "down" if diff < 0 else ""
                table_rows += f"<tr><td>{name}</td><td class='weight'>{weight}%</td><td>{p_yesterday}</td><td class='{color}'>{p_current}</td><td class='{color}'>{contrib_pct:+.2f}%</td><td class='{color}'>{contribution:+.4f}</td></tr>"
                success = True
                break 
            except Exception as e:
                time.sleep(1)
        
        if not success:
            print(f"【嚴重警告】無法抓取 {name} ({ticker_str})，請檢查代號是否正確。")
            
    return round(total_contribution, 4), round(total_pct, 2), table_rows

# (run_monitor 函式其餘部分保持不變)
# ... [請保持原本的 run_monitor 函式] ...
