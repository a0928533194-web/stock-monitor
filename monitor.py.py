import yfinance as yf
from datetime import datetime, time as dtime
import time
import os
import re

# 完全依照 2026/03/31 投資明細截圖 (共 26 檔)
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

def is_market_open():
    """ 判斷目前是否為台股開盤時間 (週一至週五 09:00-13:35) """
    now = datetime.now()
    if now.weekday() >= 5:  # 0-4 是週一到週五
        return False
    market_start = dtime(9, 0)
    market_end = dtime(13, 35)
    return market_start <= now.time() <= market_end

def run_monitor():
    total_contribution = 0
    table_rows = "" 
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"\n--- 正在更新數據: {now_str} ---")

    for name, (sid, weight) in stocks_data.items():
        try:
            stock = yf.Ticker(sid)
            hist = stock.history(period="7d")
            hist = hist[hist['Close'].notna()]
            
            if len(hist) >= 2:
                p_n1 = round(hist['Close'].iloc[-2], 2)
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
    
    # 更新 index.html
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'<div id="total-sum">.*?</div>', f'<div id="total-sum">{final_res:+.4f}</div>', content)
        content = re.sub(r'<tbody id="stock-details">.*?</tbody>', f'<tbody id="stock-details">{table_rows}</tbody>', content, flags=re.DOTALL)
        content = re.sub(r'<div class="update-time" id="last-update">.*?</div>', f'<div class="update-time" id="last-update">最後更新：{now_str}</div>', content)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
    
    print(f"✅ 更新完成，目前總貢獻: {final_res:+.4f}")

if __name__ == "__main__":
    print("🚀 實時監控啟動...")
    while True:
        if is_market_open():
            run_monitor()
            time.sleep(60)  # 開盤時間每 60 秒更新一次
        else:
            # 非開盤時間，每 15 分鐘檢查一次是否開盤
            print(f"💤 目前非交易時段 ({datetime.now().strftime('%H:%M')})，稍後檢查...")
            # 為了讓您現在測試方便，如果是「非開盤時間」想強制執行一次，可以取消下面這行的註解：
            # run_monitor() 
            time.sleep(900)
