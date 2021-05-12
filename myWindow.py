from tkinter import *
from tkinter import messagebox
from MusicTool import getMusicPath
from RequestServer import getMusicList, getUserInformation, logout, setMusicCollection
from playService import Service
from windowTool import setMyWindowOpen


class MyWindow(object):

    def addDefault(self, event):
        num = self.t1.curselection()
        music_name = self.t1.get(num)
        result = messagebox.askokcancel(title='提示', message='你确定把%s加入默认收藏吗？' % music_name)
        if result:
            setMusicCollection("add", music_name, "Default")

    def addLove(self, event):
        num = self.t1.curselection()
        music_name = self.t1.get(num)
        result = messagebox.askokcancel(title='提示', message='你确定把%s加入我喜欢吗？' % music_name)
        if result:
            setMusicCollection("add", music_name, "Love")

    def downLoad(self, event):
        num = self.t1.curselection()
        music_name = self.t1.get(num)
        result = messagebox.askokcancel(title='提示', message='你确定要下载%s吗？' % music_name)
        if result:
            getMusicPath("download", music_name)

    def recommend(self, event):
        music_list = getMusicList("recommend")
        self.updateListBox(music_list)

    def search(self, event):
        music_name = self.entry1.get()
        music_list = getMusicList("byName", music_name)
        self.updateListBox(music_list)

    def play(self, event):
        num = self.t1.curselection()  # 获得用户所选的下表位
        music_name = self.t1.get(num)  # 根据下标得到mp3的名字
        music_path = getMusicPath("play", music_name)
        self.service.play_music(music_path)

    def Logout(self, event):
        logout()
        setMyWindowOpen(False)
        self.root.destroy()

    def closeMyWindow(self):
        setMyWindowOpen(False)
        self.root.destroy()

    def updateListBox(self, music_list):
        if music_list["status"] == 200:
            self.t1.delete(0, END)
            if music_list["music"]:
                for music in music_list["music"]:
                    self.t1.insert(0, music)
            else:
                self.t1.insert(0, "没有发现你要的音乐 （° ~ °）")
        elif music_list["status"] == 704:
            self.t1.delete(0, END)
            self.t1.insert(0, "请先登录")


    def __init__(self):
        self.service = Service()
        self.root = Tk()
        self.root.title("宏音乐")
        # 设置窗口不可拉伸
        #self.root.resizable(False, False)
        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        width = 1000
        height = 650
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        rect = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(rect)
        self.root.protocol("WM_DELETE_WINDOW", self.closeMyWindow)

        self.frameTop = Frame(self.root, width=1000, height=45, bg="#33CCFF")
        self.frameTop.pack(side=TOP)
        self.frameLeft = Frame(self.root, width=200, height=605, bg="#99FFFF")
        self.frameLeft .pack(side=LEFT)
        self.frameRight = Frame(self.root, width=800, height=605, bg="#CCFFFF")
        self.frameRight.pack(side=RIGHT)

        self.t1 = Listbox(self.frameRight, {"selectmode": SINGLE}, height=28, width=100)
        self.t1.place(relx=0.5, rely=0.55, anchor="center")
        music_list = getMusicList("recommend")
        self.updateListBox(music_list)
        self.t1.bind("<Double-Button-1>", self.play)

        self.entry1 = Entry(self.frameRight, font=('Arial', 14))
        self.entry1.place(relx=0.4, rely=0.07, anchor="center",width=400, height=40)
        self.BSearch = Button(self.frameRight, text="搜索")
        self.BSearch.place(relx=0.72, rely=0.07, anchor="center", width=60, height=38)
        self.BSearch.bind("<ButtonRelease-1>", self.search)

        self.button1 = Button(self.frameLeft, width=27, height=2, text="推荐歌曲", bg="#66FFFF")
        self.button1.place(relx=0.5, rely=0.05, anchor="center")
        self.button1.bind("<ButtonRelease-1>", self.recommend)
        self.button2 = Button(self.frameLeft, width=27, height=2, text="添加至默认收藏", bg="#66FFFF")
        self.button2.place(relx=0.5, rely=0.13, anchor="center")
        self.button2.bind("<ButtonRelease-1>", self.addDefault)
        self.button3 = Button(self.frameLeft, width=27, height=2, text="添加至我喜欢", bg="#66FFFF")
        self.button3.place(relx=0.5, rely=0.21, anchor="center")
        self.button3.bind("<ButtonRelease-1>", self.addLove)
        self.button4 = Button(self.frameLeft, width=27, height=2, text="下载这首歌", bg="#66FFFF")
        self.button4.place(relx=0.5, rely=0.29, anchor="center")
        self.button4.bind("<ButtonRelease-1>", self.downLoad)

        user = getUserInformation()
        self.nameLable = Label(self.frameTop, width=30, text=user["username"], bg="#33CCFF", font=('楷体', 14))
        self.nameLable.place(relx=0.1, rely=0.5, anchor="center")
        self.BLogout = Button(self.frameTop, width=10, text="退出登录", bg="#33CCFF")
        self.BLogout.place(relx=0.9, rely=0.5, anchor="center")
        self.BLogout.bind("<ButtonRelease-1>", self.Logout)


        self.root.mainloop()


if __name__ == "__main__":
    MyWindow()
