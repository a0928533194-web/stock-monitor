import json
import requests
import time

STOCK_MAPPING = {
    # 權值與半導體
    "台積電": "2330", "聯發科": "2454", "鴻海": "2317", "台達電": "2308",
    "聯電": "2303", "日月光投控": "3711", "聯詠": "3034", "瑞昱": "2379",
    "力積電": "6770", "世界": "5347", "中美晶": "5483", "環球晶": "6488",
    "精測": "6510", "晶豪科": "3006", "強茂": "2481", "華邦電": "2344",
    "沛亨": "6291", "聯亞": "3081", "創意": "3443", "世芯-KY": "3661",
    
    # AI 伺服器、散熱、PCB、網通
    "欣興": "3037", "旺矽": "6223", "台光電": "2383", "台燿": "6274",
    "信驊": "5274", "穎崴": "6515", "奇鋐": "3017", "智邦": "2345",
    "景碩": "3189", "南電": "8046", "鴻勁": "7765", "金像電": "2368",
    "健策": "3653", "川湖": "2059", "國巨": "2327", "致茂": "2360",
    "大量": "3167", "台表科": "6278", "光寶科": "2301", "臻鼎-KY": "4958", 
    "臻鼎": "4958", "華星光": "4979", "文曄": "3036", "群聯": "8299", 
    "嘉澤": "3533", "緯創": "3231", "廣達": "2382", "緯穎": "6669", 
    "技嘉": "2376", "華碩": "2357", "M31": "6643", "力旺": "3529", 
    "祥碩": "5269", "高力": "8996", "雙鴻": "3324", "健鼎": "3044", 
    "定穎投控": "3715", "瑞儀": "6176", "英業達": "2356", "仁寶": "2324",
    
    # 其他金融、傳產、生技、ETF 等
    "富邦金": "2881", "國泰金": "2882", "中信金": "2891", "兆豐金": "2886",
    "元大金": "2885", "玉山金": "2884", "台塑": "1301", "南亞": "1303",
    "台化": "1326", "台塑化": "6505", "中鋼": "2002", "統一": "1216",
    "遠東新": "1402", "台泥": "1101", "亞泥": "1102", "長榮": "2603",
    "陽明": "2609", "萬海": "2615", "台灣高鐵": "2633", "中華車": "2204",
    "裕隆": "2201", "和泰車": "2207", "寶成": "9904", "豐泰": "9910"
}

