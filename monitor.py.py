import yfinance as yf
from datetime import datetime
import os
import re
import pytz
import time

# ==============================================================================
# 1. 元大店頭基金：最新前十大成分股固定清單 (100% 避開網頁阻擋)
# ==============================================================================
yuanta_stocks = {
    "旺矽": ("6223.TWO", 9.70),
    "台積電": ("2330.TW", 7.88),
    "穎崴": ("6515.TWO", 6.12),
    "精測": ("6510.TWO", 5.68),
    "信驊": ("5274.TWO", 5.63),
    "聯亞": ("3081.TWO", 4.56),
    "群聯": ("8299.TWO", 3.95),
    "光聖": ("6442.TW", 3.75),
    "華星光": ("4979.TWO", 3.15),
    "台燿": ("6274.TWO", 3.00)
}

# ==============================================================================
# 2. 瀚亞科技基金：固定清單 (維持原樣)
# ==============================================================================
eastspring_stocks = {
    "奇鋐": ("3017.TW", 8.25), "欣興": ("3037.TW", 8.07), "台積電": ("2330.TW", 7.90),
    "台光電": ("2383.TW", 6.74), "台達電": ("2308.TW", 6.47), "智邦": ("2345.TW", 6.00),
    "台燿": ("6274.TWO", 5.55), "光寶科": ("2301.TW", 5.20), "光聖": ("6442.TW", 5.17),
    "聯亞": ("3081.TWO", 5.03), "強茂": ("2481.TW", 4.51), "聯發科": ("2454.TW", 4.01),
    "華碩": ("2357.TW", 3.68), "健策": ("3653.TW", 3.38), "振樺電": ("8114.TW", 2.73),
    "旺矽": ("6223.TWO", 2.20), "致茂": ("2360.TW", 2.17), "川湖": ("2059.TW", 1.99),
    "緯創": ("3231.TW", 1.92), "南電": ("8046.TW", 1.80), "華星光": ("4979.TWO", 1.40),
    "精測": ("6510.TWO", 1.23)
}

# ==============================================================================
# 3. 核心數據計算：沿用你最原本、能動的 yfinance 邏輯
# ==============================================================================
def get_fund_data(stocks_dict):
    total_contribution = 0
    table_rows = ""
    
    for name, data in stocks_dict.items():
        try:
            ticker_str, weight = data
            
            # 使用原本能動的代號直接查價
            stock = yf.Ticker(ticker_str)
            hist = stock.history(period="2d")
            
            if len(hist) < 2: continue
            
            p_yesterday = round(hist['Close'].iloc[-2], 2)
            p_current = round(stock.fast_info['lastPrice'], 2)
            diff = round(p_current - p_yesterday, 2)
            
            # 公式：貢獻% = (現價 - 昨收) / 昨收 * 權重
            contrib_percent = (diff / p_yesterday) * weight
            
            # 金額預估貢獻度
            contribution = round(diff * (weight / 100), 4)
            total_contribution += contribution
            
            color_class = "up" if diff > 0 else "down" if diff < 0 else ""
            
            table_rows += f"""<tr>
                <td>{name}</td>
                <td class='weight'>{weight}%</td>
                <td>{p_yesterday}</td>
                <td class='{color_class}'>{p_current}</td>
                <td class='{color_class}'>{contrib_percent:+.2f}%</td>
                <td class='{color_class}'>{contribution:+.4f}</td>
            </tr>"""
        except Exception as e:
            print(f"計算 {name} 失敗: {e}")
            pass
            
    return round(total_contribution, 4), table_rows

# ==============================================================================
# 4. 主程式流程：結合數據並覆寫網頁檔案
# ==============================================================================
def run_monitor():
    tw_tz = pytz.timezone('Asia/Taipei')
    now_tw = datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    # 直接用固定名單去跑查價，100% 不會失敗
    y_res, y_rows = get_fund_data(yuanta_stocks)
    e_res, e_rows = get_fund_data(eastspring_stocks)

    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        content = re.sub(r'id="update-time">.*?</span>', f'id="update-time">{now_tw}</span>', content)
        content = re.sub(r'id="yuanta-sum".*?>.*?</div>', f'id="yuanta-sum" class="total-sum">{y_res:+.4f}</div>', content)
        content = re.sub(r'<tbody id="yuanta-details">.*?</tbody>', f'<tbody id="yuanta-details">{y_rows}</tbody>', content, flags=re.DOTALL)
        content = re.sub(r'id="east-sum".*?>.*?</div>', f'id="east-sum" class="total-sum">{e_res:+.4f}</div>', content)
        content = re.sub(r'<tbody id="east-details">.*?</tbody>', f'<tbody id="east-details">{e_rows}</tbody>', content, flags=re.DOTALL)

        # 根除快取問題
        force_id = int(time.time())
        content = re.sub(r'', '', content)
        content += f"\n"

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("【成功】雙固定基金名單網頁更新完畢！")

if __name__ == "__main__":
    run_monitor()
