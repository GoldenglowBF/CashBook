import tkinter as tk
from tkinter import messagebox, font
from modules.record import add_record, load_records
from modules.view import get_recent_records
from modules.statistics import calculate_statistics

class PersonalAccountingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("个人记账本")
        self.root.geometry("500x400")  # 增加窗口尺寸
        self.root.configure(bg='#f0f8ff')  # 设置背景色

        # 设置字体
        title_font = font.Font(family='Arial', size=16, weight='bold')
        label_font = font.Font(family='Arial', size=12)

        # 创建标题
        tk.Label(root, text="记账本", font=title_font, bg='#f0f8ff', fg='#4B0082').pack(pady=20)

        # 输入框和标签
        frame = tk.Frame(root, bg='#f0f8ff')
        frame.pack(pady=10)

        tk.Label(frame, text="日期 (YYYY-MM-DD):", font=label_font, bg='#f0f8ff').grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(frame, width=40, font=label_font)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="金额:", font=label_font, bg='#f0f8ff').grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(frame, width=40, font=label_font)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="类别:", font=label_font, bg='#f0f8ff').grid(row=2, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(frame, width=40, font=label_font)
        self.category_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="备注:", font=label_font, bg='#f0f8ff').grid(row=3, column=0, padx=5, pady=5)
        self.note_entry = tk.Entry(frame, width=40, font=label_font)
        self.note_entry.grid(row=3, column=1, padx=5, pady=5)

        # 创建按钮
        button_frame = tk.Frame(root, bg='#f0f8ff')
        button_frame.pack(pady=20)

        submit_button = tk.Button(button_frame, text="添加记录", command=self.submit_record, bg="#4CAF50", fg="white", font=label_font, width=20)
        submit_button.grid(row=0, column=0, padx=10)

        view_button = tk.Button(button_frame, text="查看最近记录", command=self.create_view_window, bg="#2196F3", fg="white", font=label_font, width=20)
        view_button.grid(row=0, column=1, padx=10)

        stats_button = tk.Button(button_frame, text="显示统计信息", command=self.show_statistics, bg="#FF9800", fg="white", font=label_font, width=20)
        stats_button.grid(row=0, column=2, padx=10)

    def submit_record(self):
        """获取输入并添加记录."""
        date = self.date_entry.get()
        amount = float(self.amount_entry.get())
        category = self.category_entry.get()
        note = self.note_entry.get()

        # 调用添加记录的函数
        add_record(date, amount, category, note)

        # 清空输入框
        self.date_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)

        messagebox.showinfo("成功", "记录已添加！")

    def create_view_window(self):
        """创建查看记录的窗口."""
        view_window = tk.Toplevel()
        view_window.title("最近记账记录")
        view_window.geometry("500x300")
        view_window.configure(bg='#f0f8ff')

        records = get_recent_records()
        if not records:
            tk.Label(view_window, text="没有记录可显示。", bg='#f0f8ff', font=('Arial', 12)).pack(pady=10)
        else:
            tk.Label(view_window, text="最近的记录:", font=('Arial', 14), bg='#f0f8ff').pack(pady=10)
            for record in records:
                record_text = f"日期: {record['date']}, 金额: {record['amount']}, 类别: {record['category']}, 备注: {record['note']}"
                tk.Label(view_window, text=record_text, bg='#f0f8ff').pack()

    def show_statistics(self):
        """显示统计信息."""
        total_income, total_expense, income_categories, expense_categories = calculate_statistics()
        
        stats_window = tk.Toplevel()
        stats_window.title("统计信息")
        stats_window.geometry("500x400")
        stats_window.configure(bg='#f0f8ff')

        tk.Label(stats_window, text=f"总收入: {total_income}", font=('Arial', 14), bg='#f0f8ff').pack(pady=10)
        tk.Label(stats_window, text=f"总支出: {total_expense}", font=('Arial', 14), bg='#f0f8ff').pack(pady=10)

        tk.Label(stats_window, text="各类别收入:", font=('Arial', 14), bg='#f0f8ff').pack(pady=10)
        for category, amount in income_categories.items():
            tk.Label(stats_window, text=f"  {category}: {amount}", bg='#f0f8ff').pack()

        tk.Label(stats_window, text="各类别支出:", font=('Arial', 14), bg='#f0f8ff').pack(pady=10)
        for category, amount in expense_categories.items():
            tk.Label(stats_window, text=f"  {category}: {amount}", bg='#f0f8ff').pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalAccountingApp(root)
    root.mainloop()
