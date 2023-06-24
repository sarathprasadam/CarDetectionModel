
def changeTheme(theme,style,master,text_comments):
    if theme == 'Default':
        style.configure('TFrame', background='#e1d8b9')
        master.configure(background='#e1d8b9')
        style.configure('TLabel', background='#e1d8b9', foreground='black')
        style.configure('Header.TLabel', background='#e1d8b9', foreground='black')
        text_comments.configure(background="white")


    elif theme == "Light":
        style.configure('TFrame', background='#e6d4d1')
        master.configure(background='#e6d4d1')
        style.configure('TLabel', background='#e6d4d1', foreground='black')
        style.configure('Header.TLabel', background='#e6d4d1', foreground='black')
        text_comments.configure(background="#f7f1f0")


    elif theme == "Dark":
        style.configure('TFrame', background='#141413')
        master.configure(background='#141413')
        text_comments.configure(background="#5e5e55")
        style.configure('TLabel', background='#141413', foreground='white')
        style.configure('Header.TLabel', background='#141413', foreground='white')