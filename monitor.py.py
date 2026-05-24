import yfinance as yf
from datetime import datetime
import os
import re
import pytz
import time

# ==============================================================================
# 超級旗艦陣容：13 檔基金最新前十大持股固定名單 (100% 避開爬蟲封鎖阻擋)
# ==============================================================================
funds_data_config = {
    "yuanta": {
        "旺矽": ("6223.TWO", 9.70), "台積電": ("2330.TW", 7.88), "穎崴": ("6515.TWO", 6.12),
        "精測": ("6510.TWO", 5.68), "信驊": ("5274.TWO", 5.63), "聯亞": ("3081.TWO", 4.56),
        "群聯": ("8299.TWO", 3.95), "光聖": ("6442.TW", 3.75), "華星光": ("4979.TWO", 3.15),
        "台燿": ("6274.TWO", 3.00)
    },
    "eastspring": {
        "奇鋐": ("3017.TW", 8.25), "欣興": ("3037.TW", 8.07), "台積電": ("2330.TW", 7.90),
        "台光電": ("2383.TW", 6.74), "台達電": ("2308.TW", 6.47), "智邦": ("2345.TW", 6.00),
        "台燿": ("6274.TWO", 5.55), "光寶科": ("2301.TW", 5.20), "光聖": ("6442.TW", 5.17),
        "聯亞": ("3081.TWO", 5.03)
    },
    "allianz_taiwan": {
        "旺矽": ("6223.TWO", 11.30), "穎崴": ("6515.TWO", 10.49), "台積電": ("2330.TW", 6.87),
        "台光電": ("2383.TW", 6.44), "欣興": ("3037.TW", 5.65), "信驊": ("5274.TWO", 5.45),
        "台達電": ("2308.TW", 5.05), "台燿": ("6274.TWO", 4.97), "奇鋐": ("3017.TW", 3.76),
        "智邦": ("2345.TW", 3.34)
    },
    "allianz_tech": {
        "旺矽": ("6223.TWO", 8.54), "穎崴": ("6515.TWO", 8.38), "台積電": ("2330.TW", 6.59),
        "台光電": ("2383.TW", 6.58), "創意": ("3443.TW", 5.34), "台燿": ("6274.TWO", 4.73),
        "台達電": ("2308.TW", 4.49), "信驊": ("5274.TWO", 4.09), "金像電": ("2368.TW", 4.07),
        "威剛": ("3260.TWO", 3.78)
    },
    "fubon_premium": {
        "欣興": ("3037.TW", 9.89), "旺矽": ("6223.TWO", 8.34), "金像電": ("2368.TW", 7.24),
        "台達電": ("2308.TW", 6.49), "群聯": ("8299.TWO", 5.94), "光聖": ("6442.TW", 5.50),
        "貿聯-KY": ("3665.TW", 5.48), "台積電": ("2330.TW", 5.28), "華星光": ("4979.TWO", 4.76),
        "南電": ("8046.TW", 4.58)
    },
    "nomura_etech": {
        "南電": ("8046.TW", 8.85), "欣興": ("3037.TW", 8.79), "聯亞": ("3081.TWO", 6.67),
        "台積電": ("2330.TW", 6.57), "奇鋐": ("3017.TW", 5.97), "華星光": ("4979.TWO", 4.84),
        "景碩": ("3189.TW", 4.00), "聯發科": ("2454.TW", 3.91), "竑騰": ("6680.TW", 3.82),
        "光聖": ("6442.TW", 3.63)
    },
    "nomura_premium": {
        "健策": ("3653.TW", 8.72), "台光電": ("2383.TW", 8.62), "台達電": ("2308.TW", 8.44),
        "台積電": ("2330.TW", 8.03), "穎崴": ("6515.TWO", 7.42), "川湖": ("2059.TW", 7.10),
        "鴻勁": ("7741.TW", 6.70), "金像電": ("2368.TW", 5.90), "欣興": ("3037.TW", 5.22),
        "力旺": ("3529.TWO", 4.64)
    },
    "nomura_growth": {
        "台光電": ("2383.TW", 7.24), "欣興": ("3037.TW", 7.22), "穎崴": ("6515.TWO", 6.34),
        "台達電": ("2308.TW", 5.68), "金像電": ("2368.TW", 5.53), "台積電": ("2330.TW", 5.40),
        "南電": ("8046.TW", 5.30), "奇鋐": ("3017.TW", 5.21), "健策": ("3653.TW", 5.08),
        "旺矽": ("6223.TWO", 4.70)
    },
    "nomura_fortune": {
        "欣興": ("3037.TW", 7.56), "奇鋐": ("3017.TW", 6.38), "健策": ("3653.TW", 5.97),
        "台達電": ("2308.TW", 5.90), "台光電": ("2383.TW", 5.78), "台積電": ("2330.TW", 5.57),
        "旺矽": ("6223.TWO", 4.60), "穎崴": ("6515.TWO", 4.34), "貿聯-KY": ("3665.TW", 3.70),
        "金像電": ("2368.TW", 3.69)
    },
    "shinkin_three": {
        "欣興": ("3037.TW", 9.47), "景碩": ("3189.TW", 7.10), "世芯-KY": ("3661.TW", 6.93),
        "台積電": ("2330.TW", 6.59), "旺矽": ("6223.TWO", 6.27), "大量": ("3167.TW", 6.06),
        "台達電": ("2308.TW", 5.37), "弘塑": ("3131.TW", 4.95), "旺宏": ("2337.TW", 3.94),
        "力旺": ("3529.TWO", 3.92)
    },
    "upmc_allweather": {
        "台光電": ("2383.TW", 9.85), "台達電": ("2308.TW", 8.68), "欣興": ("3037.TW", 8.50),
        "奇鋐": ("3017.TW", 7.88), "台積電": ("2330.TW", 7.08), "貿聯-KY": ("3665.TW", 6.23),
        "穎崴": ("6515.TWO", 5.44), "健策": ("3653.TW", 4.51), "南電": ("8046.TW", 3.75),
        "致茂": ("2360.TW", 3.74)
    }
}

