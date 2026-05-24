import yfinance as yf
from datetime import datetime
import os
import re
import pytz
import time

# 中文名稱對照表（首頁呈現用）
FUND_NAMES = {
    "yuanta": "元大店頭基金", "eastspring": "瀚亞科技基金", "allianz_taiwan": "安聯台灣大壩基金",
    "allianz_tech": "安聯台灣科技基金", "fubon_premium": "富邦首選基金", "nomura_etech": "野村e科技基金",
    "nomura_premium": "野村優質基金", "nomura_growth": "野村成長基金", "nomura_fortune": "野村鴻運基金",
    "shinkin_three": "新光大三通基金", "upmc_allweather": "統一全天候基金"
}

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

def get_fund_data(stocks_dict):
    total_contribution = 0
    total_pct = 0
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
            
            contrib_percent = (diff / p_yesterday) * weight
            total_pct += contrib_percent
            
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
        except:
            pass
            
    return round(total_contribution, 4), round(total_pct, 2), table_rows

def run_monitor():
    tw_tz = pytz.timezone('Asia/Taipei')
    now_tw = datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        content = re.sub(r'id="update-time">.*?</span>', f'id="update-time">{now_tw}</span>', content)
        
        home_cards_html = "" # 用來存首頁卡片
        
        for fund_key, stocks_dict in funds_data_config.items():
            fixed_key = fund_key if fund_key != "eastspring" else "east"
            total_sum, total_pct, table_rows = get_fund_data(stocks_dict)
            
            # 製作首頁小卡片 (第一排:名稱 / 第二排:總貢獻 / 第三排:總貢獻%)
            color_class = "up" if total_sum > 0 else "down" if total_sum < 0 else ""
            fund_zh_name = FUND_NAMES.get(fund_key, fund_key)
            home_cards_html += f"""
            <div class="overview-card" style="cursor:pointer;" onclick="document.getElementById('fundSelector').value='{fund_key}'; switchFund('{fund_key}');">
                <div class="card-title">{fund_zh_name}</div>
                <div class="card-sum {color_class}">{total_sum:+.4f}</div>
                <div class="card-pct {color_class}">{total_pct:+.2f}%</div>
            </div>
            """
            
            # 替換個別詳細頁面欄位
            content = re.sub(rf'id="{fixed_key}-sum".*?>.*?</div>', f'id="{fixed_key}-sum" class="total-sum">{total_sum:+.4f}</div>', content)
            content = re.sub(rf'id="{fixed_key}-pct".*?>.*?</div>', f'id="{fixed_key}-pct" class="total-percent">{total_pct:+.2f}%</div>', content)
            content = re.sub(rf'<tbody id="{fixed_key}-details">.*?</tbody>', f'<tbody id="{fixed_key}-details">{table_rows}</tbody>', content, flags=re.DOTALL)

        # 把動態卡片塞進首頁區塊中
        content = re.sub(r'<div class="home-grid" id="home-cards-container">.*?</div>', f'<div class="home-grid" id="home-cards-container">{home_cards_html}</div>', content, flags=re.DOTALL)

        # 根除快取尾碼
        force_id = int(time.time())
        content = re.sub(r'', '', content)
        content += f"\n"

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("【大功告成】首頁電視牆與細節數據已全數注入完成！")

if __name__ == "__main__":
    run_monitor()
