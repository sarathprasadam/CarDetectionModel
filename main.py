# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import Tk
from feedback import Feedback




def main():
    root=Tk()
    feedback=Feedback(root)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x =int((screen_width - root.winfo_reqwidth()) // 2)
    y = int((screen_height - root.winfo_reqheight()) // 2)
    root.geometry('+{}+{}'.format(x-100, 100))

    root.mainloop()





if __name__ == '__main__':
    main()


