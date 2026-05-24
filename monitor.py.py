import yfinance as yf
from datetime import datetime
import os
import re
import pytz
import time

# 17檔基金名稱對照表 (確保與下拉選單及首頁排序完全契合)
FUND_NAMES = {
    "yuanta": "元大店頭基金", "eastspring": "瀚亞科技基金", "shinkin_three": "新光大三通基金", "upmc_allweather": "統一全天候基金",
    "allianz_taiwan": "安聯台灣大壩基金", "allianz_tech": "安聯台灣科技基金", "allianz_intel": "安聯台灣智聯基金", "allianz_twgrowth": "安聯台灣大盤基金",
    "fubon_premium": "富邦首選基金", "fubon_dividend": "富邦高股息基金", "fubon_core": "富邦台灣核心二號基金",
    "nomura_etech": "野村e科技基金", "nomura_premium": "野村優質基金", "nomura_growth": "野村成長基金", "nomura_fortune": "野村鴻運基金", "nomura_dividend": "野村台灣高股息基金", "nomura_twdpremium": "野村優質基金-台幣"
}

funds_data_config = {
    "yuanta": {
        "旺矽": ("6223.TWO", 9.70), "台積電": ("2330.TW", 7.88), "穎崴": ("6515.TWO", 6.12), "精測": ("6510.TWO", 5.68), "信驊": ("5274.TWO", 5.63), "聯亞": ("3081.TWO", 4.56), "群聯": ("8299.TWO", 3.95), "光聖": ("6442.TW", 3.75), "華星光": ("4979.TWO", 3.15), "台燿": ("6274.TWO", 3.00)
    },
    "eastspring": {
        "奇鋐": ("3017.TW", 8.25), "欣興": ("3037.TW", 8.07), "台積電": ("2330.TW", 7.90), "台光電": ("2383.TW", 6.74), "台達電": ("2308.TW", 6.47), "智邦": ("2345.TW", 6.00), "台燿": ("6274.TWO", 5.55), "光寶科": ("2301.TW", 5.20), "光聖": ("6442.TW", 5.17), "聯亞": ("3081.TWO", 5.03)
    },
    "shinkin_three": {
        "欣興": ("3037.TW", 9.47), "景碩": ("3189.TW", 7.10), "世芯-KY": ("3661.TW", 6.93), "台積電": ("2330.TW", 6.59), "旺矽": ("6223.TWO", 6.27), "大量": ("3167.TW", 6.06), "台達電": ("2308.TW", 5.37), "弘塑": ("3131.TW", 4.95), "旺宏": ("2337.TW", 3.94), "力旺": ("3529.TWO", 3.92)
    },
    "upmc_allweather": {
        "台光電": ("2383.TW", 9.85), "台達電": ("2308.TW", 8.68), "欣興": ("3037.TW", 8.50), "奇鋐": ("3017.TW", 7.88), "台積電": ("2330.TW", 7.08), "貿聯-KY": ("3665.TW", 6.23), "穎崴": ("6515.TWO", 5.44), "健策": ("3653.TW", 4.51), "南電": ("8046.TW", 3.75), "致茂": ("2360.TW", 3.74)
    },
    "allianz_taiwan": {
        "旺矽": ("6223.TWO", 11.30), "穎崴": ("6515.TWO", 10.49), "台積電": ("2330.TW", 6.87), "台光電": ("2383.TW", 6.44), "欣興": ("3037.TW", 5.65), "信驊": ("5274.TWO", 5.45), "台達電": ("2308.TW", 5.05), "台燿": ("6274.TWO", 4.97), "奇鋐": ("3017.TW", 3.76), "智邦": ("2345.TW", 3.34)
    },
    "allianz_tech": {
        "旺矽": ("6223.TWO", 8.54), "穎崴": ("6515.TWO", 8.38), "台積電": ("2330.TW", 6.59), "台光電": ("2383.TW", 6.58), "創意": ("3443.TW", 5.34), "台燿": ("6274.TWO", 4.73), "台達電": ("2308.TW", 4.49), "信驊": ("5274.TWO", 4.09), "金像電": ("2368.TW", 4.07), "威剛": ("3260.TWO", 3.78)
    },
    "allianz_intel": {
        "旺矽": ("6223.TWO", 9.77), "創意": ("3443.TW", 8.23), "信驊": ("5274.TWO", 7.62), "台燿": ("6274.TWO", 7.15), "穎崴": ("6515.TWO", 6.84), "新唐": ("4919.TW", 5.92), "台光電": ("2383.TW", 5.38), "台積電": ("2330.TW", 4.88), "金像電": ("2368.TW", 4.58), "譜瑞-KY": ("4966.TWO", 4.14)
    },
    "allianz_twgrowth": {
        "旺矽": ("6223.TWO", 9.20), "穎崴": ("6515.TWO", 8.44), "台積電": ("2330.TW", 6.94), "台光電": ("2383.TW", 6.64), "信驊": ("5274.TWO", 5.25), "創意": ("3443.TW", 5.16), "台燿": ("6274.TWO", 4.90), "世芯-KY": ("3661.TW", 4.70), "金像電": ("2368.TW", 4.22), "台達電": ("2308.TW", 3.90)
    },
    "fubon_premium": {
        "欣興": ("3037.TW", 9.89), "旺矽": ("6223.TWO", 8.34), "金像電": ("2368.TW", 7.24), "台達電": ("2308.TW", 6.49), "群聯": ("8299.TWO", 5.94), "光聖": ("6442.TW", 5.50), "貿聯-KY": ("3665.TW", 5.48), "台積電": ("2330.TW", 5.28), "華星光": ("4979.TWO", 4.76), "南電": ("8046.TW", 4.58)
    },
    "fubon_dividend": {
        "欣興": ("3037.TW", 9.87), "健策": ("3653.TW", 8.33), "金像電": ("2368.TW", 7.42), "台達電": ("2308.TW", 7.02), "群聯": ("8299.TWO", 6.13), "智邦": ("2345.TW", 5.44), "台積電": ("2330.TW", 5.13), "南電": ("8046.TW", 4.56), "新唐": ("4919.TW", 4.02), "景碩": ("3189.TW", 3.88)
    },
    "fubon_core": {
        "欣興": ("3037.TW", 9.88), "旺矽": ("6223.TWO", 8.45), "金像電": ("2368.TW", 7.50), "台達電": ("2308.TW", 6.84), "群聯": ("8299.TWO", 5.90), "光聖": ("6442.TW", 5.23), "台積電": ("2330.TW", 5.10), "南電": ("8046.TW", 4.80), "華星光": ("4979.TWO", 4.34), "景碩": ("3189.TW", 3.95)
    },
    "nomura_etech": {
        "南電": ("8046.TW", 8.85), "欣興": ("3037.TW", 8.79), "聯亞": ("3081.TWO", 6.67), "台積電": ("2330.TW", 6.57), "奇鋐": ("3017.TW", 5.97), "華星光": ("4979.TWO", 4.84), "景碩": ("3189.TW", 4.00), "聯發科": ("2454.TW", 3.91), "竑騰": ("6680.TW", 3.82), "光聖": ("6442.TW", 3.63)
    },
    "nomura_premium": {
        "健策": ("3653.TW", 8.72), "台光電": ("2383.TW", 8.62), "台達電": ("2308.TW", 8.44), "台積電": ("2330.TW", 8.03), "穎崴": ("6515.TWO", 7.42), "川湖": ("2059.TW", 7.10), "鴻勁": ("7741.TW", 6.70), "金像電": ("2368.TW", 5.90), "欣興": ("3037.TW", 5.22), "力旺": ("3529.TWO", 4.64)
    },
    "nomura_growth": {
        "台光電": ("2383.TW", 7.24), "欣興": ("3037.TW", 7.22), "穎崴": ("6515.TWO", 6.34), "台達電": ("2308.TW", 5.68), "金像電": ("2368.TW", 5.53), "台積電": ("2330.TW", 5.40), "南電": ("8046.TW", 5.30), "奇鋐": ("3017.TW", 5.21), "健策": ("3653.TW", 5.08), "旺矽": ("6223.TWO", 4.70)
    },
    "nomura_fortune": {
        "欣興": ("3037.TW", 7.56), "奇鋐": ("3017.TW", 6.38), "健策": ("3653.TW", 5.97), "台達電": ("2308.TW", 5.90), "台光電": ("2383.TW", 5.78), "台積電": ("2330.TW", 5.57), "旺矽": ("6223.TWO", 4.60), "穎崴": ("6515.TWO", 4.34), "貿聯-KY": ("3665.TW", 3.70), "金像電": ("2368.TW", 3.69)
    },
    "nomura_dividend": {
        "健策": ("3653.TW", 8.44), "台光電": ("2383.TW", 8.12), "台積電": ("2330.TW", 7.94), "台達電": ("2308.TW", 7.82), "川湖": ("2059.TW", 6.94), "穎崴": ("6515.TWO", 6.44), "金像電": ("2368.TW", 5.48), "欣興": ("3037.TW", 5.08), "致茂": ("2360.TW", 4.14), "力旺": ("3529.TWO", 3.90)
    },
    "nomura_twdpremium": {
        "健策": ("3653.TW", 8.42), "台光電": ("2383.TW", 8.24), "台達電": ("2308.TW", 8.15), "台積電": ("2330.TW", 7.84), "川湖": ("2059.TW", 6.90), "穎崴": ("6515.TWO", 6.55), "鴻勁": ("7741.TW", 6.22), "金像電": ("2368.TW", 5.50), "欣興": ("3037.TW", 5.12), "力旺": ("3529.TWO", 4.23)
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
        home_cards_html = ""
        
        # 依照設定檔的排序順序依序運算 (這樣首頁卡片跟下拉式選單的排序就100%契合)
        for fund_key in funds_data_config.keys():
            stocks_dict = funds_data_config[fund_key]
            fixed_key = fund_key if fund_key != "eastspring" else "east"
            
            total_sum, total_pct, table_rows = get_fund_data(stocks_dict)
            
            color_class = "up" if total_sum > 0 else "down" if total_sum < 0 else ""
            fund_zh_name = FUND_NAMES.get(fund_key, fund_key)
            
            # 建立首頁網格小卡片
            home_cards_html += f"""
            <div class="overview-card" style="cursor:pointer;" onclick="document.getElementById('fundSelector').value='{fund_key}'; switchFund('{fund_key}');">
                <div class="card-title">{fund_zh_name}</div>
                <div class="card-sum {color_class}">{total_sum:+.4f}</div>
                <div class="card-pct {color_class}">{total_pct:+.2f}%</div>
            </div>
            """
            
            # 覆蓋各別子分頁表格數據
            content = re.sub(rf'id="{fixed_key}-sum".*?>.*?</div>', f'id="{fixed_key}-sum" class="total-sum">{total_sum:+.4f}</div>', content)
            content = re.sub(rf'id="{fixed_key}-pct".*?>.*?</div>', f'id="{fixed_key}-pct" class="total-percent">{total_pct:+.2f}%</div>', content)
            content = re.sub(rf'<tbody id="{fixed_key}-details">.*?</tbody>', f'<tbody id="{fixed_key}-details">{table_rows}</tbody>', content, flags=re.DOTALL)

        # 全面塞入首頁
        content = re.sub(r'<div class="home-grid" id="home-cards-container">.*?</div>', f'<div class="home-grid" id="home-cards-container">{home_cards_html}</div>', content, flags=re.DOTALL)

        # 寫入時間戳防止頁面緩存
        force_id = int(time.time())
        content = re.sub(r'', '', content)
        content += f"\n"

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("【大功告成】17檔分類基金牆與數據全數建置並更新完畢！")

if __name__ == "__main__":
    run_monitor()
