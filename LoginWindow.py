from tkinter import *
from tkinter import messagebox
from RegisterWindow import Register
from RequestServer import login, sendActivationEmail
from windowTool import setDefaultEmailAndPassword, getDefaultEmailAndPassword, setLoginWindowOpen


class LoginWindow(object):

    def closeLoginWindow(self):
        setLoginWindowOpen(False)
        self.t.destroy()

    def loginEvent(self, event):
        print("登录")
        email = self.email_entry.get()
        password = self.password_entry.get()
        status = login(email, password)
        if status["status"] == 200:
            setDefaultEmailAndPassword(email, password)
            messagebox.showinfo(title="提示", message='登录成功')
        elif status["status"] == 701:
            messagebox.showerror(title="警告", message='邮箱不存在')
        elif status["status"] == 702:
            messagebox.showerror(title="警告", message='密码错误')
        elif status["status"] == 703:
            win = messagebox.askquestion(title="警告", message='用户未激活，是否激活')
            if win == "yes":
                e_status = sendActivationEmail(email)
                if e_status["status"] == 602:
                    messagebox.showerror(title="错误", message='邮件发送失败，请检查邮箱是否正确')
        setLoginWindowOpen(False)
        self.t.destroy()

    def registerEvent(self, event):
        print("注册")
        Register()

    def forgetPassword(self, event):
        print("忘记密码")

    def __init__(self):
        self.t = Tk()
        self.t.title("登录")
        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        width = 400
        height = 200
        screenwidth = self.t.winfo_screenwidth()
        screenheight = self.t.winfo_screenheight()
        rect = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.t.geometry(rect)
        self.t.resizable(False, False)
        self.t.protocol("WM_DELETE_WINDOW", self.closeLoginWindow)
        self.b = Button(self.t, text="登录")
        self.b2 = Button(self.t, text="注册")
        self.b3 = Button(self.t, text="忘记密码")
        self.b.place(relx=0.35, rely=0.7, anchor="center")
        self.b2.place(relx=0.48, rely=0.7, anchor="center")
        self.b3.place(relx=0.62, rely=0.7, anchor="center")
        self.b.bind("<ButtonRelease-1>", self.loginEvent)
        self.b2.bind("<ButtonRelease-1>", self.registerEvent)
        self.b3.bind("<ButtonRelease-1>", self.forgetPassword)

        # 创建输入框（show="*"设置输入后的掩码，为空的话不设掩码）
        self.email_entry = Entry(self.t, show='', font=('Arial', 14))
        self.password_entry = Entry(self.t, show='*', font=('Arial', 14))
        self.email_entry.insert(0, getDefaultEmailAndPassword()[0])
        self.password_entry.insert(0, getDefaultEmailAndPassword()[1])

        # 绑定位置（0.5相当于整长的一半）
        self.email_entry.place(relx=0.5, rely=0.35, anchor="center")
        self.password_entry.place(relx=0.5, rely=0.5, anchor="center")
        self.uLabel = Label(self.t, text="用户名")
        self.pLabel = Label(self.t, text="密码")
        self.uLabel.place(relx=0.1, rely=0.35, anchor="center")
        self.pLabel.place(relx=0.1, rely=0.5, anchor="center")

        self.t.mainloop()


if __name__ == "__main__":
    LoginWindow()
