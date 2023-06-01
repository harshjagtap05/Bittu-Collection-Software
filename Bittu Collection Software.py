from tkinter import *
from add_inventory import *
from new_invoice import *
from view_inventory import *
from saved_invoices import *


main_window = Tk()

main_window.geometry("1100x650+50+50")

main_window.title("Billing Software")

#DEFINE MENUBAR
menu = Menu(main_window)
main_window.config(menu=menu)

#FIRST FRAME
frame1 = LabelFrame(main_window, text="Bittu Collection", padx=15, pady=15)
frame1.grid(row=0, column=0, sticky=W)

#DEFINE COMMANDS
def add_inventory_command():
    # Add "Add Inventory" components to the main_frame
    clear_frame()
    add_inventory_widgets_to_frame(main_frame)

def view_inventory_command():
    clear_frame()
    view_inventory_widgets_to_frame(main_frame)

def new_invoice_command():
    clear_frame()
    new_invoice_widgets_to_frame(main_frame)

def saved_invoices_command():
    clear_frame()
    saved_invoices_widgets_to_frame(main_frame)

def sales_statistics_command():
    root_6 = Tk()
    root_6.title("Sales Statistics")
    root_6.mainloop()

#DEFINE MENUBAR ITEMS
inventory = Menu(menu, tearoff=False)
inventory.add_command(label='Add Inventory', command=add_inventory_command)
inventory.add_command(label='View Inventory', command=view_inventory_command)
menu.add_cascade(label='Inventory', menu=inventory)

sales = Menu(menu, tearoff=False)
sales.add_command(label='New Invoice', command=new_invoice_command)
sales.add_command(label='Saved Invoices', command=saved_invoices_command)
sales.add_command(label='Sales Stats', command=sales_statistics_command)
menu.add_cascade(label='Sales', menu=sales)

add_inventory_button = Button(frame1, text="Add Inventory", padx=30, pady=3, command=add_inventory_command)
add_inventory_button.grid(row=0, column=0)

view_inventory_button = Button(frame1, text="View Inventory", padx=30, pady=3, command=view_inventory_command)
view_inventory_button.grid(row=0, column=1)

new_invoice_button = Button(frame1, text="New Invoice", padx=30, pady=3, command=new_invoice_command)
new_invoice_button.grid(row=0, column=2)

saved_invoices_button = Button(frame1, text="Saved Invoices", padx=30, pady=3, command=saved_invoices_command)
saved_invoices_button.grid(row=0, column=3)

sales_statistics_button = Button(frame1, text="Sales Stats", padx=30, pady=3, command=sales_statistics_command)
sales_statistics_button.grid(row=0, column=4)

main_frame = Frame(main_window)
main_frame.grid(row=2, column=0, sticky=W)

def clear_frame():
    for widgets in main_frame.winfo_children():
        widgets.destroy()


main_window.mainloop()