FUNDS_CONFIG = {
    "yuanta_otc": {"name": "元大店頭基金", "stocks": {"旺矽": 8.00, "中美晶": 6.83, "信驊": 6.78, "台積電": 6.32, "台燿": 6.05, "聯電": 5.74, "精測": 4.64, "環球晶": 4.45, "聯亞": 4.21, "沛亨": 3.95}},
    "shinkin_three": {"name": "新光大三通基金", "stocks": {"景碩": 8.79, "欣興": 8.56, "旺矽": 6.81, "世芯-KY": 6.63, "台積電": 6.51, "台達電": 5.44, "力積電": 5.33, "大量": 5.02, "台表科": 4.65, "晶豪科": 4.44}},
    "allianz_taiwan": {"name": "安聯台灣大壩基金", "stocks": {"旺矽": 11.92, "穎崴": 7.63, "台燿": 7.25, "台光電": 6.33, "欣興": 5.88, "信驊": 5.46, "台積電": 5.08, "台達電": 4.98, "智邦": 3.10, "景碩": 3.10}},
    "allianz_tech": {"name": "安聯台灣科技基金", "stocks": {"旺矽": 8.02, "台積電": 7.05, "華邦電": 6.33, "台燿": 6.13, "台光電": 5.75, "穎崴": 5.45, "創意": 4.58, "台達電": 3.93, "奇鋐": 3.69, "信驊": 3.65}},
    "allianz_smart": {"name": "安聯台灣智慧基金", "stocks": {"旺矽": 7.73, "信驊": 7.48, "台光電": 5.99, "台燿": 5.78, "智邦": 4.74, "華邦電": 4.63, "台積電": 4.62, "致茂": 4.47, "台達電": 4.31, "穎崴": 4.10}},
    "fubon_choice": {"name": "富邦首選基金", "stocks": {"欣興": 9.76, "旺矽": 7.88, "聯發科": 7.25, "台光電": 6.77, "台達電": 6.76, "南電": 6.01, "鴻勁": 5.95, "金像電": 4.76, "群聯": 4.64, "聯亞": 4.40}},
    "fubon_select": {"name": "富邦上選基金", "stocks": {"欣興": 7.32, "台光電": 5.03, "穎崴": 4.36, "台積電": 4.26, "聯電": 4.23, "南電": 4.23, "金像電": 4.19, "鴻勁": 4.16, "聯亞": 3.70, "創意": 3.47}},
    "fubon_taiwan": {"name": "富邦新台商基金", "stocks": {"旺矽": 5.71, "欣興": 5.63, "台達電": 5.57, "台光電": 5.42, "聯電": 5.02, "台積電": 4.96, "致茂": 4.16, "創意": 3.95, "嘉澤": 3.87, "聯亞": 3.74}},
    "nomura_prime": {"name": "野村優質基金", "stocks": {"鴻勁": 10.32, "台光電": 8.96, "台達電": 8.79, "川湖": 8.49, "台積電": 8.17, "聯發科": 5.95, "欣興": 5.76, "穎崴": 5.71, "健策": 5.30, "金像電": 5.17}},
    "hanya_tech": {"name": "瀚亞高科技基金", "stocks": {"欣興": 7.86, "台光電": 7.77, "台燿": 7.57, "台積電": 7.10, "聯發科": 6.80, "台達電": 6.71, "奇鋐": 6.47, "智邦": 5.66, "光寶科": 5.08, "強茂": 4.96}},
    "uni_allweather": {"name": "統一全天候基金", "stocks": {"欣興": 9.19, "台光電": 9.04, "台達電": 8.87, "台積電": 7.06, "奇鋐": 6.70, "聯發科": 5.63, "穎崴": 4.11, "致茂": 3.78, "國巨": 3.64, "智邦": 3.56}},
    "uni_prosper": {"name": "統一奔騰基金", "stocks": {"台光電": 9.92, "奇鋐": 7.54, "旺矽": 7.04, "智邦": 7.02, "欣興": 7.02, "台積電": 6.76, "台達電": 6.74, "健策": 4.78, "金像電": 4.67, "國巨": 4.38}},
    "uni_darkhorse": {"name": "統一黑馬基金", "stocks": {"台光電": 7.71, "欣興": 7.56, "台達電": 6.69, "台積電": 6.03, "奇鋐": 5.83, "台燿": 4.93, "金像電": 4.67, "旺矽": 3.72, "智邦": 3.68, "聯發科": 3.38}},
    "nomura_fortune": {"name": "野村鴻運基金", "stocks": {"欣興": 8.21, "台光電": 7.50, "川湖": 6.12, "台達電": 6.06, "台積電": 5.58, "聯發科": 5.54, "鴻勁": 5.29, "聯亞": 4.29, "旺矽": 3.96, "健策": 3.57}},
    "nomura_growth": {"name": "野村成長基金", "stocks": {"台光電": 7.42, "欣興": 7.35, "聯發科": 7.17, "台達電": 5.84, "台積電": 5.43, "旺矽": 4.90, "金像電": 4.78, "鴻勁": 4.31, "奇鋐": 3.76, "穎崴": 3.69}},
    "nomura_hightech": {"name": "野村高科技基金", "stocks": {"聯發科": 8.15, "南電": 7.57, "聯亞": 7.21, "臻鼎-KY": 6.51, "欣興": 5.90, "台積電": 5.70, "景碩": 5.12, "華星光": 5.11, "創意": 4.95, "文曄": 4.90}},
    "nomura_etech": {"name": "野村 e 科技基金", "stocks": {"聯發科": 8.09, "南電": 7.58, "聯亞": 6.70, "欣興": 6.15, "景碩": 5.61, "臻鼎-KY": 5.48, "文曄": 5.09, "創意": 5.05, "華星光": 5.04, "台積電": 3.83}}
}

