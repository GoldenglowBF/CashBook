import json
import tkinter as tk
from tkinter import messagebox, font
from modules.record import add_record, load_records, save_records, delete_record, record_2_json
from modules.view import get_recent_records
from modules.statistics import calculate_statistics
from modules.record import record_1_json
from modules.record import record_2_json
from modules.view import load_1_json
from modules.view import load_2_json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as mpl
from datetime import datetime
import numpy as np

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

class PersonalAccountingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("个人记账本")
        self.root.geometry("700x400")
        self.root.configure(bg='#f0f8ff')

        title_font = font.Font(family='Arial', size=16, weight='bold')
        label_font = font.Font(family='Arial', size=12)

        tk.Label(root, text="记账本", font=title_font, bg='#f0f8ff', fg='#4B0082').pack(pady=20)

        frame = tk.Frame(root, bg='#f0f8ff')
        frame.pack(pady=10)

        tk.Label(frame, text="日期 (YYYY-MM-DD):", font=label_font, bg='#f0f8ff').grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(frame, width=40, font=label_font)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="金额:", font=label_font, bg='#f0f8ff').grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(frame, width=40, font=label_font)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="类别:", font=label_font, bg='#f0f8ff').grid(row=2, column=0, padx=5, pady=5)

        # 定义类别选项
        self.category_var = tk.StringVar()
        self.category_var.set("选择类别")  # 设置默认值

        # 创建下拉选择框
        category_options = ["饮食", "交通", "服饰", "医疗", "娱乐", "其他"]  # 这里可以添加更多类别
        self.category_menu = tk.OptionMenu(frame, self.category_var, *category_options)
        self.category_menu.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="备注:", font=label_font, bg='#f0f8ff').grid(row=3, column=0, padx=5, pady=5)
        self.note_entry = tk.Entry(frame, width=40, font=label_font)
        self.note_entry.grid(row=3, column=1, padx=5, pady=5)

        button_frame = tk.Frame(root, bg='#f0f8ff')
        button_frame.pack(pady=20)

        submit_button = tk.Button(button_frame, text="添加记录", command=self.submit_record, bg="#4CAF50", fg="white", font=label_font, width=20)
        submit_button.grid(row=0, column=0, padx=10)

        view_button = tk.Button(button_frame, text="查看最近记录", command=self.create_view_window, bg="#2196F3", fg="white", font=label_font, width=20)
        view_button.grid(row=0, column=1, padx=10)

        stats_button = tk.Button(button_frame, text="显示统计信息", command=self.show_statistics, bg="#FF9800", fg="white", font=label_font, width=20)
        stats_button.grid(row=0, column=2, padx=10)

        delete_button = tk.Button(button_frame, text="删除记录", command=self.create_delete_window, bg="#F44336", fg="white", font=label_font, width=20)
        delete_button.grid(row=0, column=3, padx=10)

        # 添加个人信息按钮
        info_button = tk.Button(button_frame, text="个人信息", command=self.create_info_window, bg="#2196F3", fg="white", font=label_font, width=20)
        info_button.grid(row=0, column=4, padx=10)
        # 添加收支趋势分析按钮
        trends_button = tk.Button(button_frame, text="收支趋势分析", command=self.create_trend_analysis_window, bg="#FF5722",
                                  fg="white", font=label_font, width=20)
        trends_button.grid(row=0, column=5, padx=10)

        # 初始化用户字典
        self.userf = {}
        with open('data/un_pw.json','r') as f:
            self.userf = json.load(f)

    def create_trend_analysis_window(self):
        """创建收支趋势分析窗口"""
        trend_window = tk.Toplevel()
        trend_window.title("收支趋势分析")
        trend_window.geometry("600x400")
        trend_window.configure(bg='#f0f8ff')

        tk.Label(trend_window, text="开始日期 (YYYY-MM-DD):", bg='#f0f8ff').pack(pady=10)
        start_date_entry = tk.Entry(trend_window, width=20)
        start_date_entry.pack(pady=5)

        tk.Label(trend_window, text="结束日期 (YYYY-MM-DD):", bg='#f0f8ff').pack(pady=10)
        end_date_entry = tk.Entry(trend_window, width=20)
        end_date_entry.pack(pady=5)

        def generate_trend():
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("日期格式错误", "请确保日期格式为 YYYY-MM-DD。")
                return

            records = load_records()
            monthly_income = {}
            monthly_expense = {}

            for record in records:
                record_date = datetime.strptime(record['date'], "%Y-%m-%d")
                if start_date <= record_date <= end_date:
                    month = record_date.strftime("%Y-%m")
                    if record['amount'] > 0:
                        monthly_income[month] = monthly_income.get(month, 0) + record['amount']
                    else:
                        monthly_expense[month] = monthly_expense.get(month, 0) + abs(record['amount'])

            # 确保每个月都有数据，缺失的月份填0
            all_months = sorted(set(monthly_income.keys()).union(set(monthly_expense.keys())))
            income_values = [monthly_income.get(month, 0) for month in all_months]
            expense_values = [monthly_expense.get(month, 0) for month in all_months]

            # 绘制图表
            plt.figure(figsize=(10, 5))
            plt.plot(all_months, income_values, label='收入', marker='o')
            plt.plot(all_months, expense_values, label='支出', marker='o')
            plt.title('收支趋势分析')
            plt.xlabel('月份')
            plt.ylabel('金额')
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.show()

        trend_button = tk.Button(trend_window, text="生成趋势图", command=generate_trend, bg="#4CAF50", fg="white")
        trend_button.pack(pady=20)

    def show_login_window(self):
        # 设置字体
        title_font = font.Font(family='Arial', size=16, weight='bold')
        label_font = font.Font(family='Arial', size=12)
        """显示登录窗口."""
        login_window = tk.Toplevel(self.root)
        login_window.title("登录")
        login_window.geometry("300x300")
        login_window.configure(bg='#f0f8ff')

        tk.Label(login_window, text="用户名:", font=label_font, bg='#f0f8ff').pack(pady=10)
        username_entry = tk.Entry(login_window, font=label_font)
        username_entry.pack(pady=10)

        tk.Label(login_window, text="密码:", font=label_font, bg='#f0f8ff').pack(pady=10)
        password_entry = tk.Entry(login_window, show="*", font=label_font)
        password_entry.pack(pady=10)

        def login():
            username = username_entry.get()
            password = password_entry.get()
            if username in self.userf and self.userf[username] == password:
                messagebox.showinfo("登录成功", "欢迎回来！")
                login_window.destroy()
                self.root.deiconify()  # 显示主窗口
            else:
                messagebox.showerror("登录失败", "用户名或密码错误。")

        login_button = tk.Button(login_window, text="登录", command=login, bg="#4CAF50", fg="white", font=label_font, width=20)
        login_button.pack(pady=10)

        # 添加注册按钮
        register_button = tk.Button(login_window, text="注册", command=self.show_register_window, bg="#4CAF50",
                                    fg="white", font=label_font, width=20)
        register_button.pack(pady=10)

    def show_register_window(self):
        # 设置字体
        title_font = font.Font(family='Arial', size=16, weight='bold')
        label_font = font.Font(family='Arial', size=12)
        """显示注册窗口."""
        register_window = tk.Toplevel(self.root)
        register_window.title("注册")
        register_window.geometry("300x250")
        register_window.configure(bg='#f0f8ff')

        tk.Label(register_window, text="用户名:", font=label_font, bg='#f0f8ff').pack(pady=10)
        username_entry = tk.Entry(register_window, font=label_font)
        username_entry.pack(pady=10)

        tk.Label(register_window, text="密码:", font=label_font, bg='#f0f8ff').pack(pady=10)
        password_entry = tk.Entry(register_window, show="*", font=label_font)
        password_entry.pack(pady=10)

        def register():
            username = username_entry.get()
            password = password_entry.get()
            if username in self.userf:
                messagebox.showerror("注册失败", "用户名已存在。")
            else:
                users = {}
                users[username] = password
                self.userf.update(users)
                messagebox.showinfo("注册成功", "注册成功！")
                with open('data/un_pw.json', 'w') as f:
                    json.dump(self.userf, f)
                register_window.destroy()  # 关闭注册窗口

        register_button = tk.Button(register_window, text="注册", command=register, bg="#4CAF50", fg="white",
                                    font=label_font, width=20)
        register_button.pack(pady=10)

    def submit_record(self):
        date = self.date_entry.get()
        amount = float(self.amount_entry.get())
        category = self.category_var.get()  # 获取选择的类别

        note = self.note_entry.get()

        add_record(date, amount, category, note)

        self.date_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_var.set("选择类别")  # 重置类别选择
        self.note_entry.delete(0, tk.END)

        messagebox.showinfo("成功", "记录已添加！")

    def create_view_window(self):
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

    def create_delete_window(self):
        delete_window = tk.Toplevel()
        delete_window.title("删除记账记录")
        delete_window.geometry("500x300")
        delete_window.configure(bg='#f0f8ff')

        tk.Label(delete_window, text="选择要删除的记录:", bg='#f0f8ff', font=('Arial', 12)).pack(pady=10)

        self.record_listbox = tk.Listbox(delete_window, width=60, height=10)
        records = load_records()
        for record in records:
            record_text = f"日期: {record['date']}, 金额: {record['amount']}, 类别: {record['category']}, 备注: {record['note']}"
            self.record_listbox.insert(tk.END, record_text)
        self.record_listbox.pack(pady=10)

        delete_button = tk.Button(delete_window, text="删除选中记录", command=self.delete_selected_record, bg="#F44336", fg="white")
        delete_button.pack(pady=10)

    def delete_selected_record(self):
        selected_index = self.record_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("警告", "请先选择一条记录。")
            return

        records = load_records()
        selected_record_text = self.record_listbox.get(selected_index)
        selected_date = selected_record_text.split(",")[0].split(": ")[1]

        success = delete_record(date=selected_date)
        if success:
            messagebox.showinfo("成功", "记录已删除！")
            self.record_listbox.delete(selected_index)
        else:
            messagebox.showerror("错误", "未找到指定的记录！")

    def show_statistics(self):
        total_income, total_expense, income_categories, expense_categories = calculate_statistics()

        stats_window = tk.Toplevel()
        stats_window.title("统计信息")
        stats_window.geometry("1000x600")
        stats_window.configure(bg='#f0f8ff')

        tk.Label(stats_window, text=f"总收入: {total_income}", font=('Arial', 14), bg='#f0f8ff').pack(pady=10)
        tk.Label(stats_window, text=f"总支出: {total_expense}", font=('Arial', 14), bg='#f0f8ff').pack(pady=10)

        tk.Label(stats_window, text="各类别收入:", font=('Arial', 14), bg='#f0f8ff').pack(pady=10)
        for category, amount in income_categories.items():
            tk.Label(stats_window, text=f"  {category}: {amount}", bg='#f0f8ff').pack()

        tk.Label(stats_window, text="各类别支出:", font=('Arial', 14), bg='#f0f8ff').pack(pady=10)
        for category, amount in expense_categories.items():
            tk.Label(stats_window, text=f"  {category}: {amount}", bg='#f0f8ff').pack()

        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        if income_categories:
            labels = list(income_categories.keys())
            sizes = list(income_categories.values())
            axs[0].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            axs[0].set_title('各类收入占比')

        if expense_categories:
            labels = list(expense_categories.keys())
            sizes = list(expense_categories.values())
            axs[1].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            axs[1].set_title('各类支出占比')

        if total_income > 0 or total_expense > 0:
            sizes = [total_income, total_expense]
            labels = ['收入', '支出']
            axs[2].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            axs[2].set_title('收入和支出占比')

        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

    def create_info_window(self):
        info_window = tk.Toplevel()
        info_window.title("个人信息")
        info_window.geometry("400x350")  # 增加窗口高度以容纳新信息
        info_window.configure(bg='#f0f8ff')

        label_font = font.Font(family='Arial', size=12)

        tk.Label(info_window, text="姓名:", bg='#f0f8ff', font=label_font).grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(info_window, width=30, font=label_font)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(info_window, text="邮箱:", bg='#f0f8ff', font=label_font).grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(info_window, width=30, font=label_font)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(info_window, text="电话:", bg='#f0f8ff', font=label_font).grid(row=2, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(info_window, width=30, font=label_font)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)

        # 显示记账总笔数
        total_records = len(load_records())  # 获取总记录数
        tk.Label(info_window, text="记账总笔数:", bg='#f0f8ff', font=label_font).grid(row=3, column=0, padx=5, pady=5)
        tk.Label(info_window, text=str(total_records), bg='#f0f8ff', font=label_font).grid(row=3, column=1, padx=5, pady=5)

        save_button = tk.Button(info_window, text="保存信息", command=self.save_info, bg="#4CAF50", fg="white", font=label_font)
        save_button.grid(row=4, column=1, padx=5, pady=10)

        cj_button = tk.Button(info_window, text="更改账本", command=self.change_json_window, bg="#4CAF50", fg="white", font=label_font)
        cj_button.grid(row=5, column=1, padx=5, pady=10)

    def save_info(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        # 这里可以添加保存信息的逻辑，例如保存到文件或数据库
        messagebox.showinfo("成功", "个人信息已保存！")

    def change_json_window(self):
        cj_window = tk.Toplevel()
        cj_window.title("更改账本")
        cj_window.geometry("500x300")
        cj_window.configure(bg='#f0f8ff')
        label_font = font.Font(family='Arial', size=12)

        tk.Label(cj_window, text="选择要使用的账本", bg='#f0f8ff', font=('Arial', 12)).pack(pady=10)
        j1_button = tk.Button(cj_window, text="账本1", command=self.set_json1, bg="#4CAF50", fg="white",font=label_font)
        j1_button.pack(pady=10)
        j2_button = tk.Button(cj_window, text="账本2", command=self.set_json2, bg="#4CAF50", fg="white", font=label_font)
        j2_button.pack(pady=10)

    def set_json1(self):
            record_1_json()
            load_1_json()

    def set_json2(self):
            record_2_json()
            load_2_json()



if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalAccountingApp(root)
    app.root.withdraw()  # 隐藏主窗口
    app.show_login_window()  # 显示登录窗口
    root.mainloop()
