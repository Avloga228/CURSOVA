import tkinter as tk
from tkinter import ttk  # Використовуємо ttk для випадаючого меню
from tkinter import messagebox
import textwrap
from PIL import Image, ImageTk  # Використовуємо Pillow для підтримки JPG форматів

import ingredientC
import productC
import orderC

class ConfectioneryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управління кондитерською")
        self.root.geometry("1200x600")

        # Фрейм для кнопок навігації
        self.top_frame = tk.Frame(self.root, bg="white", height=50)
        self.top_frame.pack(fill="x")

        # Створення прозорих кнопок
        self.create_navigation_buttons()

        # Створення черги
        self.queue = orderC.Queue()

        # Таймер
        self.timer_running = False
        self.current_order = None
        self.remaining_time_label = None
        self.remaining_time = None

        # Фрейми для різних сторінок
        self.page1_frame = tk.Frame(self.root, bg="#fee8dd")
        self.page2_frame = tk.Frame(self.root, bg="#fee8dd")
        self.page3_frame = tk.Frame(self.root, bg="#fee8dd")
        self.page4_frame = tk.Frame(self.root, bg="#fee8dd")
        self.page5_frame = tk.Frame(self.root, bg="#fee8dd")

        # Створюємо полотно для скролінгу
        self.canvas = tk.Canvas(self.page1_frame, bg="#fee8dd")
        scrollbar = tk.Scrollbar(self.page1_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Загальний контейнер, який містить як текст, так і продукти
        self.scrollable_frame = tk.Frame(self.canvas)

        # Прокручуваний фрейм
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", tags="center")

        # Оновлюємо розмір Canvas відповідно до розміру контенту
        self.scrollable_frame.bind("<Configure>", self._update_scroll_region)

        # Прокручування колесиком миші (обмеження тільки вниз)
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        self.root.configure(bg="white")
        self.scrollable_frame.configure(bg="#fee8dd")
        self.canvas.configure(bg="#fee8dd")

        # Продукти (Назва, ціна, категорія, вага, к-сть, шлях до фото)
        self.products = [
            productC.Product("Київський торт", 485.00, "Торт", 1000, 1, "C:/Users/MSI/Desktop/Cursova/Київський торт.png"),
            productC.Product("Рулет з маком", 39.99, "Рулет", 200, 1, "C:/Users/MSI/Desktop/Cursova/Рулет з маком.png"),
            productC.Product("Печиво 'Горішки' з кремом", 99.00, "Печиво", 150, 1, "C:/Users/MSI/Desktop/Cursova/Печиво 'Горішки' з кремом.png"),
            productC.Product("Тістечко 'Картошка'", 35.00, "Тістечко", 70, 1, "C:/Users/MSI/Desktop/Cursova/Тістечко 'Картошка'.png"),
            productC.Product("Торт 'Медовик'", 325.00, "Торт", 1600, 1, "C:/Users/MSI/Desktop/Cursova/Торт 'Медовик'.png"),
            productC.Product("Пісочне печиво", 36.99, "Печиво", 400, 1, "C:/Users/MSI/Desktop/Cursova/Пісочне печиво.png"),
            productC.Product("Еклери з кремом", 84.99, "Тістечко", 210, 1, "C:/Users/MSI/Desktop/Cursova/Еклери з кремом.png"),
            productC.Product("Шоколадний торт", 413.40, "Торт", 900, 1, "C:/Users/MSI/Desktop/Cursova/Шоколадний торт.png"),
            productC.Product("Макова булочка", 17.90, "Печиво", 100, 1, "C:/Users/MSI/Desktop/Cursova/Макова булочка.png"),
            productC.Product("Вафлі з кремом", 21.90, "Вафлі", 100, 1, "C:/Users/MSI/Desktop/Cursova/Вафлі з кремом.png"),
            productC.Product("Кекс з полуницею", 34.99, "Кекс", 100, 1, "C:/Users/MSI/Desktop/Cursova/Кекс з полуницею.png"),
            productC.Product("Кекс з родзинками", 34.99, "Кекс", 100, 1, "C:/Users/MSI/Desktop/Cursova/Кекс з родзинками.png"),
            productC.Product("Кекс з чорницею", 34.99, "Кекс", 100, 1, "C:/Users/MSI/Desktop/Cursova/Кекс з чорницею.png"),
            productC.Product("Круасан зі згущеним молоком", 26.88, "Круасан", 100, 1, "C:/Users/MSI/Desktop/Cursova/Круасан зі згущеним молоком.png"),
            productC.Product("Круасан з полуницею", 26.88, "Круасан", 100, 1, "C:/Users/MSI/Desktop/Cursova/Круасан з полуницею.png"),
            productC.Product("Круасан з шоколадом", 26.88, "Круасан", 100, 1, "C:/Users/MSI/Desktop/Cursova/Круасан з шоколадом.png")
        ]

        # Словник інгрідієнтів до продуктів
        self.product_ingredients = {
            "Київський торт": {"Борошно": 2, "Цукор": 2, "Молоко": 2},
            "Рулет з маком": {"Борошно": 1, "Цукор": 1, "Молоко": 1, "Мак": 1},
            "Печиво 'Горішки' з кремом": {"Борошно": 1, "Цукор": 1, "Молоко": 1},
            "Тістечко 'Картошка'": {"Борошно": 1, "Цукор": 1, "Молоко": 1},
            "Торт 'Медовик'": {"Борошно": 2, "Цукор": 2, "Молоко": 2, "Мед": 2},
            "Пісочне печиво": {"Борошно": 1, "Цукор": 1, "Масло": 1},
            "Еклери з кремом": {"Борошно": 1, "Цукор": 1, "Крем": 2},
            "Шоколадний торт": {"Борошно": 2, "Цукор": 2, "Молоко": 2, "Какао": 2},
            "Макова булочка": {"Борошно": 1, "Цукор": 1, "Мак": 2},
            "Вафлі з кремом": {"Борошно": 1, "Цукор": 2, "Крем": 2},
            "Кекс з полуницею": {"Борошно": 1, "Цукор": 2, "Полуниця": 2},
            "Кекс з родзинками": {"Борошно": 1, "Цукор": 1, "Родзинки": 2},
            "Кекс з чорницею": {"Борошно": 1, "Цукор": 1, "Чорниця": 2},
            "Круасан зі згущеним молоком": {"Борошно": 2, "Цукор": 2, "Крем": 2},
            "Круасан з полуницею": {"Борошно":2, "Цукор": 2, "Полуниця": 2},
            "Круасан з шоколадом": {"Борошно": 2, "Цукор": 2, "Какао": 2}
        }

        # Створюємо словник інгредієнтів з використанням класу Ingredient(ім'я, ціна, к-сть)
        self.ingredients = {
            "Цукор": ingredientC.Ingredient("Цукор", 8, 10),
            "Борошно": ingredientC.Ingredient("Борошно", 8, 10),
            "Молоко": ingredientC.Ingredient("Молоко", 18, 10),
            "Мак": ingredientC.Ingredient("Мак", 1.5, 5),
            "Полуниця": ingredientC.Ingredient("Полуниця", 1.8, 5),
            "Мед": ingredientC.Ingredient("Мед", 20, 5),
            "Масло": ingredientC.Ingredient("Масло", 2.3, 5),
            "Какао": ingredientC.Ingredient("Какао", 13.5, 5),
            "Родзинки": ingredientC.Ingredient("Родзинки", 2, 5),
            "Чорниця": ingredientC.Ingredient("Чорниця", 2, 5),
            "Крем": ingredientC.Ingredient("Крем", 2.7, 5)
        }

        self.cart = {}  # Ініціалізуємо корзину
        self.load_orders_from_file("orders.txt")  # Завантажуємо замовлення з файлу

        # Зберігаємо посилання на зображення, щоб їх не було видалено збирачем сміття
        self.product_images = []

        # Відображаємо контент першої сторінки
        self.display_content_page_1()

        self.money = 100  # Початковий баланс

        self.create_page_4()

        # Центруємо весь вміст по вертикалі та горизонталі
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def display_content_page_1(self):
        # Очищуємо попередній вміст
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.clear_shapes()

        # Відображаємо фрейм першої сторінки
        self.page2_frame.pack_forget()
        self.page1_frame.pack(fill="both", expand=True)

        # Додаємо текстові заголовки
        header_text = tk.Label(self.scrollable_frame, text="Продукція кондитерської", font=("Helvetica", 24), bg="#fee8dd",
                               fg="black")
        header_text.grid(row=0, column=0, columnspan=3, pady=(20, 10))

        sub_header_text = tk.Label(self.scrollable_frame, text="Керуйте замовленнями та товарами на складі!", font=("Helvetica", 16),
                                   bg="#fee8dd", fg="black")
        sub_header_text.grid(row=1, column=0, columnspan=3, pady=(10, 20))

        # Додаємо продукти
        self.display_products()

    def display_content_page_3(self):
        """Відображення сторінки інгредієнтів"""
        self.switch_page(self.page3_frame)

        self.create_page_3()  # Створюємо сторінку 3 (Інгредієнти)

    def display_content_page_4(self):
        """Відображення сторінки профілю"""
        self.switch_page(self.page4_frame)

        self.create_page_4()

    def display_content_page_5(self):
        """Відображення сторінки замовлень"""
        self.switch_page(self.page5_frame)

        self.create_page_5()

    def display_products(self):
        self.clear_shapes()
        self.clear_canvas()  # Очищуємо канвас перед додаванням нових продуктів
        self.switch_page(self.page1_frame)
        # Відображення продуктів у сітці
        for i, product in enumerate(self.products):
            # Отримуємо атрибути об'єкта Product
            name = product.getName()
            price = product.getPrice()
            product_type = product.getProductType()
            weight = product.getWeight()
            quantity_in_stock = product.getQuantityInStock()
            image_path = product.getImagePath()

            # Обчислюємо рядок та стовпець
            row = (i // 4) + 1  # Починаємо з 1-го рядка
            col = (i % 4) - 1

            # Створюємо відображення продукту
            self.create_rounded_rectangle(row, col, product, name, price, product_type, weight, quantity_in_stock,
                                          image_path)

        self.create_rounded_hotbar()

    def create_page_3(self):
        # Очищуємо попередній вміст
        for widget in self.page3_frame.winfo_children():
            widget.destroy()

        """Створення сторінки з інгредієнтами та кнопками купівлі/продажу"""
        self.page3_title = tk.Label(self.page3_frame, text="Склад інгредієнтів", font=("Helvetica", 16), bg="#fee8dd")
        self.page3_title.grid(row=0, column=0, columnspan=3, pady=10)

        self.ingredient_labels = {}
        self.sell_buttons = {}
        self.buy_buttons = {}

        row = 1
        for name, ingredient in self.ingredients.items():
            # Отримуємо дані інгредієнта
            quantity = ingredient.getQuantity()
            price = ingredient.getPrice()

            # Відображення інгредієнта
            ingredient_label = tk.Label(self.page3_frame,
                                        text=f"{name}: {quantity} пачок по {price} грн",
                                        bg="#fee8dd")
            ingredient_label.grid(row=row, column=0, padx=5, pady=5, sticky="e")

            # Кнопки купити та продати
            sell_button = tk.Button(self.page3_frame, text="-",
                                    font=("Helvetica", 10),
                                    bg="#fee8dd",
                                    fg="black",
                                    command=lambda i=name: self.sell_ingredient(i))
            sell_button.grid(row=row, column=1, padx=5, sticky="w")

            buy_button = tk.Button(self.page3_frame, text="+", font=("Helvetica", 10),
                                   bg="#fee8dd",
                                   fg="black",
                                   command=lambda i=name: self.buy_ingredient(i))
            buy_button.grid(row=row, column=2, padx=5, sticky="w")

            self.ingredient_labels[name] = ingredient_label
            self.sell_buttons[name] = sell_button
            self.buy_buttons[name] = buy_button

            row += 1

        # Вирівнювання всіх стовпців по центру
        self.page3_frame.grid_columnconfigure(0, weight=1)
        self.page3_frame.grid_columnconfigure(2, weight=1)

    def create_page_4(self):
        # Очищуємо попередній вміст
        for widget in self.page4_frame.winfo_children():
            widget.destroy()

        """Створення сторінки профілю з балансом грошей"""
        self.page4_title = tk.Label(self.page4_frame, text="Профіль", font=("Helvetica", 16), bg="#fee8dd")
        self.page4_title.pack(pady=10)

        self.money_label = tk.Label(self.page4_frame, text=f"Ваш баланс: {self.money} грн", font=("Helvetica", 14),
                                    bg="#fee8dd")
        self.money_label.pack(pady=10)

    def create_page_5(self):
        # Очищуємо попередній вміст
        for widget in self.page5_frame.winfo_children():
            widget.destroy()

        # Заголовок сторінки
        self.page5_title = tk.Label(self.page5_frame, text="Замовлення", font=("Helvetica", 16), bg="#fee8dd")
        self.page5_title.pack(pady=10)

        # Завантажуємо поточне замовлення
        if self.queue.isEmpty():
            tk.Label(self.page5_frame, text="Немає активних замовлень!", bg="#fee8dd", fg="red").pack(pady=20)
            return

        self.current_order = self.queue.peek()  # Перше замовлення в черзі
        order_frame = tk.Frame(self.page5_frame, bg="#f7e4c3", padx=10, pady=5, relief="solid", borderwidth=1)
        order_frame.pack(pady=10, padx=10, fill="x")

        # Відображаємо товари замовлення
        tk.Label(order_frame, text="Товари замовлення:", font=("Helvetica", 12), bg="#f7e4c3").pack(anchor="w")

        items = self.current_order.getItems()  # Отримуємо список товарів
        item_dict = {}
        for item in items:
            product_name = item.getName()
            if product_name in item_dict:
                item_dict[product_name] += 1
            else:
                item_dict[product_name] = 1

        for product_name, quantity in item_dict.items():
            tk.Label(order_frame, text=f"- {product_name}: {quantity} шт.", font=("Helvetica", 12),
                     bg="#f7e4c3").pack(anchor="w")

        # Відображаємо залишковий час
        self.remaining_time = self.current_order.getRemainingTime()  # Отримуємо залишковий час за допомогою методу
        self.remaining_time_label = tk.Label(order_frame,
                                             text=f"Час очікування: {self.remaining_time // 60:02}:{self.remaining_time % 60:02} хв.",
                                             font=("Helvetica", 12), bg="#f7e4c3")
        self.remaining_time_label.pack(anchor="w")

        # Запускаємо таймер якщо не запущено
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.current_order.setRemainingTime(self.remaining_time)  # Оновлюємо залишковий час у замовленні
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60

            # Оновлюємо текст на екрані, щоб показувати хвилини та секунди
            self.remaining_time_label.config(text=f"Час очікування: {minutes:02}:{seconds:02} хв.")
            self.root.after(1000, self.update_timer)  # Оновлюємо щосекунди
        else:
            # Видаляємо замовлення, якщо час вийшов
            self.timer_running = False
            self.queue.pop()
            self.create_page_5()  # Оновлюємо екран

    def display_cart(self):
        # Очищуємо попередній вміст
        for widget in self.page2_frame.winfo_children():
            widget.destroy()

        self.switch_page(self.page2_frame)

        # Заголовок
        header_text = tk.Label(self.page2_frame, text="Продаж товарів", font=("Helvetica", 24), bg="#fee8dd",
                               fg="black")
        header_text.grid(row=0, column=1, columnspan=2, pady=20, sticky="ew")

        # Відображення товарів у кошику
        total_price = 0
        row = 1  # Початковий рядок для відображення товарів

        for product_name, quantity in self.cart.items():  # cart - це словник з товарами та їх кількістю
            try:
                product = productC.findByName(self.products, product_name)  # Отримуємо об'єкт продукту за назвою
                price = product.getPrice() * quantity  # Рахуємо ціну з урахуванням кількості

                # Відображаємо товар
                tk.Label(self.page2_frame, text=f"{product_name} - {quantity} шт. - {price:.2f} грн",
                         font=("Helvetica", 12), bg="#fee8dd").grid(row=row, column=1, sticky="ew")

                # Кнопка для видалення товару
                tk.Button(self.page2_frame, text="Видалити", font=("Helvetica", 10), bg="#fee8dd",
                          command=lambda name=product_name: self.remove_from_cart(name)).grid(row=row, column=2)

                total_price += price
                row += 1
            except RuntimeError as e:
                print(f"Error: {e}")  # Логування помилки, якщо продукт не знайдено

        # Показуємо загальну суму
        tk.Label(self.page2_frame, text=f"Загальна сума: {total_price:.2f} грн", font=("Helvetica", 14),
                 bg="#fee8dd").grid(row=row, column=1, pady=20, columnspan=2, sticky="ew")

        # Кнопка для оформлення замовлення
        tk.Button(self.page2_frame, text="Підтвердити замовлення", font=("Helvetica", 12), bg="#fee8dd",
                  command=lambda: self.confirm_order(total_price)).grid(row=row + 1, column=1, pady=10, columnspan=2)

        # Вирівнювання всіх стовпців по центру
        self.page2_frame.grid_columnconfigure(0, weight=1)
        self.page2_frame.grid_columnconfigure(3, weight=1)

    def remove_from_cart(self, product_name):
        # Видалення продукту зі словника за назвою
        if product_name in self.cart:
            quantity = self.cart[product_name]

            # Збільшуємо кількість товару на складі
            product = productC.findByName(self.products, product_name)
            self.update_product_quantity(product, quantity, 0)

            # Видаляємо товар з кошика
            del self.cart[product_name]

        self.display_cart()  # Оновлюємо відображення кошика

    def compare_products(self, cart_dict, items):
        """
        Порівнює продукти в корзині зі списком товарів у замовленні за їх іменами та кількістю.
        """
        product_dict = {}

        for product in items:
            name = product.getName()
            if name in product_dict:
                product_dict[name] += 1
            else:
                product_dict[name] = 1

        return cart_dict == product_dict

    def confirm_order(self, total_price):
        """
        Перевіряє, чи корзина відповідає поточному замовленню.
        """
        if self.queue.isEmpty():
            tk.messagebox.showinfo("Замовлення", "Немає активних замовлень.")
            return

        self.current_order = self.queue.peek()
        items = self.current_order.getItems()  # Отримуємо список товарів
        if self.compare_products(self.cart, items):
            # Замовлення зібрано правильно
            tk.messagebox.showinfo("Замовлення", "Замовлення виконано успішно!")
            self.money += total_price
            self.queue.pop()  # Видаляємо виконане замовлення
            self.cart.clear()  # Очищуємо корзину
            self.display_cart()
        else:
            # Замовлення не відповідає корзині
            tk.messagebox.showerror("Замовлення", "Замовлення не відповідає! Перевірте корзину.")

    def add_to_cart(self, product):
        """
        Додає товар до корзини.
        """
        product_name = product.getName()
        product_quantity = product.getQuantityInStock()

        if product_quantity > 0:
            self.cart[product_name] = self.cart.get(product_name, 0) + 1
            self.update_product_quantity(product, -1, 1)  # Зменшуємо кількість продукту на складі
        else:
            messagebox.showwarning("Недостатньо продуктів", f"На складі недостатньо {product_name}.")

        self.display_content_page_1()

    def load_orders_from_file(self, filename="orders.txt"):
        """
        Завантажує замовлення з текстового файлу
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    # Розділяємо рядок на товари та час
                    parts = line.strip().split('|')
                    items_part = parts[0]
                    wait_time = int(parts[1].strip())

                    # Створюємо словник товарів
                    items = []
                    for item in items_part.split(','):
                        name, quantity = item.strip().split(':')
                        product = productC.findByName(self.products, name.strip())  # Знайти продукт
                        if product:
                            for _ in range(int(quantity)):
                                items.append(product)

                    # Якщо знайшли продукти, додаємо замовлення в чергу
                    if items:
                        total_price = sum([product.getPrice() for product in items])  # Підраховуємо загальну вартість
                        order = orderC.Order(len(items), items, total_price, "2024-12-11",
                                             wait_time)  # Створюємо об'єкт замовлення
                        self.queue.append(order)  # Додаємо замовлення в чергу

        except FileNotFoundError:
            tk.messagebox.showerror("Помилка", f"Файл {filename} не знайдено!")
        except Exception as e:
            tk.messagebox.showerror("Помилка", f"Сталася помилка при зчитуванні файлу: {e}")

    def buy_ingredient(self, ingredient_name):
        """Купити інгредієнт (зменшуємо баланс і збільшуємо кількість)"""
        ingredient = self.ingredients[ingredient_name]
        cost = ingredient.getPrice()
        if self.money >= cost:
            self.money -= cost
            ingredient.setQuantity(ingredient.getQuantity() + 1)
            self.update_ingredient_label(ingredient_name)
            self.update_money_label()
        else:
            messagebox.showwarning("Недостатньо коштів", "У вас недостатньо грошей для купівлі цього інгредієнта.")

    def sell_ingredient(self, ingredient_name):
        """Продати інгредієнт (збільшуємо баланс і зменшуємо кількість)"""
        ingredient = self.ingredients[ingredient_name]
        if ingredient.getQuantity() > 0:
            cost = ingredient.getPrice()
            self.money += cost
            ingredient.setQuantity(ingredient.getQuantity() - 1)
            self.update_ingredient_label(ingredient_name)
            self.update_money_label()
        else:
            messagebox.showwarning("Немає інгредієнтів", "У вас немає цього інгредієнта для продажу.")

    def update_product_quantity(self, product, quantity_change, need_to_change):
        for p in self.products:
            if p.getName() == product.getName():
                quantity = p.getQuantityInStock()
                if quantity_change < 0: # Якщо ми продаємо товар
                    quantity += quantity_change
                    if quantity < 0:
                        quantity = 0  # Не дозволяємо від'ємну кількість
                else:                   # Якщо товар добавляється, використовуємо інгрідієнти
                    if need_to_change:
                        if self.use_ingredients_for_product(product):
                            quantity += quantity_change
                        else:
                            messagebox.showwarning("Немає інгредієнтів", f"Недостатньо інгрідієнтів для виробництва {product.getName()}")
                    else:
                        quantity += quantity_change


                p.setQuantityInStock(quantity)
        self.display_content_page_1()

    def use_ingredients_for_product(self, product):
        product_name = product.getName()
        if product_name in self.product_ingredients:
            required_ingredients = self.product_ingredients[product_name]
            for ingredient_name, quantity in required_ingredients.items():
                ingredient = self.ingredients[ingredient_name]
                if ingredient.getQuantity() < quantity:
                    return False  # Недостатньо інгредієнтів
            for ingredient_name, quantity in required_ingredients.items():
                ingredient = self.ingredients[ingredient_name]
                ingredient.setQuantity(ingredient.getQuantity() - quantity)
            return True
        return False

    def update_ingredient_label(self, ingredient_name):
        """Оновлення інформації про інгредієнт"""
        ingredient = self.ingredients[ingredient_name]
        quantity = ingredient.getQuantity()
        price = ingredient.getPrice()
        self.ingredient_labels[ingredient_name].config(text=f"{ingredient_name}: {quantity} пачок по {price} грн")

    def update_money_label(self):
        """Оновлення балансу грошей на сторінці профілю"""
        self.money_label.config(text=f"Ваш баланс: {self.money} грн")

    def create_navigation_buttons(self):
        # Кнопки навігації з прозорим фоном
        tk.Button(self.top_frame, text="Головна", font=("Helvetica", 12), bg="white", fg="black", borderwidth=0,
                  command=self.go_to_main).pack(side="left", padx=10, pady=10)
        tk.Button(self.top_frame, text="Про нас", font=("Helvetica", 12), bg="white", fg="black", borderwidth=0,
                  command=self.go_to_about).pack(side="left", padx=10, pady=10)
        tk.Button(self.top_frame, text="Продаж", font=("Helvetica", 12), bg="white", fg="black", borderwidth=0,
                  command=self.display_cart).pack(side="right", padx=10, pady=10)

        # Кнопка для переходу до сторінки складу інгредієнтів
        tk.Button(self.top_frame, text="Склад інгредієнтів", font=("Helvetica", 12), bg="white", fg="black", borderwidth=0,
                                      command=self.go_to_ingredient).pack(side="left", padx=20, pady=10)

        # Кнопка для переходу до сторінки профілю
        tk.Button(self.top_frame, text="Профіль", font=("Helvetica", 12), bg="white", fg="black", borderwidth=0,
                                        command=self.go_to_profile).pack(side="right", padx=20, pady=10)

        # Кнопка для переходу до сторінки замовлень
        tk.Button(self.top_frame, text="Замовлення", font=("Helvetica", 12), bg="white", fg="black", borderwidth=0,
                                        command=self.go_to_order).pack(side="left", padx=20, pady=10)

    def switch_page(self, page):
        """Загальний метод для перемикання між сторінками"""
        # Ховаємо всі сторінки
        self.page1_frame.pack_forget()
        self.page2_frame.pack_forget()
        self.page3_frame.pack_forget()
        self.page4_frame.pack_forget()
        self.page5_frame.pack_forget()

        # Відображаємо обрану сторінку
        page.pack(fill="both", expand=True)

    def go_to_main(self):
        # Логіка для переходу на головну сторінку
        self.display_content_page_1()

    def go_to_about(self):
        # Відображення повідомлення про автора
        info = (
            "Програму розробив студент Чабанов Павло з групи ОІ-26\n"
            "Email: pavlo.chabanov.oi.2023@lpnu.ua\n"
            "Всі фотографії, назви продуктів та інші речі, використані в програмі, не для комерційного застосування.\n"
            "Дякую за використання!"
        )
        tk.messagebox.showinfo("Про нас", info)

    def go_to_ingredient(self):
        self.display_content_page_3()

    def go_to_profile(self):
        self.display_content_page_4()

    def go_to_order(self):
        self.display_content_page_5()

    def create_rounded_rectangle(self, row, col, product, name, price, product_type, weight, quantity_in_stock,
                                 image_path):
        # Координати для округленого прямокутника
        x1 = col * 270 + 360  # Горизонтальне зміщення
        y1 = row * 310 + 10  # Вертикальне зміщення
        x2 = x1 + 240  # Ширина прямокутника
        y2 = y1 + 280  # Висота прямокутника
        radius = 20  # Радіус кутів

        # Завантажуємо та змінюємо розмір зображення продукту
        image = Image.open(image_path)
        image = image.resize((150, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.product_images.append(photo)  # Зберігаємо посилання на зображення, щоб уникнути його збору сміття

        # Малюємо округлений прямокутник
        self.canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill="#fff1ee", outline="#fff1ee", width=2, tags="dynamic")
        self.canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill="#fff1ee", outline="#fff1ee", width=2, tags="dynamic")
        self.canvas.create_oval(x1, y1, x1 + radius * 2, y1 + radius * 2, fill="#fff1ee", outline="#fff1ee", tags="dynamic")
        self.canvas.create_oval(x2 - radius * 2, y1, x2, y1 + radius * 2, fill="#fff1ee", outline="#fff1ee", tags="dynamic")
        self.canvas.create_oval(x1, y2 - radius * 2, x1 + radius * 2, y2, fill="#fff1ee", outline="#fff1ee", tags="dynamic")
        self.canvas.create_oval(x2 - radius * 2, y2 - radius * 2, x2, y2, fill="#fff1ee", outline="#fff1ee", tags="dynamic")

        # Додаємо зображення в центр округленого прямокутника
        image_x = (x1 + x2) / 2
        image_y = y1 + radius + 50
        self.canvas.create_image(image_x, image_y, image=photo, anchor="center", tags="dynamic")

        # Додаємо текст з вагою продукту під зображенням
        weight_x = image_x
        weight_y = y2 - 70  # Розташовуємо текст на відстані 20 пікселів від нижнього краю прямокутника
        self.canvas.create_text(weight_x, weight_y, text=f"{weight} грам", font=("Helvetica", 12), anchor="center", tags="dynamic")

        # Додаємо текст з назвою продукту та кількістю на складі під зображенням
        wrapped_name = textwrap.fill(f"{name} ({quantity_in_stock}. шт)",
                                     width=30)  # Переносимо текст на новий рядок, якщо більше 15 символів
        name_x = image_x
        name_y = y2 - 47  # Розташовуємо текст на відстані 20 пікселів від нижнього краю прямокутника
        self.canvas.create_text(name_x, name_y, text=wrapped_name, font=("Helvetica", 12), anchor="center", tags="dynamic")

        # Додаємо текст з ціною під зображенням
        price_x = image_x
        price_y = y2 - 20  # Розташовуємо текст на відстані 20 пікселів від нижнього краю прямокутника
        formatted_price = f"{price:.2f} грн"
        self.canvas.create_text(price_x, price_y, text=formatted_price, font=("Helvetica", 15), anchor="center", tags="dynamic")

        # Додаємо кнопку "Додати до кошика" під ціною
        add_to_cart_button = tk.Button(
            self.root,
            text="Добавити",
            font=("Helvetica", 10),
            bg="#fff1ee",
            fg="black",
            command=lambda p=product: self.add_to_cart(p)  # Передаємо продукт в метод
        )

        # Додаємо кнопку "Виробити продукт" під ціною
        add_to_stock_button = tk.Button(
            self.root,
            text="+",
            font=("Helvetica", 10),
            bg="#fff1ee",
            fg="black",
            command=lambda p=product: self.update_product_quantity(p, 1, 1)
        )

        # Розміщуємо кнопку на канвасі за координатами (під фото)
        button1_x = image_x
        button1_y = image_y + 100  # Зміщуємо кнопку трохи нижче фото
        self.canvas.create_window(button1_x, button1_y, window=add_to_cart_button, tags="dynamic")

        # Розміщуємо кнопку на канвасі за координатами (під фото)
        button2_x = image_x + 50
        button2_y = image_y + 100  # Зміщуємо кнопку трохи нижче фото
        self.canvas.create_window(button2_x, button2_y, window=add_to_stock_button, tags="dynamic")

    def clear_shapes(self):
        # Видаляємо всі об'єкти з тегом "product"
        self.canvas.delete("product_*")

    def clear_canvas(self):
        self.canvas.delete("dynamic")  # Видаляє тільки елементи з тегом "dynamic"

    def create_rounded_hotbar(self):
        # Координати для округленого прямокутника
        x1 = 90  # Горизонтальне зміщення
        y1 = 240  # Вертикальне зміщення
        x2 = 1140  # Ширина прямокутника
        y2 = 300  # Висота прямокутника
        radius = 20  # Радіус кутів

        # Малюємо округлений прямокутник
        self.canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill="#fff1ee", outline="#fff1ee", width=2, tags="dynamic")
        self.canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill="#fff1ee", outline="#fff1ee", width=2, tags="dynamic")
        self.canvas.create_oval(x1, y1, x1 + radius * 2, y1 + radius * 2, fill="#fff1ee", outline="#fff1ee", tags="dynamic")
        self.canvas.create_oval(x2 - radius * 2, y1, x2, y1 + radius * 2, fill="#fff1ee", outline="#fff1ee", tags="dynamic")
        self.canvas.create_oval(x1, y2 - radius * 2, x1 + radius * 2, y2, fill="#fff1ee", outline="#fff1ee", tags="dynamic")
        self.canvas.create_oval(x2 - radius * 2, y2 - radius * 2, x2, y2, fill="#fff1ee", outline="#fff1ee", tags="dynamic")

        # Створюємо контейнер для випадаючого списку справа хотбара
        sort_frame = tk.Frame(self.canvas, bg="#fff1ee", bd=0)
        self.canvas.create_window(x2 - 300, y1 + 20, window=sort_frame, anchor="nw", tags="dynamic")  # Розташування вікна

        # Додаємо текст для заголовка сортування
        tk.Label(sort_frame, text="Сортування:", font=("Helvetica", 12), bg="#fff1ee").pack(side="left", padx=10)

        # Випадаючий список для сортування
        self.sort_option = tk.StringVar()
        sort_dropdown = ttk.Combobox(sort_frame, textvariable=self.sort_option, font=("Arial", 12), width=10,
                                     state="readonly")
        sort_dropdown['values'] = (
            "По алфавіту (А-Я)", "По алфавіту (Я-А)", "По ціні (зростання)", "По ціні (спадання)")
        sort_dropdown.current(0)  # Вибір за замовчуванням
        sort_dropdown.pack(side="left", padx=10)
        sort_dropdown.bind("<<ComboboxSelected>>", self.sort_products)

    def sort_products(self, event):
        # Логіка для сортування за вибраним параметром
        option = self.sort_option.get()
        if option == "По алфавіту (А-Я)":
            # Викликаємо C++ метод сортування за алфавітом (А-Я)
            self.products = productC.sortByNameAsc(self.products)
        elif option == "По алфавіту (Я-А)":
            # Викликаємо C++ метод сортування за алфавітом (Я-А)
            self.products = productC.sortByNameDesc(self.products)
        elif option == "По ціні (зростання)":
            # Викликаємо C++ метод сортування за ціною (зростання)
            self.products = productC.sortByPriceAsc(self.products)
        elif option == "По ціні (спадання)":
            # Викликаємо C++ метод сортування за ціною (спадання)
            self.products = productC.sortByPriceDesc(self.products)

        # Відображаємо продукти знову
        self.display_products()

    def _update_scroll_region(self, event=None):
        # Оновлюємо область скролінгу, щоб починалась з самого верху
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Центруємо контент по горизонталі
        canvas_width = self.canvas.winfo_width()
        frame_width = self.scrollable_frame.winfo_reqwidth()
        if canvas_width > frame_width:
            self.canvas.coords("center", (canvas_width / 2 - frame_width / 2, 0))
        else:
            self.canvas.coords("center", (0, 0))

    def _on_mouse_wheel(self, event):
        # Прокрутка canvas при використанні колеса миші, тільки вниз
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# Запуск програми
root = tk.Tk()
app = ConfectioneryApp(root)
root.mainloop()
