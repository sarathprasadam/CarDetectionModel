from tkinter import *
from tkinter import ttk
import webbrowser
def clickInfo(master,kind):
    if kind == "Software":
        window = Toplevel(master)
        screen_width = master.winfo_screenwidth()
        x = int((screen_width - master.winfo_reqwidth()) // 2)
        window.resizable(False, False)
        window.title('About Software')
        window.iconbitmap("Images//logo1.ico")
        description = "This software is developed as part of GreatLearning Capstone project."
        label = Label(window, text=description, padx=20, pady=20, wraplength=200)
        window.geometry("400x150+{}+200".format(x + 70))
        label.pack()
    if kind == "Contributers":
        window = Toplevel(master)
        window.resizable(False, False)
        window.title('Software Contributers')
        window.iconbitmap("Images//logo1.ico")
        screen_width = master.winfo_screenwidth()
        x = int((screen_width - master.winfo_reqwidth()) // 2)
        window.geometry("400x150+{}+200".format(x + 70))
        tree = ttk.Treeview(window)

        tree["columns"] = ("First Name", "LinkedIn Link")

        # Format column headings
        tree.heading("#0", text="ID")
        tree.heading("First Name", text="Name")
        tree.heading("LinkedIn Link", text="LinkedIn Link")

        # Add data to the table
        tree.insert("", "end", text="1", values=("Anupam Chakraborty", "https://www.linkedin.com/in/anupam-chakraborty-434640b8/"))
        tree.insert("", "end", text="2", values=("Sarath M", "https://www.linkedin.com/in/sarath-mohan-kdm"))
        tree.insert("", "end", text="3", values=("Boobalan.m.k", "https://www.linkedin.com"))
        tree.insert("", "end", text="4", values=("Fini Sabu", "https://www.linkedin.com/in/fini-sabu/"))
        tree.insert("", "end", text="5", values=("Saiteja Thota", "https://www.linkedin.com/in/saiteja-thota/"))

        # Configure column widths
        tree.column("#0", width=50)
        tree.column("First Name", width=125)
        tree.column("LinkedIn Link", width=200)

        # Function to handle the click event
        def open_link(event):
            item = tree.focus()
            values = tree.item(item)["values"]
            if len(values) > 1:
                link = values[1]
                webbrowser.open(link)

        # Bind the click event to the LinkedIn Link column
        tree.tag_bind("link", "<Button-1>", open_link)

        # Add tags to the LinkedIn Link column
        for item in tree.get_children():
            tree.item(item, tags=("link",))

        # Pack the Treeview widget
        tree.pack()