# ==============================================================================
# 核心單一基金算價引擎
# ==============================================================================
def get_fund_data(stocks_dict):
    total_contribution = 0
    table_rows = ""
    
    for name, data in stocks_dict.items():
        try:
            ticker_str, weight = data
            stock = yf.Ticker(ticker_str)
            hist = stock.history(period="2d")
            
            if len(hist) < 2: continue
            
            p_yesterday = round(hist['Close'].iloc[-2], 2)
            p_current = round(stock.fast_info['lastPrice'], 2)
            diff = round(p_current - p_yesterday, 2)
            
            # 預估單檔貢獻度與百分比
            contrib_percent = (diff / p_yesterday) * weight
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
# 主更新排程
# ==============================================================================
def run_monitor():
    tw_tz = pytz.timezone('Asia/Taipei')
    now_tw = datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 替換時間
        content = re.sub(r'id="update-time">.*?</span>', f'id="update-time">{now_tw}</span>', content)
        
        # 迴圈自動注入 13 檔基金數據
        for fund_key, stocks_dict in funds_data_config.items():
            total_sum, table_rows = get_fund_data(stocks_dict)
            
            # 替換總合
            sum_pattern = rf'id="{fund_key if fund_key != "eastspring" else "east"}-sum".*?>.*?</div>'
            sum_replace = f'id="{fund_key if fund_key != "eastspring" else "east"}-sum" class="total-sum">{total_sum:+.4f}</div>'
            content = re.sub(sum_pattern, sum_replace, content)
            
            # 替換表格細節
            detail_pattern = rf'<tbody id="{fund_key if fund_key != "eastspring" else "east"}-details">.*?</tbody>'
            detail_replace = f'<tbody id="{fund_key if fund_key != "eastspring" else "east"}-details">{table_rows}</tbody>'
            content = re.sub(detail_pattern, detail_replace, content, flags=re.DOTALL)

        # 寫入防止快取尾碼
        force_id = int(time.time())
        content = re.sub(r'', '', content)
        content += f"\n"

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("【大成功】13 檔黃金旗艦基金選單與數據全面更新完畢！")

if __name__ == "__main__":
    run_monitor()
