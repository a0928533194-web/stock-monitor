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
    """ 🚀 僅從 MoneyDJ 網頁動態抓取元大店頭基金的【成分股標的與權重】 """
    url = "https://www.moneydj.com/funddj/yp/yp013000.djhtm?a=ACYT07"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    stocks = {}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.encoding = 'big5' # MoneyDJ 網頁指定 big5 編碼避免亂碼
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 尋找網頁中所有的超連結
        for a_tag in soup.find_all('a'):
            href = a_tag.get('href', '')
            text_name = a_tag.text.strip()
            
            # 透過網址中的 Link2Stk('代號') 或 ?a=代號 提取出純數字股票代號
            code_match = re.search(r'Link2Stk\(\'([0-9]+)\'\)', href) or re.search(r'\?a=([0-9]+)', href)
            
            if code_match and text_name:
                code = code_match.group(1)
                
                # 確保是 4 碼以上的台灣個股代號，且過濾掉基金本身
                if code.isdigit() and len(code) >= 4 and not text_name.startswith("元大"):
                    # 找到該個股那一列表格 (tr)，抓取其持股比例
                    tr = a_tag.find_parent('tr')
                    if tr:
                        tds = [td.text.strip() for td in tr.find_all('td')]
                        weight = None
                        for td_text in tds:
                            clean_td = td_text.replace('%', '').strip()
                            try:
                                val = float(clean_td)
                                if 0.05 < val < 95.0: # 鎖定合理的權重數字
                                    weight = val
                                    break
                            except ValueError:
                                continue
                        
                        if weight is not None:
                            stocks[text_name] = (code, weight)
                            
        print(f"【成功抓取標的】已從網頁更新獲取 {len(stocks)} 檔元大店頭成分股標的。")
    except Exception as e:
        print(f"【抓取標的失敗】: {e}")
        
    return stocks

def get_fund_data(stocks_dict, is_dynamic=False):
    total_contribution = 0
    table_rows = ""
    
    for name, data in stocks_dict.items():
        try:
            if is_dynamic:
                sid, weight = data
                # 🔄 完全沿用您原本最原始、能動的 yfinance 查價與後綴識別邏輯
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
            
            # 公式：貢獻% = (現價 - 昨收) / 昨收 * 權重
            contrib_percent = (diff / p_yesterday) * weight
            
            # 預估金額貢獻度
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
    
    # 從網頁抓取最新標的清單
    yuanta_dynamic_stocks = fetch_yuanta_holdings()
    
    # 丟進原始 yfinance 流程查價並計算
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
