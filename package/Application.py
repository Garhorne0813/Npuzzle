from tkinter import *
from PIL import Image, ImageTk, ImageGrab
from Run import Run
from MyThread import MyThread


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.v = IntVar()
        self.v.set(1)
        self.m = 3

        self.run = Run(self.m, self.m)
        self.run.init_aim()
        self.p = self.run.random_state()
        self.imagel = []
        self.image_list2 = []
        self.path = []
        self.create_widget()

    # 创建布局函数
    def create_widget(self):
        self.image = Image.open('lemon.jpg')
        self.fm1 = Frame(self)
        self.fm1.pack(side=LEFT, fill='y')
        self.show_pictures()

        self.fm2 = Frame(self)
        self.fm2.pack(side=RIGHT, fill='y', pady='100')

        size = [('3 * 3', 1), ('4 * 4', 2), ('5 * 5', 3)]
        for s, num in size:
            Radiobutton(self.fm2, text=s, value=num, variable=self.v, command=self.rb_ckecked).pack()

        self.btn_mess = Button(self.fm2, text='打乱', width=15, height=2, command=self.mess_callback)
        self.btn_mess.pack(padx=25, pady=10)
        self.btn_start = Button(self.fm2, text='开始排序', width=15, height=2, command=self.start_callback)
        self.btn_start.pack(padx=25, pady=10)
        self.text_statement = Label(self.fm2, text='本程序第一个方格为0，若算法中循环超过3000次仍计算不出，则终止算法', wraplength=140)
        self.text_statement.pack(padx=15, pady=10)
        self.str = StringVar()
        self.str.set('静止')
        self.text_condition = Label(self.fm2, textvariable=self.str)
        self.text_condition.pack(padx=25, pady=10)
        self.str2 = StringVar()
        self.str2.set('步数为：')
        self.text_info = Label(self.fm2, textvariable=self.str2)
        self.text_info.pack(padx=25, pady=10)

    def rb_ckecked(self):
        print(self.v.get())

    # “打乱”按钮的监听响应函数
    def mess_callback(self):
        k = self.v.get()
        if k == 1:
            self.m = 3
            hard = 150
        elif k == 2:
            self.m = 4
            hard = 50
        else:
            self.m = 5
            hard = 40
        self.run.set_mn(self.m, self.m, hard)
        self.run.init_aim()
        self.p = self.run.random_state()
        for widget in self.fm1.winfo_children():
            widget.destroy()
        self.show_pictures()
        self.str.set('静止')
        print(self.m)

    # “开始排序”按钮的监听响应函数
    def start_callback(self):
        print('开始')
        # self.text_condition.configure(text='开始')
        self.str.set('开始')
        th = MyThread(self.p, self.run)
        th.setDaemon(True)
        th.start()
        th.join()
        self.path = th.get_result()
        if self.path:
            self.printp()
            self.str.set('静止')
            step = th.get_Infor()
            self.str2.set('步数为：'+str(step))
            for i in self.path:
                print(i)
        else:
            self.str.set('计算不出来')

    # 裁剪图片函数
    @staticmethod
    def cut_image(image, m):
        width, height = image.size
        item_width = int(width / m)
        box_list = []
        for i in range(0, m):
            for j in range(0, m):
                box = (j * item_width, i * item_width, (j + 1) * item_width, (i + 1) * item_width)
                box_list.append(box)
        image_list = [image.crop(box) for box in box_list]
        return image_list

    # 显示图片函数
    def show_pictures(self):
        image_list = self.cut_image(self.image, self.m)

        self.image_list2.clear()
        self.imagel.clear()

        for im2 in image_list:
            self.image_list2.append(ImageTk.PhotoImage(im2))

        for i in range(0, self.m):
            for j in range(0, self.m):
                self.imagel.append(IntVar())
                self.imagel[i * self.m + j] = Label(self.fm1, width=600 / self.m, height=600 / self.m, image=self.image_list2[self.p.state[i * self.m + j]], borderwidth=3)
                self.imagel[i * self.m + j].grid(row=i, column=j)

    # 根据计算出的路径实现图片的移动函数
    def printp(self):
        # pic = ImageGrab.grab((self.winfo_y() + 70, self.winfo_x() + 90, self.winfo_y() + self.winfo_width() + 70,
        #                       230 + self.winfo_x() + self.winfo_height()))
        # pic.save(str(len(self.path)) + '.jpg')
        if not self.path:
            return
        pa = self.path[0]
        count = 0
        for i in self.imagel:
            i.config(imag=self.image_list2[pa[count]])
            count += 1
        self.path.remove(pa)
        self.fm1.after(200, self.printp)
