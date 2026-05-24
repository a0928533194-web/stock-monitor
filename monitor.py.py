import yfinance as yf
from datetime import datetime
import os
import re
import pytz

# 17檔基金名稱對照表 (保持不變)
FUND_NAMES = {
    "yuanta": "元大店頭基金", "eastspring": "瀚亞科技基金", "shinkin_three": "新光大三通基金", "upmc_allweather": "統一全天候基金",
    "allianz_taiwan": "安聯台灣大壩基金", "allianz_tech": "安聯台灣科技基金", "allianz_intel": "安聯台灣智聯基金", "allianz_twgrowth": "安聯台灣大盤基金",
    "fubon_premium": "富邦首選基金", "fubon_dividend": "富邦高股息基金", "fubon_core": "富邦台灣核心二號基金",
    "nomura_etech": "野村e科技基金", "nomura_premium": "野村優質基金", "nomura_growth": "野村成長基金", "nomura_fortune": "野村鴻運基金", 
    "nomura_dividend": "野村台灣高股息基金", "nomura_twdpremium": "野村優質基金-台幣"
}

# (funds_data_config 區塊保持不變，為節省空間此處略過，請保留你原有的內容)

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
        
        # 產生簡潔清單
        home_table_html = """
        <table class="overview-table" style="width:100%; border-collapse:collapse; margin-top:20px;">
            <thead>
                <tr style="background:#f8f9fa;">
                    <th style="padding:10px; border:1px solid #ddd;">基金名稱</th>
                    <th style="padding:10px; border:1px solid #ddd;">今日貢獻數值</th>
                    <th style="padding:10px; border:1px solid #ddd;">今日貢獻 %</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for fund_key, fund_name in FUND_NAMES.items():
            stocks_dict = funds_data_config.get(fund_key, {})
            total_sum, total_pct, table_rows = get_fund_data(stocks_dict)
            fixed_key = fund_key if fund_key != "eastspring" else "east"
            
            color_class = "up" if total_sum > 0 else "down" if total_sum < 0 else ""
            
            # 清單列
            home_table_html += f"""
            <tr onclick="document.getElementById('fundSelector').value='{fund_key}'; switchFund('{fund_key}');" style="cursor:pointer; border-bottom:1px solid #eee;">
                <td style="padding:10px;">{fund_name}</td>
                <td style="padding:10px;" class="{color_class}">{total_sum:+.4f}</td>
                <td style="padding:10px;" class="{color_class}">{total_pct:+.2f}%</td>
            </tr>
            """
            
            # 同時更新詳細頁面資訊
            content = re.sub(rf'id="{fixed_key}-sum".*?>.*?</div>', f'id="{fixed_key}-sum" class="total-sum">{total_sum:+.4f}</div>', content)
            content = re.sub(rf'id="{fixed_key}-pct".*?>.*?</div>', f'id="{fixed_key}-pct" class="total-percent">{total_pct:+.2f}%</div>', content)
            content = re.sub(rf'<tbody id="{fixed_key}-details">.*?</tbody>', f'<tbody id="{fixed_key}-details">{table_rows}</tbody>', content, flags=re.DOTALL)

        home_table_html += "</tbody></table>"
        content = re.sub(r'<div class="home-grid" id="home-cards-container">.*?</div>', f'<div class="home-grid" id="home-cards-container">{home_table_html}</div>', content, flags=re.DOTALL)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("【成功】首頁清單模式更新完成！")

if __name__ == "__main__":
    run_monitor()
