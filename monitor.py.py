import yfinance as yf
from datetime import datetime
import os
import re
import pytz
import time
import requests
from bs4 import BeautifulSoup

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
    """ 🚀 100% 從 MoneyDJ 網頁抓取元大店頭基金成分股與權重 """
    url = "https://www.moneydj.com/funddj/yp/yp013000.djhtm?a=ACYT07"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    stocks = {}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        # 自動識別 MoneyDJ 的網頁編碼 (通常是 Big5 或 cp950)，防止文字變亂碼導致後面查不到 yfinance
        res.encoding = res.apparent_encoding if res.apparent_encoding else 'big5'
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 掃描網頁中的所有表格行
        for tr in soup.find_all('tr'):
            tds = [td.text.strip() for td in tr.find_all('td')]
            
            # MoneyDJ 的成分股表格通常一行有 3~5 個欄位 (名稱、比例、前後期對比等)
            if len(tds) >= 2:
                # 欄位一通常是股票名稱（例如 "旺矽(6223)" 或 "旺矽"）
                name_field = tds[0]
                
                # 利用正規表達式把名稱中的 4 碼以上數字（代號）抓出來
                code_match = re.search(r'(\d{4,5})', name_field)
                
                # 如果名稱欄沒寫代號，就去這行裡面的超連結 (a tag) 找有沒有代號
                if not code_match:
                    a_tag = tr.find('a')
                    if a_tag:
                        href = a_tag.get('href', '')
                        code_match = re.search(r'a=(\d{4,5})', href) or re.search(r'\'(\d{4,5})\'', href)
                
                if code_match:
                    code = code_match.group(1)
                    # 清理名稱，把括號和代號去掉，只留純中文名稱
                    clean_name = re.sub(r'[\(\)\d\s]', '', name_field)
                    if not clean_name and a_tag: 
                        clean_name = a_tag.text.strip()
                    
                    # 在同一行中尋找帶有百分比 (%) 或是可以轉成 float 的權重數字
                    weight = None
                    for text in tds[1:]:
                        text_clean = text.replace('%', '').strip()
                        try:
                            val = float(text_clean)
                            if 0.1 < val < 99.0: # 合理的單一成分股權重範圍
                                weight = val
                                break
                        except ValueError:
                            continue
                    
                    if clean_name and code and weight is not None:
                        stocks[clean_name] = (code, weight)
                        
        print(f"【網頁抓取成功】成功從 MoneyDJ 撈到 {len(stocks)} 檔成分股。")
    except Exception as e:
        print(f"【網頁抓取失敗】錯誤原因: {e}")
        
    return stocks

def get_fund_data(stocks_dict, is_dynamic=False):
    total_contribution = 0
    table_rows = ""
    
    for name, data in stocks_dict.items():
        try:
            if is_dynamic:
                sid, weight = data
                # 🔄 自動上市(.TW)與上櫃(.TWO)代碼市場容錯識別機制
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
            
            # 公式：貢獻趴數 = (限價 - 昨收) / 昨收 * 權重
            contrib_percent = (diff / p_yesterday) * weight
            
            # 原金額預估貢獻度
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
    
    # 執行修正版全網頁解析爬蟲
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

        force_id = int(time.time())
        content = re.sub(r'', '', content)
        content += f"\n"

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    run_monitor()
