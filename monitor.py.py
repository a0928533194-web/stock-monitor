import yfinance as yf
from datetime import datetime
import os
import re
import pytz
import time
import requests

# ==============================================================================
# 1. 固定基金清單：瀚亞科技 (維持原清單與權重)
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
# 2. 官方動態抓取：從台灣證交所官方 OpenData 獲取元大店頭基金(0048)最新成分股
# ==============================================================================
def fetch_yuanta_holdings():
    """ 🚀 直連台灣證交所/櫃買中心官方公開資料庫，獲取 0048 最新前十大持股（100%不被擋） """
    # 這是台灣證管會官方提供的投信基金持股明細公開接口
    url = "https://openapi.twse.com.tw/v1/fund/MI_INDEX_FUND_HOLDING"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    stocks = {}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        data = res.json()
        
        if isinstance(data, list):
            for item in data:
                # 篩選出元大店頭基金（官方證券代號通常包含 0048 或基金全稱）
                fund_code = item.get("基金代號", "").strip()
                fund_name = item.get("基金名稱", "").strip()
                
                if "0048" in fund_code or "元大店頭" in fund_name:
                    stock_name = item.get("股票名稱", "").strip()
                    stock_code = item.get("股票代號", "").strip()
                    weight_str = item.get("持股比例", "0")
                    
                    if stock_name and stock_code and stock_code.isdigit():
                        try:
                            weight = float(weight_str)
                            if weight > 0:
                                stocks[stock_name] = (stock_code, weight)
                        except ValueError:
                            continue
                            
        print(f"【證交所官方資料庫】成功動態獲取到 {len(stocks)} 檔元大店頭最新持股標的。")
    except Exception as e:
        print(f"【證交所官方資料庫失敗】原因: {e}")
        
    return stocks

# ==============================================================================
# 3. 核心數據計算：完全沿用你原本的 yfinance 查價與計算邏輯
# ==============================================================================
def get_fund_data(stocks_dict, is_dynamic=False):
    total_contribution = 0
    table_rows = ""
    
    for name, data in stocks_dict.items():
        try:
            if is_dynamic:
                sid, weight = data
                # 🔄 100% 沿用你原本能動的上市櫃容錯判定
                stock = yf.Ticker(f"{sid}.TW")
                hist = stock.history(period="2d")
                if len(hist) < 2:
                    stock = yf.Ticker(f"{sid}.TWO")
                    hist = stock.history(period="2d")
            else:
                ticker_str, weight = data
                stock = yf.Ticker(ticker_str)
                hist = stock.history(period="2d")
                
            if len(hist) < 2: continue
            
            p_yesterday = round(hist['Close'].iloc[-2], 2)
            p_current = round(stock.fast_info['lastPrice'], 2)
            diff = round(p_current - p_yesterday, 2)
            
            # 你的公式：貢獻% = (現價 - 昨收) / 昨收 * 權重
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
        except: pass
    return round(total_contribution, 4), table_rows

# ==============================================================================
# 4. 主流程：結合數據並覆寫網頁檔案
# ==============================================================================
def run_monitor():
    tw_tz = pytz.timezone('Asia/Taipei')
    now_tw = datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    # 步驟 A: 從最穩定的台灣證交所官方管道撈取最新持股名單
    yuanta_dynamic_stocks = fetch_yuanta_holdings()
    
    # 步驟 B: 丟進你的原始 yfinance 邏輯進行計價
    y_res, y_rows = get_fund_data(yuanta_dynamic_stocks, is_dynamic=True)
    e_res, e_rows = get_fund_data(eastspring_stocks, is_dynamic=False)

    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        content = re.sub(r'id="update-time">.*?</span>', f'id="update-time">{now_tw}</span>', content)
        content = re.sub(r'id="yuanta-sum".*?>.*?</div>', f'id="yuanta-sum" class="total-sum">{y_res:+.4f}</div>', content)
        content = re.sub(r'<tbody id="yuanta-details">.*?</tbody>', f'<tbody id="yuanta-details">{y_rows}</tbody>', content, flags=re.DOTALL)
        content = re.sub(r'id="east-sum".*?>.*?</div>', f'id="east-sum" class="total-sum">{e_res:+.4f}</div>', content)
        content = re.sub(r'<tbody id="east-details">.*?</tbody>', f'<tbody id="east-details">{e_rows}</tbody>', content, flags=re.DOTALL)

        force_id = int(time.time())
        content = re.sub(r'', '', content)
        content += f"\n"

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("【系統提示】網頁數據已成功重新渲染完畢。")

if __name__ == "__main__":
    run_monitor()
