import yfinance as yf
from datetime import datetime
import pytz
import time

# 設定
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
        time.sleep(0.5) # 稍微緩衝，避免請求過快
        
        # 強力容錯：如果發生任何錯誤，給予預設值，不讓該行消失
        p_yesterday, p_current, diff = 0, 0, 0
        try:
            stock = yf.Ticker(ticker_str)
            hist = stock.history(period="5d")
            if not hist.empty:
                p_yesterday = round(hist['Close'].iloc[-2], 2)
                p_current = round(stock.fast_info.get('lastPrice', hist['Close'].iloc[-1]), 2)
                diff = round(p_current - p_yesterday, 2)
        except:
            pass # 即使失敗也不會中斷迴圈

        contrib_pct = (diff / p_yesterday * 100) if p_yesterday != 0 else 0
        contribution = round(diff * (weight / 100), 4)
        
        color = "up" if diff > 0 else "down" if diff < 0 else ""
        table_rows += f"<tr><td>{name}</td><td class='weight'>{weight}%</td><td>{p_yesterday}</td><td class='{color}'>{p_current}</td><td class='{color}'>{contrib_pct:+.2f}%</td><td class='{color}'>{contribution:+.4f}</td></tr>"
    
    return "", "", table_rows

def run_monitor():
    now_tw = datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')
    # ... (HTML 生成部分同前，保持不變)
    # 這裡省略部分代碼以節省篇幅，請保留您原本的 HTML 結構
    # 關鍵是確保 get_fund_data 呼叫後，table_rows 永遠有值
