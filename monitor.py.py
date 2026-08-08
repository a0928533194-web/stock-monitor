import json

# 完整基金數據設定
FUNDS_CONFIG = {
    "yuanta_otc": {"name": "元大店頭基金", "stocks": {"旺矽": ("6223", 8.00), "中美晶": ("5483", 6.83), "信驊": ("5274", 6.78), "台積電": ("2330", 6.32), "台燿": ("6274", 6.05), "聯電": ("2303", 5.74), "精測": ("6510", 4.64), "環球晶": ("6488", 4.45), "聯亞": ("3081", 4.21), "沛亨": ("6291", 3.95)}},
    "shinkin_three": {"name": "新光大三通基金", "stocks": {"景碩": ("3189", 8.79), "欣興": ("3037", 8.56), "旺矽": ("6223", 6.81), "世芯-KY": ("3661", 6.63), "台積電": ("2330", 6.51), "台達電": ("2308", 5.44), "力積電": ("6770", 5.33), "大量": ("3167", 5.02), "台表科": ("6278", 4.65), "晶豪科": ("3006", 4.44)}},
    "allianz_taiwan": {"name": "安聯台灣大壩基金", "stocks": {"旺矽": ("6223", 11.92), "穎崴": ("6515", 7.63), "台燿": ("6274", 7.25), "台光電": ("2383", 6.33), "欣興": ("3037", 5.88), "信驊": ("5274", 5.46), "台積電": ("2330", 5.08), "台達電": ("2308", 4.98), "智邦": ("2345", 3.10), "景碩": ("3189", 3.10)}},
    "allianz_tech": {"name": "安聯台灣科技基金", "stocks": {"旺矽": ("6223", 8.02), "台積電": ("2330", 7.05), "華邦電": ("2344", 6.33), "台燿": ("6274", 6.13), "台光電": ("2383", 5.75), "穎崴": ("6515", 5.45), "創意": ("3443", 4.58), "台達電": ("2308", 3.93), "奇鋐": ("3017", 3.69), "信驊": ("5274", 3.65)}},
    "allianz_smart": {"name": "安聯台灣智慧基金", "stocks": {"旺矽": ("6223", 7.73), "信驊": ("5274", 7.48), "台光電": ("2383", 5.99), "台燿": ("6274", 5.78), "智邦": ("2345", 4.74), "華邦電": ("2344", 4.63), "台積電": ("2330", 4.62), "致茂": ("2360", 4.47), "台達電": ("2308", 4.31), "穎崴": ("6515", 4.10)}},
    "fubon_choice": {"name": "富邦首選基金", "stocks": {"欣興": ("3037", 9.76), "旺矽": ("6223", 7.88), "聯發科": ("2454", 7.25), "台光電": ("2383", 6.77), "台達電": ("2308", 6.76), "南電": ("8046", 6.01), "鴻勁": ("7765", 5.95), "金像電": ("2368", 4.76), "群聯": ("8299", 4.64), "聯亞": ("3081", 4.40)}},
    "fubon_select": {"name": "富邦上選基金", "stocks": {"欣興": ("3037", 7.32), "台光電": ("2383", 5.03), "穎崴": ("6515", 4.36), "台積電": ("2330", 4.26), "聯電": ("2303", 4.23), "南電": ("8046", 4.23), "金像電": ("2368", 4.19), "鴻勁": ("7765", 4.16), "聯亞": ("3081", 3.70), "創意": ("3443", 3.47)}},
    "fubon_taiwan": {"name": "富邦新台商基金", "stocks": {"旺矽": ("6223", 5.71), "欣興": ("3037", 5.63), "台達電": ("2308", 5.57), "台光電": ("2383", 5.42), "聯電": ("2303", 5.02), "台積電": ("2330", 4.96), "致茂": ("2360", 4.16), "創意": ("3443", 3.95), "嘉澤": ("3533", 3.87), "聯亞": ("3081", 3.74)}},
    "nomura_prime": {"name": "野村優質基金", "stocks": {"鴻勁": ("7765", 10.32), "台光電": ("2383", 8.96), "台達電": ("2308", 8.79), "川湖": ("2059", 8.49), "台積電": ("2330", 8.17), "聯發科": ("2454", 5.95), "欣興": ("3037", 5.76), "穎崴": ("6515", 5.71), "健策": ("3653", 5.30), "金像電": ("2368", 5.17)}},
    "hanya_tech": {"name": "瀚亞高科技基金", "stocks": {"欣興": ("3037", 7.86), "台光電": ("2383", 7.77), "台燿": ("6274", 7.57), "台積電": ("2330", 7.10), "聯發科": ("2454", 6.80), "台達電": ("2308", 6.71), "奇鋐": ("3017", 6.47), "智邦": ("2345", 5.66), "光寶科": ("2301", 5.08), "強茂": ("2481", 4.96)}},
    "uni_allweather": {"name": "統一全天候基金", "stocks": {"欣興": ("3037", 9.19), "台光電": ("2383", 9.04), "台達電": ("2308", 8.87), "台積電": ("2330", 7.06), "奇鋐": ("3017", 6.70), "聯發科": ("2454", 5.63), "穎崴": ("6515", 4.11), "致茂": ("2360", 3.78), "國巨": ("2327", 3.64), "智邦": ("2345", 3.56)}},
    "uni_prosper": {"name": "統一奔騰基金", "stocks": {"台光電": ("2383", 9.92), "奇鋐": ("3017", 7.54), "旺矽": ("6223", 7.04), "智邦": ("2345", 7.02), "欣興": ("3037", 7.02), "台積電": ("2330", 6.76), "台達電": ("2308", 6.74), "健策": ("3653", 4.78), "金像電": ("2368", 4.67), "國巨": ("2327", 4.38)}},
    "uni_darkhorse": {"name": "統一黑馬基金", "stocks": {"台光電": ("2383", 7.71), "欣興": ("3037", 7.56), "台達電": ("2308", 6.69), "台積電": ("2330", 6.03), "奇鋐": ("3017", 5.83), "台燿": ("6274", 4.93), "金像電": ("2368", 4.67), "旺矽": ("6223", 3.72), "智邦": ("2345", 3.68), "聯發科": ("2454", 3.38)}},
    "nomura_fortune": {"name": "野村鴻運基金", "stocks": {"欣興": ("3037", 8.21), "台光電": ("2383", 7.50), "川湖": ("2059", 6.12), "台達電": ("2308", 6.06), "台積電": ("2330", 5.58), "聯發科": ("2454", 5.54), "鴻勁": ("7765", 5.29), "聯亞": ("3081", 4.29), "旺矽": ("6223", 3.96), "健策": ("3653", 3.57)}},
    "nomura_growth": {"name": "野村成長基金", "stocks": {"台光電": ("2383", 7.42), "欣興": ("3037", 7.35), "聯發科": ("2454", 7.17), "台達電": ("2308", 5.84), "台積電": ("2330", 5.43), "旺矽": ("6223", 4.90), "金像電": ("2368", 4.78), "鴻勁": ("7765", 4.31), "奇鋐": ("3017", 3.76), "穎崴": ("6515", 3.69)}},
    "nomura_hightech": {"name": "野村高科技基金", "stocks": {"聯發科": ("2454", 8.15), "南電": ("8046", 7.57), "聯亞": ("3081", 7.21), "臻鼎-KY": ("4958", 6.51), "欣興": ("3037", 5.90), "台積電": ("2330", 5.70), "景碩": ("3189", 5.12), "華星光": ("4979", 5.11), "創意": ("3443", 4.95), "文曄": ("3036", 4.90)}},
    "nomura_etech": {"name": "野村 e 科技基金", "stocks": {"聯發科": ("2454", 8.09), "南電": ("8046", 7.58), "聯亞": ("3081", 6.70), "欣興": ("3037", 6.15), "景碩": ("3189", 5.61), "臻鼎-KY": ("4958", 5.48), "文曄": ("3036", 5.09), "創意": ("3443", 5.05), "華星光": ("4979", 5.04), "台積電": ("2330", 3.83)}}
}

