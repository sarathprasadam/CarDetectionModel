from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from info_click import clickInfo
from themeChange import changeTheme
from detectImage import imageDetect
import shutil
from datetime import datetime
class Feedback:
    def __init__(self, master):
        self.master = master
        master.title("Car Detection Model")
        try:
            master.iconbitmap("Images//logo1.ico")
        except:
            master.iconbitmap("Images\logo1.ico")

        master.resizable(False, False)
        master.configure(background='#e1d8b9')


        self.style = ttk.Style()
        self.style.theme_use('winnative')
        self.style.configure('TFrame', background='#e1d8b9')
        self.style.configure('TButton', background='#4CAF50', foreground='black')
        self.style.configure('TLabel', background='#e1d8b9', font=('Arial', 11))
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'))
        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()
        self.header_text = ttk.Label(self.frame_header, text='Car Detection Model', style='Header.TLabel')
        self.header_text.grid(row=0, column=1,rowspan = 2)
        try:
            self.logo_file = PhotoImage(file='Images//logo.png').subsample(4,4)
        except:
            self.logo_file = PhotoImage(file='Images\logo.png').subsample(4, 4)
        self.logo = ttk.Label(self.frame_header, image = self.logo_file)
        self.logo.grid(row=0, column=0, rowspan=2)
        ttk.Label(self.frame_content, text='Select Image :').grid(row=0, column=0, padx=5, pady=5,ipadx=5,ipady=5)
        self.process_button=Button(self.frame_content, text="Choose", command=self.processImage)
        self.process_button.grid(row=0, column=1, padx=5, pady=5, sticky='sw',columnspan=2)
        ttk.Label(self.frame_content, text='Class:').grid(row=1, column=0, padx=5,pady=5,ipadx=5,ipady=5)
        self.class_name = ttk.Entry(self.frame_content, width=48, font=('Arial', 10,'bold'))
        self.class_name.state(['readonly'])
        self.class_variable = StringVar()
        self.class_name.configure(textvariable=self.class_variable,foreground="Red")
        self.class_name.grid(row=1 , column=1 , padx=5,pady=5,ipadx=5,ipady=5 , sticky='sw')
        #self.text_comments = Text(self.frame_content, width = 50, height = 10, font = ('Arial', 10))
        self.text_comments=Canvas(self.frame_content, width=480, height=300)
        self.detect_imageFile=None
        self.text_comments.grid(row=3, column=0, columnspan=2, padx=5,pady=5,ipadx=5,ipady=5)
        #self.text_comments.configure(bg='#e1d8b9')
        #self.img_file=PhotoImage(file='Images//logo.png').subsample(1,1)
        #self.text_comments.create_image(480,300,image=self.img_file )
        #self.download_icon=PhotoImage(file='Images//download.png').subsample(8,8)
        ttk.Button(self.frame_content, text='Download', command=self.downloadImage
                  ).grid(row=4, column=0, padx=5, pady=5, sticky='e')
        ttk.Button(self.frame_content, text='Clear',command=self.clearData
                   ).grid(row=4, column=1, padx=5, pady=5, sticky='w')


        self.master.option_add('*tearOff', False)
        self.menu_bar = Menu(master)
        master.config(menu=self.menu_bar)
        self.menuLst = Menu(self.menu_bar)
        self.menu_bar.add_cascade(label='Menu', menu=self.menuLst)


        self.themes_menu = Menu(self.menuLst)
        try:
            self.theme = PhotoImage(file="Images//theme.png").subsample(20, 20)
        except:
            self.theme = PhotoImage(file="Images\theme.png").subsample(20, 20)
        self.menuLst.add_cascade(menu=self.themes_menu, label="Themes",image=self.theme,compound='left')
        try:
            self.aboutImage = PhotoImage(file="Images//info.png").subsample(20, 20)
        except:
            self.aboutImage = PhotoImage(file="Images\info.png").subsample(20, 20)
        self.about = Menu(self.menuLst)
        self.menuLst.add_cascade(menu=self.about, label="About",image=self.aboutImage, compound='left')
        #self.menuLst.add_command(label="About", command=self.infoClick,image=self.aboutImage,compound='left')
        try:
            self.default = PhotoImage(file="Images//default.png").subsample(10, 22)
            self.light = PhotoImage(file="Images//light.png").subsample(22, 18)
            self.dark = PhotoImage(file="Images//dark.png").subsample(20, 20)
            self.contri= PhotoImage(file="Images//contirbuters.png").subsample(10,10)
            self.soft=PhotoImage(file="Images//software.png").subsample(42,36)
        except:
            self.default = PhotoImage(file="Images\default.png").subsample(10, 22)
            self.light = PhotoImage(file="Images\light.png").subsample(22, 18)
            self.dark = PhotoImage(file="Images\dark.png").subsample(20, 20)
            self.contri = PhotoImage(file="Images\contirbuters.png").subsample(10, 10)
            self.soft = PhotoImage(file="Images\software.png").subsample(42, 36)
        # Add theme options to the "Themes" menu
        self.themes_menu.add_command( label='Default', image=self.default, compound='left', command=lambda: self.change_theme('Default'))
        self.themes_menu.add_command(label='Light', image=self.light, compound='left', command=lambda: self.change_theme('Light'))
        self.themes_menu.add_command(label='Dark',image=self.dark, compound='left', command=lambda: self.change_theme('Dark'))
        self.about.add_command(label='Software', image=self.soft, compound='left', command=lambda:self.infoClick('Software'))
        self.about.add_command(label='Contributers', image=self.contri, compound='left', command=lambda: self.infoClick('Contributers'))

    def processImage(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        #self.class_variable.set("Sk_class")
        if(image_path!=""):
            file_=imageDetect(self.master, image_path, self.class_variable, self.text_comments)
            if file_!=None:
                self.detect_imageFile =file_



    def clearData(self):
        self.class_variable.set('')
        self.text_comments.delete(ALL)
        self.detect_image_item = None



    def infoClick(self, kind):
        clickInfo(self.master,kind)

    def change_theme(self, theme):
        changeTheme(theme, self.style, self.master, self.text_comments)

    def downloadImage(self):
        if self.detect_imageFile is not None:
            current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = '_'.join(self.class_variable.get().split())
            default_filename = default_filename+"_"+current_datetime+".jpg"
            destination_path = filedialog.asksaveasfilename(defaultextension='.jpg',
                                                            filetypes=[("JPEG files", "*.jpg")],
                                                            initialfile=default_filename)
            if destination_path:
                try:
                    path="Detections//image.jpg"
                    shutil.copy(path, destination_path)
                    print("Image downloaded successfully!")
                except Exception as e:
                    print("An error occurred while downloading the image:", str(e))
        else:
            print("No image available to download.")
