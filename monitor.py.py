import yfinance as yf
from datetime import datetime
import pytz

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
    table_rows = ""
    for name, (ticker_str, weight) in stocks_dict.items():
        stock = yf.Ticker(ticker_str)
        hist = stock.history(period="5d")
        
        # --- 診斷輸出 ---
        if len(hist) < 1:
            print(f"!!! {name} ({ticker_str}) 抓不到任何歷史資料 !!!")
            continue
        
        last_price = stock.fast_info.get('lastPrice')
        print(f"正在檢查 {name}: lastPrice={last_price}, 歷史資料筆數={len(hist)}")
        
        # 計算逻辑... (此處略，執行後看終端機即可)
        # ... (代碼保持相同功能)
