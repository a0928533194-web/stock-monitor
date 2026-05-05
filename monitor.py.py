import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import yfinance as yf
from datetime import datetime
import threading

# 完整成分股對照表 (數據來源：image_e630f7.png)
stocks_data = {
    "旺矽": ("6223.TW", 9.70), "台積電": ("2330.TW", 7.88), "穎崴": ("6515.TW", 6.12),
    "精測": ("6510.TW", 5.68), "信驊": ("5274.TW", 5.63), "聯亞": ("3081.TWO", 4.56),
    "群聯": ("8299.TWO", 3.95), "光聖": ("6442.TW", 3.75), "華星光": ("4979.TWO", 3.15),
    "台燿": ("6274.TWO", 3.00), "沛亨": ("6291.TWO", 2.94), "力旺": ("3529.TWO", 2.94),
    "聖暉*": ("5536.TWO", 2.63), "波若威": ("3163.TWO", 2.59), "京元電子": ("2449.TW", 2.58),
    "中光電": ("5371.TWO", 2.50), "邑錡": ("7402.TWO", 2.45), "日月光投控": ("3711.TW", 2.40),
    "環球晶": ("6488.TWO", 2.21), "新應材": ("4749.TWO", 2.10), "鴻勁": ("7769.TW", 1.85),
    "世禾": ("3551.TWO", 1.79), "台特化": ("4772.TWO", 1.45), "旺宏": ("2337.TW", 1.35),
    "聯鈞": ("3450.TW", 1.07), "大江": ("8436.TWO", 1.01)
}

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("台股基金持股監測 v15.3")
        self.root.geometry("850x650")
        
        # 上方控制區
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=10, fill='x')
        
        self.run_btn = tk.Button(self.top_frame, text="更新數據並計算總和", command=self.start_update_thread, 
                                 bg="#1a5276", fg="white", font=("微软雅黑", 11, "bold"))
        self.run_btn.pack(side=tk.LEFT, padx=20)
        
        self.total_label = tk.Label(self.top_frame, text="預估基金總漲跌: --", font=("微软雅黑", 12, "bold"), fg="#c0392b")
        self.total_label.pack(side=tk.RIGHT, padx=20)

        # 表格區
        columns = ("Name", "Symbol", "Weight", "Price_N1", "Price_N", "Contribution")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        
        self.tree.heading("Name", text="投資名稱")
        self.tree.heading("Symbol", text="代號")
        self.tree.heading("Weight", text="比例 (%)")
        self.tree.heading("Price_N1", text="昨日(n-1)") 
        self.tree.heading("Price_N", text="當天(n)")    
        self.tree.heading("Contribution", text="漲跌貢獻") # (n - n-1) * 比例
        
        for col in columns:
            self.tree.column(col, width=120, anchor='center')
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

    def start_update_thread(self):
        self.run_btn.config(state=tk.DISABLED, text="計算中...")
        threading.Thread(target=self.update_data, daemon=True).start()

    def update_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        total_contribution = 0
        
        for name, (sid, weight) in stocks_data.items():
            try:
                stock = yf.Ticker(sid)
                hist = stock.history(period="5d")
                
                if len(hist) >= 2:
                    p_n = hist['Close'].iloc[-1]   # 當天 (n)
                    p_n1 = hist['Close'].iloc[-2]  # 昨日 (n-1)
                    
                    # 計算邏輯：(當天 - 昨天) * 比例 / 100 (因為比例是百分比)
                    contribution = (p_n - p_n1) * (weight / 100)
                    total_contribution += contribution
                    
                    self.tree.insert("", "end", values=(
                        name, sid, f"{weight}%", round(p_n1, 2), round(p_n, 2), round(contribution, 4)
                    ))
            except:
                pass
        
        # 更新總和標籤
        self.total_label.config(text=f"預估基金總漲跌: {round(total_contribution, 4)}")
        self.run_btn.config(state=tk.NORMAL, text="更新數據並計算總和")
        messagebox.showinfo("完成", f"計算完畢！\n當前基金成分股總貢獻：{round(total_contribution, 4)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()