import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

# глобальный список расходов
expenses = []

# загрузка данных из файла при запуске
def load_data():
    try:
        with open('expenses.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# сохранение данных в файл
def save_data():
    with open('expenses.json', 'w') as f:
        json.dump(expenses, f, indent=4)

# обновление таблицы, заполняет её данными
def update_tree(filtered_expenses=None):
    for row in tree.get_children():
        tree.delete(row)
    data = filtered_expenses if filtered_expenses is not None else expenses
    for exp in data:
        tree.insert('', 'end', values=(exp['amount'], exp['category'], exp['date']))

# добавление расхода
def add_expense():
    amount_str = entry_amount.get()
    category = entry_category.get()
    date_str = entry_date.get()

    # проверка суммы
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except:
        messagebox.showerror("Ошибка", "Введите положительное число для суммы.")
        return

    # проверка даты
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except:
        messagebox.showerror("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД.")
        return

    expense = {
        'amount': amount,
        'category': category,
        'date': date_str
    }
    expenses.append(expense)
    update_tree()
    save_data()

# фильтрация и подсчёт суммы
def filter_expenses():
    cat_filter = entry_filter_category.get().strip()
    date_from = entry_date_from.get().strip()
    date_to = entry_date_to.get().strip()

    filtered = []
    for exp in expenses:
        # категория
        if cat_filter and exp['category'] != cat_filter:
            continue
        # даты
        try:
            exp_date = datetime.strptime(exp['date'], '%Y-%m-%d')
            if date_from:
                df = datetime.strptime(date_from, '%Y-%m-%d')
                if exp_date < df:
                    continue
            if date_to:
                dt = datetime.strptime(date_to, '%Y-%m-%d')
                if exp_date > dt:
                    continue
        except:
            continue
        filtered.append(exp)
    update_tree(filtered)

    # подсчёт суммы
    total = sum(item['amount'] for item in filtered)
    lbl_total.config(text=f"Общая сумма: {total:.2f}")

# инициализация
expenses = load_data()

# создаем главное окно
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x600")

# поля ввода
frm_input = tk.Frame(root)
frm_input.pack(pady=10)

tk.Label(frm_input, text='Сумма:').grid(row=0, column=0)
entry_amount = tk.Entry(frm_input)
entry_amount.grid(row=0, column=1)

tk.Label(frm_input, text='Категория:').grid(row=1, column=0)
entry_category = tk.Entry(frm_input)
entry_category.grid(row=1, column=1)

tk.Label(frm_input, text='Дата (ГГГГ-ММ-ДД):').grid(row=2, column=0)
entry_date = tk.Entry(frm_input)
entry_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
entry_date.grid(row=2, column=1)

btn_add = tk.Button(frm_input, text='Добавить расход', command=add_expense)
btn_add.grid(row=3, column=0, columnspan=2, pady=5)

# таблица расходов
columns = ('amount', 'category', 'date')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.capitalize())
tree.pack(pady=10, fill=tk.BOTH, expand=True)

# фильтры
frm_filters = tk.Frame(root)
frm_filters.pack(pady=10)

tk.Label(frm_filters, text='Категория:').grid(row=0, column=0)
entry_filter_category = tk.Entry(frm_filters)
entry_filter_category.grid(row=0, column=1)

tk.Label(frm_filters, text='Дата с (ГГГГ-ММ-ДД):').grid(row=1, column=0)
entry_date_from = tk.Entry(frm_filters)
entry_date_from.grid(row=1, column=1)

tk.Label(frm_filters, text='Дата по (ГГГГ-ММ-ДД):').grid(row=2, column=0)
entry_date_to = tk.Entry(frm_filters)
entry_date_to.grid(row=2, column=1)

btn_filter = tk.Button(frm_filters, text='Применить фильтр', command=filter_expenses)
btn_filter.grid(row=3, column=0, columnspan=2, pady=5)

# итоговая сумма
lbl_total = tk.Label(root, text='Общая сумма: 0.00', font=('Arial', 14))
lbl_total.pack(pady=10)

btn_total = tk.Button(root, text='Посчитать сумму по текущему фильтру', command=filter_expenses)
btn_total.pack()

# загружаем старые данные
update_tree()

# обработка закрытия/сохранение
def on_closing():
    save_data()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# запуск приложения
root.mainloop()