from tkinter import *
import datetime as dt
from tkinter import ttk
import mysql.connector
import cv2
from pyzbar import pyzbar


def new_invoice_widgets_to_frame(frame):
    root = frame

    style = ttk.Style()
    style.theme_use('clam')

    label_1 = Label(root, text="Date: ")
    label_1.grid(row=0, column=0)

    date = dt.datetime.now()
    format_date = f"{date:%b %d %Y}"
    label_2 = Label(root, text=format_date)
    label_2.grid(row=0, column=1)

    label_3 = Label(root, text="Bill No.: ")
    label_3.grid(row=1, column=0)
    billing_id_entry = Entry(root, width=15)
    billing_id_entry.grid(row=1, column=1, padx=20, pady=10)

    print_bill = Button(root, text="print bill", padx=30, pady=3)
    print_bill.grid(row=2, column=4, columnspan=4)

    tree = ttk.Treeview(root, columns=("c1", "c2", "c3", "c4", "c5"), show='headings', height=10)

    tree.column("# 1", anchor=CENTER, width=250)
    tree.heading("# 1", text="Product Name")
    tree.column("# 2", anchor=CENTER, width=120)
    tree.heading("# 2", text="Colour")
    tree.column("# 3", anchor=CENTER, width=120)
    tree.heading("# 3", text="Size")
    tree.column("# 4", anchor=CENTER, width=120)
    tree.heading("# 4", text="Quantity")
    tree.column("# 5", anchor=CENTER, width=120)
    tree.heading("# 5", text="Rate")

    # Total column is yet remaining to code

    tree.grid(row=3, columnspan=6)

    def insert_data():
        # Create a new database connection and cursor
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="hrjagtap@1",
            database="inventory"
        )
        cursor = cnx.cursor()

        # Get billing id from input box
        billing_id = billing_id_entry.get()

        # Retrieve data from database
        query = "SELECT Productname, Colour, Size, Qty, Rate FROM recently_added WHERE billing_id = %s"
        values = (billing_id,)
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result:
            print(result)

            # Update quantity in database
            current_qty = result[3]
            new_qty = current_qty - 1
            print("current_qty:", current_qty)
            print("new_qty:", new_qty)
            update_query = "UPDATE recently_added SET Qty = %s WHERE billing_id = %s"
            update_values = (new_qty, billing_id)
            cursor.execute(update_query, update_values)
            cnx.commit()

            # Insert data into treeview
            tree.insert("", "end", text=billing_id, values=(result[0], result[1], result[2], 1, result[4]))
        else:
            # Display error message if billing id is not found
            error_label = Label(root, text="Billing ID not found")
            error_label.grid()

        cursor.execute("DROP TRIGGER IF EXISTS update_main")

        cursor.execute("""

        CREATE TRIGGER update_main AFTER UPDATE ON added
        FOR EACH ROW
        BEGIN
            UPDATE main SET qty = (SELECT SUM(qty) FROM invoice WHERE productname = NEW.productname AND colour = NEW.colour AND size = NEW.size AND rate = NEW.rate ) WHERE productname = NEW.productname AND colour = NEW.colour AND size = NEW.size AND rate = NEW.rate;
        END;
        """)

        # Close database connection and cursor
        cursor.close()
        cnx.close()

    def store_data():

        # Get a list of all item IDs in the ttk treeview widget
        import mysql.connector

        # connect to MySQL database
        mydb = mysql.connector.connect(host="localhost", user="root", password="hrjagtap@1", database="inventory")

        # get the cursor object
        mycursor = mydb.cursor()

        # get the last inserted bill_id from the table
        mycursor.execute("SELECT bill_id FROM item ORDER BY bill_id DESC LIMIT 1")
        result = mycursor.fetchone()

        # generate a new bill_id
        if result:
            bill_id = result[0] + 1
        else:
            bill_id = 1

        # insert each row of the treeview into the MySQL table with the new bill_id
        for child in tree.get_children():
            values = tree.item(child, 'values')
            product_name = values[0]
            colour = values[1]
            size = values[2]
            quantity = values[3]
            rate = values[4]

            # insert the data into the MySQL table with the new bill_id
            mycursor.execute(
                "INSERT INTO item (bill_id, product_name, colour, size, quantity, rate) VALUES (%s, %s, %s, %s, %s, %s)",
                (bill_id, product_name, colour, size, quantity, rate))

        # commit the changes to the database
        mydb.commit()

        # close the database connection
        mydb.close()

    print_bill = Button(root, text="Print Bill", padx=60, pady=10, bd=6, command=insert_data)
    print_bill.grid(row=5, column=4, columnspan=4)

    def camera():
        cap = cv2.VideoCapture(0)  # Open the default camera
        detected_barcodes = []  # Initialize an empty list to keep track of detected barcodes

        while True:
            frame = cap.read()  # Read a frame from the camera
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

            # Find and decode Code 128 barcodes in the grayscale image
            barcodes = pyzbar.decode(gray, symbols=[pyzbar.ZBarSymbol.CODE128])

            # Iterate over all detected barcodes and extract the data
            for barcode in barcodes:
                data = barcode.data.decode('utf-8')
                if data not in detected_barcodes:  # Check if this barcode has already been detected
                    detected_barcodes.append(data)  # Add this barcode to the list of detected barcodes
                    print("Detected barcode:", data)

                    # Set the value of the billing_id entry to the detected barcode data
                    billing_id_entry.delete(0, END)
                    billing_id_entry.insert(0, data)

                    # Call the insert_data function to insert the data into the treeview
                    insert_data()

            cv2.imshow('frame', frame)  # Display the captured frame
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit if 'q' is pressed
                break

        cap.release()  # Release the camera
        cv2.destroyAllWindows()  # Close all windows

    save_bill = Button(root, text="Start Scanning", padx=60, pady=10, bd=6, command=camera)
    save_bill.grid(row=4, column=4, columnspan=4)

    print_bill = Button(root, text="print bill", padx=30, pady=3, command=store_data)
    print_bill.grid(row=2, column=4, columnspan=4)