def fetch_stock_data():
    price_cache = {}
    print("開始抓取最新股價...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    session = requests.Session()
    otc_list = {"台燿", "環球晶", "聯亞", "沛亨", "旺矽", "中美晶", "信驊", "精測", "世界", "華星光", "M31", "世芯-KY"}
    
    for name, code in STOCK_MAPPING.items():
        success = False
        suffixes = [".TWO", ".TW"] if name in otc_list else [".TW", ".TWO"]
        for suf in suffixes:
            if success: break
            ticker = code + suf
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=10d&interval=1d"
            try:
                res = session.get(url, headers=headers, timeout=4)
                if res.status_code == 200:
                    data = res.json()
                    result = data.get('chart', {}).get('result')
                    if result:
                        quotes = result[0]['indicators']['quote'][0]['close']
                        valid_quotes = [q for q in quotes if q is not None]
                        if len(valid_quotes) >= 2:
                            price_cache[name] = {
                                "yesterday": valid_quotes[-2],
                                "current": valid_quotes[-1],
                                "success": True
                            }
                            success = True
                            break
            except Exception:
                pass
        if not success:
            price_cache[name] = {"yesterday": 0, "current": 0, "success": False}
        time.sleep(0.05)
    print("股價抓取完畢！")
    return price_cache

def run_monitor():
    stock_prices = fetch_stock_data()
    options_html = ""
    
    for i, (key, info) in enumerate(FUNDS_CONFIG.items()):
        options_html += f'<option value="{key}">{info["name"]}</option>'

    all_prices_json = json.dumps(stock_prices)
    default_config_json = json.dumps(FUNDS_CONFIG)

    html_template = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>基金監測系統</title>
    <style>
        :root {{ --up: #ff4d4f; --down: #52c41a; }}
        body {{ font-family: sans-serif; background: #f0f2f5; padding: 10px; margin: 0; }}
        .container {{ max-width: 750px; margin: auto; background: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .fund-section {{ display: none; }} 
        .fund-section.active {{ display: block; }}
        .dashboard {{ text-align: center; background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 15px 0; }}
        .total-sum {{ font-size: 24px; font-weight: bold; color: #333; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 11px; }}
        th {{ color: #888; padding: 8px 2px; border-bottom: 2px solid #ddd; text-align: center; }}
        td {{ padding: 6px 2px; text-align: center; border-bottom: 1px solid #f9f9f9; }}
        .up {{ color: var(--up); font-weight: bold; }} 
        .down {{ color: var(--down); font-weight: bold; }}
        select {{ width: 100%; padding: 12px; font-size: 16px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px; }}
        .update-box {{ text-align:center; margin: 20px 0; padding: 15px; border-top: 1px solid #eee; }}
    </style>
</head>
<body>
<div class="container">
    <div style="text-align:center; font-size: 12px; color: #666; margin-bottom: 5px;">🕒 系統就緒 (已啟用自動記憶功能)</div>
    
    <select id="fundSelect" onchange="switchFund(this.value)">{options_html}</select>
    
    <div id="sections-container"></div>
    
    <div class="update-box">
        <button type="button" onclick="resetConfig()" style="background-color: #ff4d4f; color: white; border: none; padding: 8px 12px; border-radius: 5px; cursor: pointer; margin-bottom: 10px; font-size: 12px;">🔄 恢復預設值</button>
        <br>
        <button id="updateBtn" onclick="triggerUpdate()" style="background-color: #1890ff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">更新 GitHub 動作</button>
        <button type="button" onclick="location.reload()" style="background-color: #8c8c8c; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; margin-left: 5px;">重新整理</button>
        <p id="status" style="font-size: 12px; color: #666; margin-top: 10px;"></p>
    </div>
</div>

<script>
const globalPrices = {all_prices_json};
const defaultConfig = {default_config_json};

function getConfig() {{
    const saved = localStorage.getItem('user_funds_config');
    if (saved) {{
        try {{ return JSON.parse(saved); }} catch(e) {{}}
    }}
    return defaultConfig;
}}

function saveConfig(config) {{
    localStorage.setItem('user_funds_config', JSON.stringify(config));
}}

function renderApp() {{
    const config = getConfig();
    const container = document.getElementById('sections-container');
    container.innerHTML = '';
    
    const activeKey = document.getElementById('fundSelect').value || Object.keys(config)[0];
    
    for (const [key, info] of Object.entries(config)) {{
        const active = (key === activeKey) ? "active" : "";
        
        let table_rows = "";
        let total_contribution = 0;
        let total_pct = 0;
        
        if (info && info.stocks) {{
            for (const [name, weight] of Object.entries(info.stocks)) {{
                let pYester = 0, pCurr = 0, diff = 0, pctChange = 0, contribPct = 0, contribution = 0;
                if (globalPrices[name] && globalPrices[name].success) {{
                    pYester = globalPrices[name].yesterday;
                    pCurr = globalPrices[name].current;
                    diff = pCurr - pYester;
                    pctChange = pYester !== 0 ? (diff / pYester) * 100 : 0;
                    contribPct = pctChange * (weight / 100);
                    contribution = diff * (weight / 100);
                    
                    total_pct += contribPct;
                    total_contribution += contribution;
                }}
                
                const color_class = diff > 0 ? "up" : (diff < 0 ? "down" : "");
                const sign_pct = pctChange >= 0 ? '+' : '';
                const sign_contrib_pct = contribPct >= 0 ? '+' : '';
                const sign_contrib = contribution >= 0 ? '+' : '';
                
                table_rows += `<tr>
                    <td><input type="text" class="edit-name" value="${{name}}" style="width:90%; text-align:center; border:1px solid #ddd; border-radius:3px; background:transparent;" oninput="updateData()"></td>
                    <td><input type="number" step="0.01" class="edit-weight" value="${{weight}}" style="width:80%; text-align:center; border:1px solid #ddd; border-radius:3px;" oninput="updateData()">%</td>
                    <td class="col-yesterday">${{pYester.toFixed(2)}}</td>
                    <td class="col-current ${{color_class}}">${{pCurr.toFixed(2)}}</td>
                    <td class="col-pct ${{color_class}}"><strong>${{sign_pct}}${{pctChange.toFixed(2)}}%</strong></td>
                    <td class="col-contrib-pct ${{color_class}}">${{sign_contrib_pct}}${{contribPct.toFixed(2)}}%</td>
                    <td class="col-contrib ${{color_class}}">${{sign_contrib}}${{contribution.toFixed(4)}}</td>
                    <td><button type="button" onclick="this.closest('tr').remove(); updateData();" style="background:#ff4d4f; color:white; border:none; border-radius:3px; cursor:pointer; padding:2px 6px;">X</button></td>
                </tr>`;
            }}
        }}

        const sum_str = (total_contribution >= 0 ? '+' : '') + total_contribution.toFixed(4);
        const pct_str = (total_pct >= 0 ? '+' : '') + total_pct.toFixed(2) + '%';
        const fundName = info ? info.name : key;

        const sectionHtml = `
        <div id="sector-${{key}}" class="fund-section ${{active}}" data-key="${{key}}">
            <div class="dashboard">
                <div class="dashboard-title">${{fundName}} - 今日預估總貢獻</div>
                <div class="total-sum" id="sum-${{key}}">${{sum_str}}</div>
                <div class="dashboard-title">今日預估總貢獻 %</div>
                <div class="total-percent" id="pct-${{key}}" style="font-size: 18px; font-weight: bold; color: #333;">${{pct_str}}</div>
            </div>
            
            <div style="margin-bottom: 8px;">
                <button type="button" onclick="addStockRow('${{key}}')" style="background: #52c41a; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 12px;">＋ 新增一檔股票</button>
            </div>

            <table style="width:100%; table-layout:fixed;">
                <thead>
                    <tr>
                        <th style="width:18%">成分股</th>
                        <th style="width:14%">權重</th>
                        <th style="width:12%">昨收</th>
                        <th style="width:12%">現價</th>
                        <th style="width:14%">漲跌幅%</th>
                        <th style="width:15%">貢獻%</th>
                        <th style="width:15%">貢獻度</th>
                        <th style="width:8%"></th>
                    </tr>
                </thead>
                <tbody id="tbody-${{key}}">
                    ${{table_rows}}
                </tbody>
            </table>
        </div>`;
        container.insertAdjacentHTML('beforeend', sectionHtml);
    }}
}

function switchFund(key) {{
    document.querySelectorAll('.fund-section').forEach(s => s.classList.remove('active'));
    const target = document.getElementById('sector-' + key);
    if (target) target.classList.add('active');
}}

function addStockRow(key) {{
    const tbody = document.getElementById('tbody-' + key);
    const tr = document.createElement('tr');
    tr.innerHTML = `
        <td><input type="text" class="edit-name" value="" placeholder="股票名稱" style="width:90%; text-align:center; border:1px solid #ddd; border-radius:3px;" oninput="updateData()"></td>
        <td><input type="number" step="0.01" class="edit-weight" value="0" style="width:80%; text-align:center; border:1px solid #ddd; border-radius:3px;" oninput="updateData()">%</td>
        <td class="col-yesterday">0.00</td>
        <td class="col-current">0.00</td>
        <td class="col-pct"><strong>0.00%</strong></td>
        <td class="col-contrib-pct">0.00%</td>
        <td class="col-contrib">0.0000</td>
        <td><button type="button" onclick="this.closest('tr').remove(); updateData();" style="background:#ff4d4f; color:white; border:none; border-radius:3px; cursor:pointer; padding:2px 6px;">X</button></td>
    `;
    tbody.appendChild(tr);
    updateData();
}}

function updateData() {{
    const config = getConfig();
    
    document.querySelectorAll('.fund-section').forEach(section => {{
        const key = section.getAttribute('data-key');
        const rows = section.querySelectorAll('tbody tr');
        
        let newStocks = {{}};
        let totalSum = 0;
        let totalPct = 0;
        
        rows.forEach(row => {{
            const nameInput = row.querySelector('.edit-name');
            const weightInput = row.querySelector('.edit-weight');
            const name = nameInput ? nameInput.value.trim() : '';
            const weight = parseFloat(weightInput ? weightInput.value : 0) || 0;
            
            if (name) {{
                newStocks[name] = weight;
            }}
            
            const yCell = row.querySelector('.col-yesterday');
            const cCell = row.querySelector('.col-current');
            const pctCell = row.querySelector('.col-pct');
            const cpctCell = row.querySelector('.col-contrib-pct');
            const contribCell = row.querySelector('.col-contrib');
            
            let pYester = 0, pCurr = 0;
            if (name && globalPrices[name] && globalPrices[name].success) {{
                pYester = globalPrices[name].yesterday;
                pCurr = globalPrices[name].current;
                yCell.innerText = pYester.toFixed(2);
                cCell.innerText = pCurr.toFixed(2);
            }} else {{
                yCell.innerText = "0.00";
                cCell.innerText = "0.00";
            }}
            
            const diff = pCurr - pYester;
            const pctChange = pYester !== 0 ? (diff / pYester) * 100 : 0;
            const contribPct = pctChange * (weight / 100);
            const contribution = diff * (weight / 100);
            
            if (pYester !== 0) {{
                totalSum += contribution;
                totalPct += contribPct;
            }}
            
            const colorClass = diff > 0 ? "up" : (diff < 0 ? "down" : "");
            const signPct = pctChange >= 0 ? '+' : '';
            const signCPct = contribPct >= 0 ? '+' : '';
            const signContrib = contribution >= 0 ? '+' : '';
            
            cCell.className = "col-current " + colorClass;
            pctCell.className = "col-pct " + colorClass;
            cpctCell.className = "col-contrib-pct " + colorClass;
            contribCell.className = "col-contrib " + colorClass;
            
            pctCell.innerHTML = `<strong>${{signPct}}${{pctChange.toFixed(2)}}%</strong>`;
            cpctCell.innerText = `${{signCPct}}${{contribPct.toFixed(2)}}%`;
            contribCell.innerText = `${{signContrib}}${{contribution.toFixed(4)}}`;
        }});
        
        if (config[key]) {{
            config[key].stocks = newStocks;
        }}
        
        const sumEl = document.getElementById('sum-' + key);
        const pctEl = document.getElementById('pct-' + key);
        if (sumEl) sumEl.innerText = (totalSum >= 0 ? '+' : '') + totalSum.toFixed(4);
        if (pctEl) pctEl.innerText = (totalPct >= 0 ? '+' : '') + totalPct.toFixed(2) + '%';
    }});
    
    saveConfig(config);
}}

function resetConfig() {{
    if (confirm("確定要恢復為預設的基金與權重嗎？")) {{
        localStorage.removeItem('user_funds_config');
        location.reload();
    }}
}}

async function triggerUpdate() {{
    const GITHUB_OWNER = "a0928533194-web"; 
    const REPO_NAME = "stock-monitor";
    const WORKFLOW_FILE = "run.yml"; 
    const userToken = prompt("請輸入您的 GitHub Token:");
    if (!userToken) return;
    document.getElementById('status').innerText = "正在發送請求...";
    const response = await fetch(`https://api.github.com/repos/${{GITHUB_OWNER}}/${{REPO_NAME}}/actions/workflows/${{WORKFLOW_FILE}}/dispatches`, {{
        method: "POST",
        headers: {{"Authorization": "token " + userToken, "Accept": "application/vnd.github.v3+json"}},
        body: JSON.stringify({{"ref": "main"}})
    }});
    if (response.ok) {{ document.getElementById('status').innerText = "✅ 請求已送出！"; }}
    else {{ document.getElementById('status').innerText = "❌ 請求失敗"; }}
}}

renderApp();
</script>
</body>
</html>'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("【更新成功】index.html 已重新生成！")

if __name__ == "__main__":
    run_monitor()
