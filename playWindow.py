import shutil
from random import randint
from tkinter import *
import tkinter.messagebox
from tkinter.ttk import Combobox
import pygame, sys, time
from LoginWindow import LoginWindow
from MusicTool import getMusicPath
from RequestServer import getMusicList, setMusicCollection, getUserInformation
from myWindow import MyWindow
from playService import Service
from threading import Timer
from windowTool import *
import tkinter.filedialog



# <Button-1>: 鼠标左击事件
# <Button-2>: 鼠标中击事件
# <Button-3>: 鼠标右击事件
# <ButtonRelease-x>鼠标释放事件,x=[1,2,3],分别表示鼠标左中右操作
# <Double-Button-1>: 双击事件

class MainWindow(object):
    __MusicPlaying = False
    __MusicSilence = False
    __MusicStop = True
    __LastMusic = None
    __PlayingMusicList = []
    __PlayClick = False

    def playMusic(self, music_name):
        self.setNowPlayMp3Text("正在加载: %s" % music_name)
        music_path = getMusicPath("play", music_name)
        MainWindow.__PlayClick = False
        if music_path:
            music_status = self.service.play_music(music_path)
            if music_status:
                self.setNowPlayMp3Text("正在播放: %s" % music_name)
                self.button1["image"] = self.imgbutton1_2
                MainWindow.__MusicPlaying = True
                MainWindow.__MusicStop = False
                MainWindow.__LastMusic = music_name
                print(music_name)
            else:
                tkinter.messagebox.showerror(title="警告", message='文件不可播放')
                MainWindow.__LastMusic = None
        else:
            self.setNowPlayMp3Text("获取音乐失败")
            MainWindow.__LastMusic = None

    def getNextMusicName(self):
        play_mode = self.play_mode.get()
        if play_mode == "随机播放":
            while True:
                music_list_number = len(MainWindow.__PlayingMusicList)
                music_name = MainWindow.__PlayingMusicList[randint(0, music_list_number - 1)]
                if music_name != MainWindow.__LastMusic:
                    return music_name
        elif play_mode == "列表循环":
            music_list = MainWindow.__PlayingMusicList
            music_index = music_list.index(MainWindow.__LastMusic)
            music_next_index = music_index - 1
            if music_next_index < 0:
                music_next_index = len(music_list) - 1
            music_name = MainWindow.__PlayingMusicList[music_next_index]
            return music_name
        elif play_mode == "单曲循环":
            return MainWindow.__LastMusic

    def nextMp3(self):
        time.sleep(0.5)
        if not pygame.mixer.music.get_busy() and not MainWindow.__MusicStop and not MainWindow.__PlayClick:
            music_name = self.getNextMusicName()
            self.playMusic(music_name)
        thread = Timer(0.5, self.nextMp3)
        thread.setDaemon(True)  # 将这个线程设置为守护线程，当关闭窗口时主线程关闭，守护线程同时关闭
        thread.start()

    def setNowPlayMp3Text(self, name):
        if len(name) > 30:
            name = name[0:30]
        self.now_play_mp3['text'] = name

    def play(self, event):
        if self.now_play_mp3["text"].split(":")[0] != "正在加载":
            MainWindow.__PlayClick = True
            status = getUserInformation()
            if status["status"] == 200 or self.collection_mode.get() != "本地音乐":
                num = self.t1.curselection()  # 获得用户所选的下表位
                music_name = self.t1.get(num)  # 根据下标得到mp3的名字
                self.playMusic(music_name)
                collection_name = self.collection_mode.get()
                MainWindow.__PlayingMusicList = self.get_music_list(collection_name)["music"]
            elif status["status"] == 704:
                LoginWindow()

    def suspend(self, event):
        if pygame.mixer.music.get_busy():
            if MainWindow.__MusicPlaying:
                print("暂停")
                self.service.suspend_music()
                self.button1["image"] = self.imgbutton1
                MainWindow.__MusicPlaying = False
            else:
                print("播放")
                self.service.UNsuspend_music()
                self.button1["image"] = self.imgbutton1_2
                MainWindow.__MusicPlaying = True
        else:
            num = self.t1.curselection()  # 获得用户所选的下表位
            if num:
                self.play("event")

    def nextPlay(self, event):
        print("下一首")
        if pygame.mixer.music.get_busy():
            music_name = self.getNextMusicName()
            self.playMusic(music_name)
        else:
            collection_name = self.collection_mode.get()
            MainWindow.__PlayingMusicList = self.get_music_list(collection_name)["music"]
            music_name = self.getNextMusicName()
            self.playMusic(music_name)

    def stop(self, event):
        print("停止")
        self.service.stop_music()
        self.button1["image"] = self.imgbutton1
        self.setNowPlayMp3Text("")
        MainWindow.__MusicPlaying = False
        MainWindow.__MusicStop = True
        MainWindow.__PlayingMusic = None

    def silence(self, event):
        if MainWindow.__MusicSilence:
            print("取消静音")
            self.service.UNmute_music()
            self.button4["image"] = self.imgbutton4
            MainWindow.__MusicSilence = False
        else:
            print("静音")
            self.service.mute_music()
            self.button4["image"] = self.imgbutton4_2
            MainWindow.__MusicSilence = True

    def deleteMusic(self, event):
        print("delete")
        num = self.t1.curselection()  # 获得用户所选的下表位
        if num:
            collection = self.collection_mode.get()
            name = self.t1.get(num)  # 根据下标得到mp3的名字
            if collection == "本地音乐":
                win = tkinter.messagebox.askquestion(title="提示", message='是否从%s删除 %s' % (collection, name))
                if win == "yes":
                    os.remove("./download/{}.mp3".format(name))
                return
            elif collection == "默认收藏":
                collection = "Default"
            elif collection == "我喜欢":
                collection = "Love"

            win = tkinter.messagebox.askquestion(title="提示", message='是否从%s删除 %s' % (collection, name))
            if win == "yes":
                status = setMusicCollection("del", name, collection)
                if status["status"] == 400:
                    tkinter.messagebox.showerror(title="警告", message="删除失败")
            music_list = getMusicList("byCollection", collection)
            self.updateListBox(music_list)

    def myMine(self, event):
        status = getUserInformation()
        if status["status"] == 200 and not getMyWindowOpen():
            setMyWindowOpen(True)
            MyWindow()
        elif status["status"] in [704, 401]:
            if not getLoginWindowOpen():
                setLoginWindowOpen(True)
                LoginWindow()

    def volumeUp(self, event):
        self.service.volume_up()

    def volumeDown(self, event):
        self.service.volume_Down()

    def updateListBox(self, music_list):
        if music_list["status"] == 200:
            self.t1.delete(0, END)
            if music_list["music"]:
                for music in music_list["music"]:
                    self.t1.insert(0, music)
            else:
                self.t1.insert(0, "这个收藏夹啥都没有 （° ~ °）")
        elif music_list["status"] == 704:
            self.t1.delete(0, END)
            self.t1.insert(0, "请先登录")
            LoginWindow()

    def get_music_list(self, collection_name):
        if collection_name == "本地音乐":
            music_list = {"status": 200, "music": []}
            for root, dirs, files in os.walk("download"):
                for file in files:
                    if os.path.splitext(file)[1] == '.mp3':
                        file_name = file.split(".mp3")[0]
                        music_list["music"].append(file_name)
            return music_list
        elif collection_name == "默认收藏":
            collection_name = "Default"
        elif collection_name == "我喜欢":
            collection_name = "Love"
        music_list = getMusicList("byCollection", collection_name)
        return music_list

    def collectionModeEvent(self, event):
        collection_name = self.collection_mode.get()
        music_list = self.get_music_list(collection_name)
        if music_list["status"] in [401, 704]:
            LoginWindow()
        elif music_list["status"] == 200:
            self.updateListBox(music_list)

    def playModeEvent(self, event):
        print(self.play_mode.get())

    def closeMainWindow(self):
        win = tkinter.messagebox.askquestion(title="提示", message='是否关闭程序')
        if win == "yes":
            sys.exit()

    def clearCache(self, event):
        filepath = "cache/"
        cache_dir = os.path.join(os.curdir, 'cache')
        if os.path.isdir(cache_dir):
            del_list = os.listdir(filepath)
            for f in del_list:
                file_path = os.path.join(filepath, f)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                    except PermissionError:
                        pass

    def intoLocal(self, event):
        music_list = tkinter.filedialog.askopenfilenames()
        for music in music_list:
            music_name = music.split("/")
            new_music = "./download/{}".format(music_name[-1])
            shutil.copyfile(music, new_music)
            print("导入成功:", music_name)

    def __init__(self):
        self.service = Service()
        self.root = Tk()
        self.root.title("简音乐")
        # 设置窗口不可拉伸
        self.root.resizable(False, False)
        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        width = 365
        height = 319
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        rect = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(rect)
        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.closeMainWindow)
        # 创建画布，为主窗口添加背景图片
        self.get_image = tkinter.PhotoImage(file=r'image\主背景.png')
        self.frame = tkinter.Canvas(self.root)
        self.frame.create_image(150, 20, image=self.get_image)
        self.frame.create_line(0, 37, 370, 37, fill="#FFFFFF")
        self.frame.pack()

        # 创建按钮图片对象
        self.imgbutton1 = tkinter.PhotoImage(file=r'image\播放 .gif')
        self.imgbutton1_2 = tkinter.PhotoImage(file=r'image\暂停.gif')
        self.imgbutton2 = tkinter.PhotoImage(file=r'image\下一首.gif')
        self.imgbutton3 = tkinter.PhotoImage(file=r'image\停止.gif')
        self.imgbutton4 = tkinter.PhotoImage(file=r'image\不静音.gif')
        self.imgbutton4_2 = tkinter.PhotoImage(file=r'image\静音.gif')
        self.imgbutton5 = tkinter.PhotoImage(file=r'image\导入.gif')
        self.imgbutton6 = tkinter.PhotoImage(file=r'image\删除.gif')
        self.imgbutton7 = tkinter.PhotoImage(file=r'image\用户.gif')
        self.imgbutton8 = tkinter.PhotoImage(file=r'image\音量减.gif')
        self.imgbutton9 = tkinter.PhotoImage(file=r'image\音量加.gif')

        # 创建按钮对象
        self.button1 = Button(self.frame, image=self.imgbutton1, compound=tkinter.CENTER, height=20, width=35)
        self.button2 = Button(self.frame, image=self.imgbutton2, compound=tkinter.CENTER, height=20, width=35)
        self.button3 = Button(self.frame, image=self.imgbutton3, compound=tkinter.CENTER, height=20, width=35)
        self.button4 = Button(self.frame, image=self.imgbutton4, compound=tkinter.CENTER, height=20, width=35)
        self.button5 = Button(self.frame, image=self.imgbutton5, compound=tkinter.CENTER, height=20, width=35)
        self.button6 = Button(self.frame, image=self.imgbutton6, compound=tkinter.CENTER, height=20, width=35)
        self.button7 = Button(self.frame, image=self.imgbutton7, compound=tkinter.CENTER, height=20, width=35)
        self.button8 = Button(self.frame, image=self.imgbutton8, compound=tkinter.CENTER, height=20, width=35)
        self.button9 = Button(self.frame, image=self.imgbutton9, compound=tkinter.CENTER, height=20, width=35)
        # 创建收藏夹下拉框
        self.collection_mode = Combobox(self.frame, width=10, state="readonly")
        self.collection_mode["values"] = ("本地音乐", "默认收藏", "我喜欢")
        self.collection_mode.current(0)  # 选择第一个
        # 创建播放模式下拉框
        self.play_mode = Combobox(self.frame, width=10, state="readonly")
        self.play_mode["values"] = ("随机播放", "列表循环", "单曲循环")
        self.play_mode.current(0)  # 选择第一个
        # 创建列表对象     （       {模式：一次选一个}）
        self.t1 = Listbox(self.frame, {"selectmode": SINGLE}, height=12, width=50)
        # 创建文本
        self.now_play_mp3 = Label(self.frame, width=355, height=20, text="", image=self.get_image,
                                  compound=tkinter.CENTER)

        # 绑定按钮坐标（行，列，x间距，y间距）
        self.button1.grid(row=0, column=0, padx=5, pady=5)
        self.button2.grid(row=0, column=1, padx=5, pady=5)
        self.button3.grid(row=0, column=2, padx=5, pady=5)
        self.button4.grid(row=0, column=3, padx=5, pady=5)
        self.button5.grid(row=0, column=4, padx=5, pady=5)
        self.button6.grid(row=0, column=5, padx=5, pady=5)
        self.button7.grid(row=0, column=6, padx=5, pady=5)
        self.button8.grid(row=1, column=2, padx=5, pady=5)
        self.button9.grid(row=1, column=3, padx=5, pady=5)

        # 绑定下拉框
        self.collection_mode.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        self.play_mode.grid(row=1, column=5, padx=5, pady=5, columnspan=2)
        # 绑定列表坐标（行，列，x间距，y间距，占6列）
        self.t1.grid(row=2, column=0, padx=5, pady=1, columnspan=7)
        # 绑定文本
        self.now_play_mp3.grid(row=3, column=0, padx=5, pady=1, columnspan=7)

        # 绑定事件
        # 按钮绑定事件（鼠标左键释放类型，事件）
        self.button1.bind("<ButtonRelease-1>", self.suspend)
        self.button2.bind("<ButtonRelease-1>", self.nextPlay)
        self.button3.bind("<ButtonRelease-1>", self.stop)
        self.button4.bind("<ButtonRelease-1>", self.silence)
        # self.button5.bind("<ButtonRelease-1>", self.clearCache)
        self.button5.bind("<ButtonRelease-1>", self.intoLocal)
        self.button6.bind("<ButtonRelease-1>", self.deleteMusic)
        self.button7.bind("<ButtonRelease-1>", self.myMine)
        self.button8.bind("<ButtonRelease-1>", self.volumeDown)
        self.button9.bind("<ButtonRelease-1>", self.volumeUp)
        # 下拉框绑定事件
        self.collection_mode.bind("<<ComboboxSelected>>", self.collectionModeEvent)  # 绑定事件,(下拉列表框被选中时，绑定函数)
        self.play_mode.bind("<<ComboboxSelected>>", self.playModeEvent)  # 绑定事件,(下拉列表框被选中时，绑定函数)
        # 列表绑定事件
        self.t1.bind("<Double-Button-1>", self.play)
        self.collectionModeEvent("event")
        self.nextMp3()

        self.root.mainloop()


if __name__ == "__main__":
    main_window = MainWindow()
