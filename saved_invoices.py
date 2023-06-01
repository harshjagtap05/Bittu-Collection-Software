from tkinter import *
from tkinter import ttk

def saved_invoices_widgets_to_frame(frame):
    root = frame
    style = ttk.Style()
    style.theme_use('clam')

    frame1 = LabelFrame(root, text="Add Inventory", padx=15, pady=15)
    frame1.grid(row=0, column=0, sticky=W)

    tree_frame = Frame(root)
    tree_frame.grid(row=2, column=0, padx=10, pady=10)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.grid(row=0, column=6, sticky='ns')

    tree = ttk.Treeview(tree_frame, columns=("c1", "c2", "c3", "c4", "c5"), show='headings', height=10,
                        yscrollcommand=tree_scroll.set)
    tree.grid(row=0, column=0, columnspan=5, sticky=W)

    tree_scroll.config(command=tree.yview)

    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Product Name")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Colour")
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="Size")
    tree.column("# 4", anchor=CENTER)
    tree.heading("# 4", text="Quantity")
    tree.column("# 5", anchor=CENTER)
    tree.heading("# 5", text="Rate")

    bill_no_label = Label(frame1, text="Bill No.:")
    bill_no_label.grid(row=0, column=0)
    e_1 = Entry(frame1, width=40)
    e_1.grid(row=0, column=1, padx=20, pady=10)

    show_details = Button(frame1, text="Show Details", padx=30, pady=2)
    show_details.grid(row=1, column=1)