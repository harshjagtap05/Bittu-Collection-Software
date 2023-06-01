from tkinter import *
from tkinter import ttk
import mysql.connector


def view_inventory_widgets_to_frame(frame):
    root = frame
    style = ttk.Style()
    style.theme_use('clam')

    connect = mysql.connector.connect(host='localhost', user='root', password='hrjagtap@1',
                                      database='inventory')
    conn = connect.cursor()

    conn.execute("SELECT * FROM total_inventory")

    tree_frame = Frame(root)
    tree_frame.grid(row=1, column=0, padx=10, pady=10)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.grid(row=1, column=1, sticky='ns')

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    tree.grid(row=1, column=0)

    tree_scroll.config(command=tree.yview)

    tree['show'] = 'headings'
    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure(".", font=('Helvetica', 11))
    s.configure("Treeview.Heading", font=('Helvetica', 11, "bold"))

    tree["column"] = ("Product", "Colour", "Size", "Quantity", "Rate")

    tree.column("Product", width=150, minwidth=150)
    tree.column("Colour", width=150, minwidth=150)
    tree.column("Size", width=150, minwidth=150, anchor=CENTER)
    tree.column("Quantity", width=100, minwidth=100, anchor=CENTER)
    tree.column("Rate", width=100, minwidth=100, anchor=CENTER)

    tree.heading("Product", text="Product")
    tree.heading("Colour", text="Colour")
    tree.heading("Size", text="Size")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Rate", text="Rate")

    i = 0
    for ro in conn:
        tree.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4]))
        i = i + 1