import yfinance as yf
from datetime import datetime
import os
import re
import pytz
import time
import requests
from bs4 import BeautifulSoup

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
# 2. 動態網頁抓取：元大店頭基金成分股 (直擊點擊「持股」按鈕後的真實資料網址)
# ==============================================================================
def fetch_yuanta_holdings():
    """ 🚀 繞過網頁選單，直擊 MoneyDJ 按下「持股」按鈕後的動態明細頁面 """
    # 這是破解下拉選單機關後，實際存放元大店頭(ACYT07)持股比例表格的隱藏網址
    url = "https://www.moneydj.com/funddj/yp/yp013002.djhtm?a=ACYT07"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.moneydj.com/funddj/yp/yp013000.djhtm?a=ACYT07"
    }
    stocks = {}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.encoding = 'big5' # MoneyDJ 指定 big5 編碼避免中文變亂碼
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 遍歷網頁中含有股票代號超連結的表格欄位
        for tr in soup.find_all('tr'):
            a_tag = tr.find('a', href=re.compile(r'Link2Stk|yp013000|\?a='))
            if a_tag:
                text_name = a_tag.text.strip()
                href = a_tag.get('href', '')
                
                # 從網址或超連結文字中，精準提取出 4~5 碼的台股純數字代號
                code_match = re.search(r'([0-9]{4,5})', href) or re.search(r'([0-9]{4,5})', text_name)
                
                if code_match and text_name and not text_name.startswith("元大"):
                    code = code_match.group(1)
                    
                    # 抓取跟股票名稱在同一列(tr)的持股權重百分比
                    tds = [td.text.strip() for td in tr.find_all('td')]
                    weight = None
                    for text in tds:
                        clean_text = text.replace('%', '').strip()
                        try:
                            val = float(clean_text)
                            if 0.1 < val < 95.0: # 鎖定正常的持股比例數字範圍
                                weight = val
                                break
                        except ValueError:
                            continue
                    
                    if weight is not None:
                        stocks[text_name] = (code, weight)
                        
        print(f"【網頁解析成功】已動態提取到 {len(stocks)} 檔最新的元大店頭成分股標的。")
    except Exception as e:
        print(f"【網頁解析失敗】原因: {e}")
        
    return stocks

# ==============================================================================
# 3. 核心數據計算：沿用你原本最穩定的 yfinance 邏輯
# ==============================================================================
def get_fund_data(stocks_dict, is_dynamic=False):
    total_contribution = 0
    table_rows = ""
    
    for name, data in stocks_dict.items():
        try:
            if is_dynamic:
                sid, weight = data
                # 🔄 沿用你原本能動的邏輯：優先嘗試上市(.TW)，不行自動切換成上櫃(.TWO)
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
# 4. 主程式流程：結合兩大基金數據並更新 index.html 網頁內容
# ==============================================================================
def run_monitor():
    # 統一設定台北時間
    tw_tz = pytz.timezone('Asia/Taipei')
    now_tw = datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    # 步驟 A: 到 MoneyDJ 解密後的明細頁面動態抓取元大店頭最新標的名單
    yuanta_dynamic_stocks = fetch_yuanta_holdings()
    
    # 步驟 B: 計算兩份基金的即時漲跌貢獻數據
    y_res, y_rows = get_fund_data(yuanta_dynamic_stocks, is_dynamic=True)
    e_res, e_rows = get_fund_data(eastspring_stocks, is_dynamic=False)

    # 步驟 C: 將計算好的 HTML 表格與時間塞入 index.html 檔案中
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 使用正則表達式精準替換網頁對應欄位
        content = re.sub(r'id="update-time">.*?</span>', f'id="update-time">{now_tw}</span>', content)
        content = re.sub(r'id="yuanta-sum".*?>.*?</div>', f'id="yuanta-sum" class="total-sum">{y_res:+.4f}</div>', content)
        content = re.sub(r'<tbody id="yuanta-details">.*?</tbody>', f'<tbody id="yuanta-details">{y_rows}</tbody>', content, flags=re.DOTALL)
        content = re.sub(r'id="east-sum".*?>.*?</div>', f'id="east-sum" class="total-sum">{e_res:+.4f}</div>', content)
        content = re.sub(r'<tbody id="east-details">.*?</tbody>', f'<tbody id="east-details">{e_rows}</tbody>', content, flags=re.DOTALL)

        # 強制附加一個隨機 ID 到網頁結尾，徹底根除手機瀏覽器的頑固網頁快取問題
        force_id = int(time.time())
        content = re.sub(r'', '', content)
        content += f"\n"

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("【網頁更新完畢】index.html 已成功寫入最新數據。")

if __name__ == "__main__":
    run_monitor()
