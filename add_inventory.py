from tkinter import *
from tkinter import ttk
import mysql.connector
import os
import barcode
from barcode.writer import ImageWriter
import uuid
import hashlib
import datetime


def add_inventory_widgets_to_frame(frame):
    root = frame

    style = ttk.Style()
    style.theme_use('clam')

    frame1 = LabelFrame(root, text="Add Inventory", padx=15, pady=15)
    frame1.grid(row=0, column=0, columnspan=2, sticky=W)

    frame2 = LabelFrame(root, padx=15, pady=15)
    frame2.grid(row=1, column=1, sticky=W)

    myLabel_0 = Label(frame1, text="School Name")
    myLabel_0.grid(row=0, column=0)
    school_options = ["NHSS", "St. Xaviers", "SRV"]
    e_0 = ttk.Combobox(frame1, width=30, values=school_options)  # state="readonly"
    e_0.grid(row=1, column=0, padx=5, pady=10)

    myLabel_1 = Label(frame1, text="Product")
    myLabel_1.grid(row=0, column=1)
    product_options = ["Regular Shirt", "Regular H Pant", "Regular Skirt", "Tie", "Belt", "Socks", "Activity Tshirt", "Activity Pant"]
    e_1 = ttk.Combobox(frame1, width=30, values=product_options)  # state="readonly"
    e_1.grid(row=1, column=1, padx=5, pady=10)

    myLabel_2 = Label(frame1, text="Colour")
    myLabel_2.grid(row=0, column=2)
    colour_options = ["Blue", "Green", "Red", "Yellow"]
    e_2 = ttk.Combobox(frame1, width=20, values=colour_options)  # state="readonly"
    e_2.grid(row=1, column=2, padx=5, pady=10)

    myLabel_3 = Label(frame1, text="Size")
    myLabel_3.grid(row=0, column=3)
    e_3 = Entry(frame1, width=20)
    e_3.grid(row=1, column=3, padx=5, pady=10)

    myLabel_4 = Label(frame1, text="Quantity")
    myLabel_4.grid(row=0, column=4)
    e_4 = Entry(frame1, width=20)
    e_4.grid(row=1, column=4, padx=5, pady=10)

    myLabel_5 = Label(frame1, text="Rate")
    myLabel_5.grid(row=0, column=5)
    e_5 = Entry(frame1, width=20)
    e_5.grid(row=1, column=5, padx=5, pady=10)

    tree_frame = Frame(root)
    tree_frame.grid(row=1, column=0, padx=10, pady=10)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.grid(row=0, column=1, sticky='ns')

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    tree.grid(row=0, column=0)

    tree_scroll.config(command=tree.yview)

    tree['show'] = 'headings'
    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure(".", font=('Helvetica', 11))
    s.configure("Treeview.Heading", font=('Helvetica', 11, "bold"))

    tree["column"] = ("Product", "Colour", "Size", "Quantity", "Rate")

    tree.column("Product", width=250, minwidth=250)
    tree.column("Colour", width=100, minwidth=100)
    tree.column("Size", width=100, minwidth=100, anchor=CENTER)
    tree.column("Quantity", width=100, minwidth=100, anchor=CENTER)
    tree.column("Rate", width=100, minwidth=100, anchor=CENTER)

    tree.heading("Product", text="Product")
    tree.heading("Colour", text="Colour")
    tree.heading("Size", text="Size")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Rate", text="Rate")

    connect = mysql.connector.connect(host='localhost', user='root', password='hrjagtap@1', database='inventory')
    conn = connect.cursor()
    conn.execute("SELECT * FROM recently_added ORDER BY id DESC;")
    i = 0
    for ro in conn:
        tree.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[6]))
        i = i + 1

    def select_item():
        selected_item = tree.focus()
        if selected_item:
            item_values = tree.item(selected_item)['values']
            first_text = item_values[0]
            second_text = item_values[1]
            third_text = item_values[2]
            fourth_int = item_values[3]
            fifth_int = item_values[4]
            sixth_text = item_values[5]
            print("Product:", first_text)
            print("Colour:", second_text)
            print("Size:", third_text)
            print("Quantity:", fourth_int)
            print("Rate:", fifth_int)
            print("Billing ID:", sixth_text)
            codes = [sixth_text]
            generate_code128_barcodes(codes, fourth_int)

    # noinspection PyShadowingNames
    def generate_code128_barcodes(codes, fourth_int):
        code128 = barcode.get_barcode_class('code128')
        for code in codes:
            for i in range(int(fourth_int)):
                code128_barcode = code128(code, writer=ImageWriter())
                file_path = os.path.join("C:/Users/harsh/Desktop/barcode", f"{code}_{i}")
                code128_barcode.save(file_path)

    def add_items():
        # Get product data from input fields
        Product = e_0.get() + ", " + e_1.get()
        Colour = e_2.get()
        Size = e_3.get()
        Quantity = e_4.get()
        Rate = e_5.get()

        db = mysql.connector.connect(host="localhost", user="root", password="hrjagtap@1", database="inventory")

        # Create a cursor object
        cursor = db.cursor()

        # Create the total_inventory table trigger
        cursor.execute("DROP TRIGGER IF EXISTS update_total_inventory")
        cursor.execute("""
        CREATE TRIGGER update_total_inventory AFTER INSERT ON recently_added
        FOR EACH ROW
            BEGIN
                IF EXISTS(SELECT * FROM total_inventory WHERE product = NEW.product AND size = NEW.size AND colour=NEW.colour AND rate=NEW.rate) THEN
                    UPDATE total_inventory SET qty = qty + NEW.qty WHERE product = NEW.product AND colour=NEW.colour AND size = NEW.size AND rate=NEW.rate AND quantity=NEW.quantity;
                ELSE
                    INSERT INTO total_inventory (product, colour, size, qty, rate, quantity, product_id) VALUES (NEW.product, NEW.colour, NEW.size, NEW.qty, NEW.rate, NEW.quantity, NEW.product_id);
        END IF;
        END;
        """)

        # Generate billing ID using hash function and current timestamp
        product_id = str(uuid.uuid4())[:8]

        # Insert data and billing ID into table
        query = "INSERT INTO recently_added(Product, Colour, Size, Qty, Rate, Quantity, product_id) VALUES(%s, %s, %s,%s, %s, %s, %s)"
        values = (Product, Colour, Size, Quantity, Rate, 1, product_id)
        cursor.execute(query, values)
        db.commit()
        query = "INSERT INTO mediator(Product, Colour, Size, Qty, Rate, Quantity, product_id) VALUES(%s, %s, %s,%s, %s, %s, %s)"
        values = (Product, Colour, Size, Quantity, Rate, 1, product_id)
        cursor.execute(query, values)
        db.commit()

        # Insert data into treeview
        column1 = Product
        column2 = Colour
        column3 = int(Size)
        column4 = int(Quantity)
        column5 = Rate
        column6 = product_id
        tree.insert("", "end", values=(column1, column2, column3, column4, column5, column6))

        e_1.delete(0, END)
        e_2.delete(0, END)
        e_3.delete(0, END)
        e_4.delete(0, END)
        e_5.delete(0, END)

    # noinspection PyShadowingNames
    def refresh_tree():
        connect = mysql.connector.connect(host='localhost', user='root', password='hrjagtap@1', database='inventory')
        conn = connect.cursor()
        conn.execute("SELECT * FROM recently_added ORDER BY id DESC;")
        i = 0
        for ro in conn:
            tree.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[6]))
            i = i + 1

    def save_and_refresh():
        add_items()
        refresh_tree()

    def delete_row():
        selected_items = tree.selection()
        if selected_items:
            for item in selected_items:
                item_values = tree.item(item)['values']
                product = item_values[0]
                colour = item_values[1]
                size = item_values[2]
                quantity = item_values[3]
                rate = item_values[4]
                product_id = item_values[5]

                db = mysql.connector.connect(host='localhost', user='root', password='hrjagtap@1', database='inventory')
                cursor = db.cursor()
                query = "DELETE FROM recently_added WHERE product = %s AND colour = %s AND size = %s AND qty = %s AND rate = %s AND product_id = %s"
                values = (product, colour, size, quantity, rate, product_id)
                cursor.execute(query, values)
                db.commit()

                tree.delete(item)

    def edit_record():
        e_0.delete(0, END)
        e_1.delete(0, END)
        e_2.delete(0, END)
        e_3.delete(0, END)
        e_4.delete(0, END)
        e_5.delete(0, END)
        selected = tree.focus()
        values = tree.item(selected, 'values')

        product_parts = values[0].split(", ")
        e_0.insert(0, product_parts[0])
        e_1.insert(0, product_parts[1])
        e_2.insert(0, values[1])
        e_3.insert(0, values[2])
        e_4.insert(0, values[3])
        e_5.insert(0, values[4])

    def update_record():
        pass

    button_save = Button(frame1, text="Save", padx=37, pady=5, command=save_and_refresh)
    button_save.grid(row=2, column=5)

    update_button = Button(frame1, text="Update", padx=30, pady=5, command=update_record)
    update_button.grid(row=3, column=5)

    delete_button = Button(frame2, text="Delete", padx=55, pady=10, command=delete_row)
    delete_button.grid(row=0, column=0, pady=5)

    edit_button = Button(frame2, text="Edit", padx=61, pady=10, command=edit_record)
    edit_button.grid(row=1, column=0, pady=5)

    button_generate_barcode = Button(frame2, text="Generate Barcode", padx=25, pady=10, command=select_item)
    button_generate_barcode.grid(row=2, column=0, pady=5)