import tkinter as tk
from tkinter import messagebox, font
from modules.record import add_record, load_records, save_records, delete_record  # 确保delete_record函数在modules.record中
from modules.view import get_recent_records
from modules.statistics import calculate_statistics
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
mpl.rcParams['axes.unicode_minus'] = False

class LoginWindow:
    def __init__(self):
        self.login_root = tk.Tk()
        self.login_root.title("记账本登录")
        self.login_root.geometry("300x150")
        self.login_root.configure(bg='#f0f8ff')

        # 设置字体
        label_font = font.Font(family='Arial', size=12)

        tk.Label(self.login_root, text="用户名:", bg='#f0f8ff', font=label_font).grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.login_root, width=20, font=label_font)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.login_root, text="密码:", bg='#f0f8ff', font=label_font).grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_root, width=20, show='*', font=label_font)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        login_button = tk.Button(self.login_root, text="登录", command=self.login, bg="#4CAF50", fg="white", font=label_font)
        login_button.grid(row=2, column=1, padx=5, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == '123456' and password == '123456':
            self.login_root.destroy()
            self.open_main_app()
        else:
            messagebox.showerror("错误", "用户名或密码错误！")

    def open_main_app(self):
        root = tk.Tk()
        app = PersonalAccountingApp(root)
        root.mainloop()

class PersonalAccountingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("个人记账本")
        self.root.geometry("700x400")
        self.root.configure(bg='#f0f8ff')

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

        delete_button = tk.Button(button_frame, text="删除记录", command=self.create_delete_window, bg="#F44336", fg="white", font=label_font, width=20)
        delete_button.grid(row=0, column=3, padx=10)

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

    def create_delete_window(self):
        """创建删除记录的窗口."""
        delete_window = tk.Toplevel()
        delete_window.title("删除记账记录")
        delete_window.geometry("300x150")
        delete_window.configure(bg='#f0f8ff')

        tk.Label(delete_window, text="输入要删除的记录日期 (YYYY-MM-DD):", bg='#f0f8ff', font=('Arial', 12)).pack(pady=10)
        date_entry = tk.Entry(delete_window, width=30)
        date_entry.pack(pady=5)

        delete_button = tk.Button(delete_window, text="删除", command=lambda: self.delete_record(date_entry.get()), bg="#F44336", fg="white")
        delete_button.pack(pady=10)

    def delete_record(self, date):
        """删除指定日期的记录."""
        success = delete_record(date)  # 调用modules.record中的delete_record函数
        print(f"删除操作返回值: {success}")  # 调试输出
        if success:
            messagebox.showinfo("成功", "记录已删除！")
        else:
            messagebox.showerror("错误", "未找到指定的记录！")

    def show_statistics(self):
        """显示统计信息和可视化图表."""
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

        # 创建三个子图用于三个饼图
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        # 绘制收入类别饼图
        if income_categories:
            labels = list(income_categories.keys())
            sizes = list(income_categories.values())
            axs[0].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            axs[0].set_title('各类收入占比')

        # 绘制支出类别饼图
        if expense_categories:
            labels = list(expense_categories.keys())
            sizes = list(expense_categories.values())
            axs[1].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            axs[1].set_title('各类支出占比')

        # 绘制收入和支出占比饼图
        if total_income > 0 or total_expense > 0:
            sizes = [total_income, total_expense]
            labels = ['收入', '支出']
            axs[2].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            axs[2].set_title('收入和支出占比')

        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.login_root.mainloop()
