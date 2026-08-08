import json

STOCK_MAPPING = {
    "台積電": "2330.TW", "聯發科": "2454.TW", "鴻海": "2317.TW", "台達電": "2308.TW",
    "聯電": "2303.TW", "欣興": "3037.TW", "旺矽": "6223.TWO", "台光電": "2383.TW",
    "台燿": "6274.TW", "信驊": "5274.TWO", "穎崴": "6515.TW", "奇鋐": "3017.TW",
    "智邦": "2345.TW", "景碩": "3189.TW", "南電": "8046.TW", "鴻勁": "7765.TW",
    "金像電": "2368.TW", "聯亞": "3081.TWO", "創意": "3443.TW", "健策": "3653.TW",
    "川湖": "2059.TW", "國巨": "2327.TW", "華邦電": "2344.TW", "致茂": "2360.TW",
    "中美晶": "5483.TWO", "精測": "6510.TWO", "環球晶": "6488.TW", "沛亨": "6291.TW",
    "世芯-KY": "3661.TW", "大量": "3167.TW", "台表科": "6278.TW", "晶豪科": "3006.TW",
    "光寶科": "2301.TW", "強茂": "2481.TW", "臻鼎-KY": "4958.TW", "華星光": "4979.TWO",
    "文曄": "3036.TW", "群聯": "8299.TW", "嘉澤": "3533.TW"
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

def run_monitor():
    funds_json = json.dumps(FUNDS_CONFIG, ensure_ascii=False)
    mapping_json = json.dumps(STOCK_MAPPING, ensure_ascii=False)
    options_html, sections_html = "", ""
    
    for i, (key, info) in enumerate(FUNDS_CONFIG.items()):
        active = "active" if i == 0 else ""
        options_html += f'<option value="{key}">{info["name"]}</option>'
        
        editor_rows = ""
        for name, weight in info["stocks"].items():
            editor_rows += f'''
            <div class="stock-input-row" style="display: flex; gap: 8px; margin-bottom: 5px;">
                <input type="text" class="edit-name" value="{name}" placeholder="股票名稱" style="width: 55%;">
                <input type="number" step="0.01" class="edit-weight" value="{weight}" placeholder="權重%" style="width: 35%;">
                <button type="button" onclick="this.parentElement.remove()" style="background:#ff4d4f; color:white; border:none; border-radius:3px; cursor:pointer; width:10%;">X</button>
            </div>'''
            
        sections_html += f'''
        <div id="sector-{key}" class="fund-section {active}">
            <div class="dashboard">
                <div class="dashboard-title">{info["name"]} - 今日預估總貢獻</div>
                <div class="total-sum" id="sum-{key}">0.0000</div>
                <div class="dashboard-title">今日預估總貢獻 %</div>
                <div class="total-percent" id="pct-{key}" style="font-size: 18px; font-weight: bold; color: #333;">0.00%</div>
            </div>
            
            <div style="text-align: right; margin-bottom: 8px;">
                <button type="button" onclick="toggleEditor('{key}')" style="background: #fa8c16; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 11px;">⚙️ 編輯此基金持股</button>
            </div>
            
            <div id="editor-{key}" style="display: none; background: #fffbe6; padding: 10px; border-radius: 8px; border: 1px solid #ffe58f; margin-bottom: 10px;">
                <div style="font-weight: bold; font-size: 12px; margin-bottom: 5px;">修改成分股與權重（系統會自動對應代號）：</div>
                <div id="container-{key}">
                    {editor_rows}
                </div>
                <button type="button" onclick="addStockRow('{key}')" style="background: #52c41a; color: white; border: none; padding: 4px 8px; border-radius: 3px; cursor: pointer; font-size: 11px; margin-top: 5px;">＋ 新增一檔股票</button>
                <button type="button" onclick="saveAndCalculate('{key}')" style="background: #1890ff; color: white; border: none; padding: 4px 12px; border-radius: 3px; cursor: pointer; font-size: 11px; margin-top: 5px; float: right;">儲存並重新計算</button>
            </div>

            <table style="width:100%; table-layout:fixed;">
                <thead>
                    <tr>
                        <th style="width:20%">成分股</th>
                        <th style="width:12%">權重</th>
                        <th style="width:12%">昨收</th>
                        <th style="width:12%">現價</th>
                        <th style="width:14%">漲跌幅%</th>
                        <th style="width:15%">貢獻%</th>
                        <th style="width:15%">貢獻度</th>
                    </tr>
                </thead>
                <tbody id="tbody-{key}">
                    <tr><td colspan="7" style="color: #888;">載入中...</td></tr>
                </tbody>
            </table>
        </div>'''

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>基金監測系統</title>
<style>
    :root {{ --up: #ff4d4f; --down: #52c41a; }}
    body {{ font-family: sans-serif; background: #f0f2f5; padding: 10px; margin: 0; }}
    .container {{ max-width: 700px; margin: auto; background: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
    .fund-section {{ display: none; }} .fund-section.active {{ display: block; }}
    .dashboard {{ text-align: center; background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 15px 0; }}
    .total-sum {{ font-size: 24px; font-weight: bold; color: #333; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 11px; }}
    th {{ color: #888; padding: 8px 2px; border-bottom: 2px solid #ddd; text-align: center; }}
    td {{ padding: 8px 2px; text-align: center; border-bottom: 1px solid #f9f9f9; }}
    .up {{ color: var(--up); font-weight: bold; }} .down {{ color: var(--down); font-weight: bold; }}
    select {{ width: 100%; padding: 12px; font-size: 16px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px; }}
    .update-box {{ text-align:center; margin: 20px 0; padding: 15px; border-top: 1px solid #eee; }}
</style></head>
<body>
<div class="container">
    <div style="text-align:center; font-size: 12px; color: #666; margin-bottom: 10px;">🕒 系統就緒 (僅需輸入名稱與權重)</div>
    <select onchange="switchFund(this.value)">{options_html}</select>
    {sections_html}
    <div class="update-box">
        <button id="updateBtn" onclick="triggerUpdate()" style="background-color: #1890ff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">更新 GitHub 動作</button>
        <button type="button" onclick="resetSettings()" style="background-color: #8c8c8c; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; margin-left: 5px;">重置為預設設定</button>
        <p id="status" style="font-size: 12px; color: #666; margin-top: 10px;"></p>
    </div>
</div>
<script>
const stockMapping = {mapping_json};
let savedFundsData = localStorage.getItem('myCustomFundsDataNameOnly');
let fundsData = savedFundsData ? JSON.parse(savedFundsData) : {funds_json};

function toggleEditor(key) {{
    const editor = document.getElementById('editor-' + key);
    editor.style.display = editor.style.display === 'none' ? 'block' : 'none';
}}

function addStockRow(key) {{
    const container = document.getElementById('container-' + key);
    const div = document.createElement('div');
    div.className = 'stock-input-row';
    div.style.cssText = 'display: flex; gap: 8px; margin-bottom: 5px;';
    div.innerHTML = `
        <input type="text" class="edit-name" placeholder="股票名稱" style="width: 55%;">
        <input type="number" step="0.01" class="edit-weight" placeholder="權重%" style="width: 35%;">
        <button type="button" onclick="this.parentElement.remove()" style="background:#ff4d4f; color:white; border:none; border-radius:3px; cursor:pointer; width:10%;">X</button>
    `;
    container.appendChild(div);
}}

function saveAndCalculate(key) {{
    const container = document.getElementById('container-' + key);
    const rows = container.getElementsByClassName('stock-input-row');
    let newStocks = {{}};
    
    for (let r of rows) {{
        let name = r.querySelector('.edit-name').value.trim();
        let weight = parseFloat(r.querySelector('.edit-weight').value) || 0;
        if (name) {{
            newStocks[name] = weight;
        }}
    }}
    
    fundsData[key].stocks = newStocks;
    localStorage.setItem('myCustomFundsDataNameOnly', JSON.stringify(fundsData));
    toggleEditor(key);
    fetchFundData(key);
}}

function resetSettings() {{
    if (confirm("確定要清除自訂資料並重置回原始預設設定嗎？")) {{
        localStorage.removeItem('myCustomFundsDataNameOnly');
        location.reload();
    }}
}}

function switchFund(key) {{
    document.querySelectorAll('.fund-section').forEach(s => s.classList.remove('active'));
    document.getElementById('sector-' + key).classList.add('active');
    fetchFundData(key);
}}

async function fetchFundData(key) {{
    const stocks = fundsData[key].stocks;
    const tbody = document.getElementById('tbody-' + key);
    tbody.innerHTML = `<tr><td colspan="7" style="color: #1890ff;">正在對應代號並抓取股價數據...</td></tr>`;
    
    let totalContribution = 0;
    let totalPct = 0;
    let tableRows = "";
    
    for (let name in stocks) {{
        let weight = stocks[name];
        let tickerBase = stockMapping[name];
        
        if (!tickerBase) {{
            tableRows += `<tr>
                <td>${{name}} (未知)</td>
                <td>${{weight}}%</td>
                <td colspan="5" style="color: #ff4d4f;">找不到對應的股票代號，請確認名稱是否正確</td>
            </tr>`;
            continue;
        }}
        
        let success = false;
        let pYester = 0, pCurr = 0, diff = 0;
        
        try {{
            let url = `https://query1.finance.yahoo.com/v8/finance/chart/${{tickerBase}}?range=5d&interval=1d`;
            let res = await fetch(`https://api.allorigins.win/get?url=` + encodeURIComponent(url));
            let json = await res.json();
            let data = JSON.parse(json.contents);
            let quotes = data.chart.result[0].indicators.quote[0].close;
            let validQuotes = quotes.filter(q => q !== null);
            
            if (validQuotes.length >= 2) {{
                pYester = validQuotes[validQuotes.length - 2];
                pCurr = validQuotes[validQuotes.length - 1];
                diff = pCurr - pYester;
                success = true;
            }}
        }} catch (e) {{}}
        
        let pctChange = pYester !== 0 ? (diff / pYester) * 100 : 0;
        let contribPct = pctChange * (weight / 100);
        let contribution = diff * (weight / 100);
        
        totalPct += contribPct;
        totalContribution += contribution;
        
        let colorClass = diff > 0 ? "up" : (diff < 0 ? "down" : "");
        
        tableRows += `<tr>
            <td>${{name}}</td>
            <td>${{weight}}%</td>
            <td>${{success ? pYester.toFixed(2) : 'N/A'}}</td>
            <td class="${{colorClass}}">${{success ? pCurr.toFixed(2) : 'N/A'}}</td>
            <td class="${{colorClass}}"><strong>${{pctChange >= 0 ? '+' : ''}}${{pctChange.toFixed(2)}}%</strong></td>
            <td class="${{colorClass}}">${{contribPct >= 0 ? '+' : ''}}${{contribPct.toFixed(2)}}%</td>
            <td class="${{colorClass}}">${{contribution >= 0 ? '+' : ''}}${{contribution.toFixed(4)}}</td>
        </tr>`;
    }}
    
    tbody.innerHTML = tableRows;
    document.getElementById('sum-' + key).innerText = (totalContribution >= 0 ? '+' : '') + totalContribution.toFixed(4);
    document.getElementById('pct-' + key).innerText = (totalPct >= 0 ? '+' : '') + totalPct.toFixed(2) + '%';
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

window.onload = function() {{
    let firstKey = Object.keys(fundsData)[0];
    fetchFundData(firstKey);
}};
</script>
</body></html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("【更新成功】index.html 已生成")

if __name__ == "__main__":
    run_monitor()
