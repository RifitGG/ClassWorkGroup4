import sqlite3
import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk
from datetime import datetime


conn = sqlite3.connect('restaurant.db')
c = conn.cursor()




class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ресторан Гюсто")


        self.root.geometry("1920x1080")
        self.root.configure(bg='#f2f2f2')


        self.cart = []
        self.username = ""


        self.create_login_page()

    def create_login_page(self):
        self.clear_window()


        self.map_image = self.load_map_image()
        if self.map_image:
            map_label = tk.Label(self.root, image=self.map_image, bg='#f2f2f2')
            map_label.pack(pady=10)

        self.username_label = tk.Label(self.root, text="Имя пользователя:", bg='#f2f2f2', font=("Arial", 12))
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Пароль:", bg='#f2f2f2', font=("Arial", 12))
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Войти", command=self.login, font=("Arial", 12), bg='#4CAF50', fg='white')
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.root, text="Зарегистрироваться", command=self.open_registration_window, font=("Arial", 12), bg='#2196F3', fg='white')
        self.register_button.pack(pady=10)

    def load_map_image(self):
        try:
            img = Image.open("map.png")  # Замените "map.png" на путь к вашему изображению карты
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Ошибка загрузки изображения карты: {e}")
            return None

    def open_registration_window(self):
        registration_window = tk.Toplevel(self.root)
        registration_window.title("Регистрация")
        registration_window.geometry("1600x800")
        registration_window.configure(bg='#f2f2f2')

        # Отображение карты
        map_image = self.load_map_image()
        if map_image:
            map_label = tk.Label(registration_window, image=map_image, bg='#f2f2f2')
            map_label.pack(pady=10)

        username_label = tk.Label(registration_window, text="Имя пользователя:", bg='#f2f2f2', font=("Arial", 12))
        username_label.pack(pady=10)
        username_entry = tk.Entry(registration_window, font=("Arial", 12))
        username_entry.pack(pady=5)

        password_label = tk.Label(registration_window, text="Пароль:", bg='#f2f2f2', font=("Arial", 12))
        password_label.pack(pady=10)
        password_entry = tk.Entry(registration_window, show="*", font=("Arial", 12))
        password_entry.pack(pady=5)

        register_button = tk.Button(registration_window, text="Зарегистрироваться", font=("Arial", 12), bg='#2196F3', fg='white', command=lambda: self.register(username_entry.get(), password_entry.get(), registration_window))
        register_button.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()

        if user:
            self.username = username
            self.create_menu_page()
        else:
            messagebox.showerror("Ошибка входа", "Неверное имя пользователя или пароль")

    def register(self, username, password, window):
        if username and password:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            window.destroy()
        else:
            messagebox.showerror("Ошибка регистрации", "Заполните все поля")

    def create_menu_page(self):
        self.clear_window()

        c.execute("SELECT * FROM menu_items")
        menu_items = c.fetchall()

        for item in menu_items:
            item_frame = tk.Frame(self.root, bg='#ffffff', bd=2, relief=tk.GROOVE)
            item_frame.pack(fill='x', padx=10, pady=5)

            item_name = tk.Label(item_frame, text=item[1], font=("Arial", 14), bg='#ffffff')
            item_name.grid(row=0, column=0, padx=10, pady=5)

            item_desc = tk.Label(item_frame, text=item[2], font=("Arial", 10), bg='#ffffff')
            item_desc.grid(row=1, column=0, padx=10, pady=5)

            item_price = tk.Label(item_frame, text=f"Цена: {item[3]:.2f} руб.", font=("Arial", 12), bg='#ffffff')
            item_price.grid(row=0, column=1, padx=10, pady=5)

            try:
                img = Image.open(item[4])
                img = img.resize((50, 50), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                item_image = tk.Label(item_frame, image=img, bg='#ffffff')
                item_image.image = img
                item_image.grid(row=0, column=2, rowspan=2, padx=10, pady=5)
            except Exception as e:
                print(f"Ошибка загрузки изображения: {e}")

            add_to_cart_button = tk.Button(item_frame, text="В корзину", command=lambda i=item: self.add_to_cart(i), bg='#4CAF50', fg='white')
            add_to_cart_button.grid(row=0, column=3, rowspan=2, padx=10, pady=5)

        checkout_button = tk.Button(self.root, text="Оформить заказ", command=self.create_order_page, font=("Arial", 14), bg='#FF9800', fg='white')
        checkout_button.pack(pady=20)

        view_orders_button = tk.Button(self.root, text="Просмотреть заказы", command=self.view_orders, font=("Arial", 12), bg='#2196F3', fg='white')
        view_orders_button.pack(pady=10)

    def add_to_cart(self, item):
        self.cart.append(item)
        messagebox.showinfo("Корзина", f"Добавлено {item[1]} в корзину")

    def create_order_page(self):
        self.clear_window()

        if not self.cart:
            messagebox.showinfo("Оформление заказа", "Ваша корзина пуста!")
            self.create_menu_page()
            return

        total_price = sum(item[3] for item in self.cart)

        order_label = tk.Label(self.root, text="Ваш заказ:", font=("Arial", 16), bg='#f2f2f2')
        order_label.pack(pady=10)

        for item in self.cart:
            item_label = tk.Label(self.root, text=f"{item[1]} - {item[3]:.2f} руб.", font=("Arial", 12), bg='#f2f2f2')
            item_label.pack(pady=5)

        total_label = tk.Label(self.root, text=f"Итого: {total_price:.2f} руб.", font=("Arial", 14), bg='#f2f2f2')
        total_label.pack(pady=10)

        table_number_label = tk.Label(self.root, text="Введите номер столика:", bg='#f2f2f2', font=("Arial", 12))
        table_number_label.pack(pady=10)
        self.table_number_entry = tk.Entry(self.root, font=("Arial", 12))
        self.table_number_entry.pack(pady=5)

        confirm_button = tk.Button(self.root, text="Подтвердить заказ", command=lambda: self.confirm_order(total_price), font=("Arial", 14), bg='#4CAF50', fg='white')
        confirm_button.pack(pady=20)

        back_button = tk.Button(self.root, text="Назад в меню", command=self.create_menu_page, font=("Arial", 12), bg='#2196F3', fg='white')
        back_button.pack(pady=10)

    def confirm_order(self, total_price):
        table_number = self.table_number_entry.get()
        if not table_number.isdigit():
            messagebox.showerror("Ошибка", "Введите корректный номер столика!")
            return

        order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        items_list = ', '.join([item[1] for item in self.cart])

        c.execute("INSERT INTO orders (username, items, total_price, order_time, table_number) VALUES (?, ?, ?, ?, ?)",
                  (self.username, items_list, total_price, order_time, table_number))
        conn.commit()

        messagebox.showinfo("Заказ подтвержден", "Ваш заказ успешно оформлен!")
        self.cart.clear()
        self.create_menu_page()

    def view_orders(self):
        self.clear_window()

        c.execute("SELECT * FROM orders WHERE username=?", (self.username,))
        orders = c.fetchall()

        if not orders:
            messagebox.showinfo("Заказы", "У вас нет оформленных заказов.")
            self.create_menu_page()
            return

        for order in orders:
            order_label = tk.Label(self.root, text=f"Заказ №{order[0]} - Столик: {order[5]} - Время: {order[4]} - Сумма: {order[3]:.2f} руб.", font=("Arial", 12), bg='#f2f2f2')
            order_label.pack(pady=5)

        clear_orders_button = tk.Button(self.root, text="Очистить заказы", command=self.clear_orders, font=("Arial", 12), bg='#FF5722', fg='white')
        clear_orders_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Назад в меню", command=self.create_menu_page, font=("Arial", 12), bg='#2196F3', fg='white')
        back_button.pack(pady=20)

    def clear_orders(self):
        c.execute("DELETE FROM orders WHERE username=?", (self.username,))
        conn.commit()
        messagebox.showinfo("Очистка", "Все заказы удалены!")
        self.create_menu_page()

# Запуск приложения
root = tk.Tk()
app = RestaurantApp(root)
root.mainloop()

# Закрытие соединения с базой данных
conn.close()