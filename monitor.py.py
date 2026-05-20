import yfinance as yf
from datetime import datetime
import os
import re
import pytz
import time
import requests

# 瀚亞科技 (維持原固定清單)
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

def fetch_yuanta_holdings():
    """ 🚀 直接向元大投信官方 API 獲取元大店頭基金最新成分股與比例（百分百不被阻擋） """
    url = "https://www.yuantafunds.com.tw/api/FundHolding/GetFundHoldingRatio"
    payload = {
        "FundCode": "0048",  # 元大店頭基金在官方的內部代碼
        "PageIndex": 1,
        "PageSize": 50
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }
    stocks = {}
    try:
        # 向官方發送 POST 請求獲取結構化 JSON 數據
        res = requests.post(url, json=payload, headers=headers, timeout=15)
        data = res.json()
        
        if data and "Data" in data and "List" in data["Data"]:
            for item in data["Data"]["List"]:
                name = item.get("StockName", "").strip()
                code = item.get("StockCode", "").strip()
                weight_str = item.get("Ratio", "0")
                
                # 確保名稱存在、代號為純數字
                if name and code and code.isdigit():
                    try:
                        weight = float(weight_str)
                        if weight > 0:
                            stocks[name] = (code, weight)
                    except ValueError:
                        continue
        print(f"【元大官方 API】成功下載 {len(stocks)} 檔最新成分股明細。")
    except Exception as e:
        print(f"【元大官方 API 失敗】: {e}")
        
    return stocks

def get_fund_data(stocks_dict, is_dynamic=False):
    total_contribution = 0
    table_rows = ""
    
    for name, data in stocks_dict.items():
        try:
            if is_dynamic:
                sid, weight = data
                # 🔄 自動進行上市(.TW)與上櫃(.TWO)市場代碼容錯識別
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
            
            # 計算公式：貢獻% = (現價 - 昨收) / 昨收 * 權重
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

def run_monitor():
    tw_tz = pytz.timezone('Asia/Taipei')
    now_tw = datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    # 執行元大投信官網 API 動態獲取
    yuanta_dynamic_stocks = fetch_yuanta_holdings()
    
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

        # 強制更新網頁 ID 避免快取
        force_id = int(time.time())
        content = re.sub(r'', '', content)
        content += f"\n"

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    run_monitor()