def run_monitor():
    funds_json = json.dumps(FUNDS_CONFIG, ensure_ascii=False)
    options_html, sections_html = "", ""
    
    for i, (key, info) in enumerate(FUNDS_CONFIG.items()):
        active = "active" if i == 0 else ""
        options_html += f'<option value="{key}">{info["name"]}</option>'
        
        editor_rows = ""
        for name, (ticker, weight) in info["stocks"].items():
            editor_rows += f'''
            <div class="stock-input-row" style="display: flex; gap: 5px; margin-bottom: 5px;">
                <input type="text" class="edit-name" value="{name}" placeholder="名稱" style="width: 25%;">
                <input type="text" class="edit-ticker" value="{ticker}" placeholder="代號" style="width: 35%;">
                <input type="number" step="0.01" class="edit-weight" value="{weight}" placeholder="權重%" style="width: 30%;">
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
                <div style="font-weight: bold; font-size: 12px; margin-bottom: 5px;">修改成分股與權重：</div>
                <div id="container-{key}">
                    {editor_rows}
                </div>
                <button type="button" onclick="addStockRow('{key}')" style="background: #52c41a; color: white; border: none; padding: 4px 8px; border-radius: 3px; cursor: pointer; font-size: 11px; margin-top: 5px;">＋ 新增一檔股票</button>
                <button type="button" onclick="saveAndCalculate('{key}')" style="background: #1890ff; color: white; border: none; padding: 4px 12px; border-radius: 3px; cursor: pointer; font-size: 11px; margin-top: 5px; float: right;">儲存並重新計算</button>
            </div>

            <table style="width:100%; table-layout:fixed;">
                <thead>
                    <tr>
                        <th style="width:15%">成分股</th>
                        <th style="width:10%">權重</th>
                        <th style="width:12%">昨收</th>
                        <th style="width:12%">現價</th>
                        <th style="width:17%">漲跌幅%</th>
                        <th style="width:17%">貢獻%</th>
                        <th style="width:17%">貢獻度</th>
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
    <div style="text-align:center; font-size: 12px; color: #666; margin-bottom: 10px;">🕒 系統就緒 (支援前端自訂持股)</div>
    <select onchange="switchFund(this.value)">{options_html}</select>
    {sections_html}
    <div class="update-box">
        <button id="updateBtn" onclick="triggerUpdate()" style="background-color: #1890ff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">更新 GitHub 動作</button>
        <p id="status" style="font-size: 12px; color: #666; margin-top: 10px;"></p>
    </div>
</div>
<script>
let fundsData = {funds_json};

function toggleEditor(key) {{
    const editor = document.getElementById('editor-' + key);
    editor.style.display = editor.style.display === 'none' ? 'block' : 'none';
}}

function addStockRow(key) {{
    const container = document.getElementById('container-' + key);
    const div = document.createElement('div');
    div.className = 'stock-input-row';
    div.style.cssText = 'display: flex; gap: 5px; margin-bottom: 5px;';
    div.innerHTML = `
        <input type="text" class="edit-name" placeholder="名稱" style="width: 25%;">
        <input type="text" class="edit-ticker" placeholder="代號" style="width: 35%;">
        <input type="number" step="0.01" class="edit-weight" placeholder="權重%" style="width: 30%;">
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
        let ticker = r.querySelector('.edit-ticker').value.trim();
        let weight = parseFloat(r.querySelector('.edit-weight').value) || 0;
        if (name && ticker) {{
            newStocks[name] = [ticker, weight];
        }}
    }}
    
    fundsData[key].stocks = newStocks;
    toggleEditor(key);
    fetchFundData(key);
}}

function switchFund(key) {{
    document.querySelectorAll('.fund-section').forEach(s => s.classList.remove('active'));
    document.getElementById('sector-' + key).classList.add('active');
    fetchFundData(key);
}}

async function fetchFundData(key) {{
    const stocks = fundsData[key].stocks;
    const tbody = document.getElementById('tbody-' + key);
    tbody.innerHTML = `<tr><td colspan="7" style="color: #1890ff;">正在抓取最新股價數據...</td></tr>`;
    
    let totalContribution = 0;
    let totalPct = 0;
    let tableRows = "";
    
    for (let name in stocks) {{
        let [tickerBase, weight] = stocks[name];
        let success = false;
        let pYester = 0, pCurr = 0, diff = 0;
        
        const suffixes = ["", ".TW", ".TWO"];
        for (let suffix of suffixes) {{
            try {{
                let url = `https://query1.finance.yahoo.com/v8/finance/chart/${{tickerBase + suffix}}?range=5d&interval=1d`;
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
                    break;
                }}
            }} catch (e) {{ continue; }}
        }}
        
        let pctChange = pYester !== 0 ? (diff / pYester) * 100 : 0;
        let contribPct = pctChange * (weight / 100);
        let contribution = diff * (weight / 100);
        
        totalPct += contribPct;
        totalContribution += contribution;
        
        let colorClass = diff > 0 ? "up" : (diff < 0 ? "down" : "");
        
        tableRows += `<tr>
            <td>${{name}} (${{tickerBase}})</td>
            <td>${{weight}}%</td>
            <td>${{success ? pYester.toFixed(2) : 'N/A'}}</td>
            <td class="${{colorClass}}">${{success ? pCurr.toFixed(2) : 'N/A'}}</td>
            <td class="${{colorClass}}"><strong>${{pctChange >= 0 ? '+' : ''}}{{pctChange.toFixed(2)}}%</strong></td>
            <td class="${{colorClass}}">${{contribPct >= 0 ? '+' : ''}}{{contribPct.toFixed(2)}}%</td>
            <td class="${{colorClass}}">${{contribution >= 0 ? '+' : ''}}{{contribution.toFixed(4)}}</td>
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
