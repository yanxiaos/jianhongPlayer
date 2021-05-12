from tkinter import *
from tkinter import messagebox
from RequestServer import register


class Register(object):

    def checkPassword(self, password):
        if " " in password:
            messagebox.showerror(title="错误", message='密码不能包含空格')
            return
        else:
            for i in password:
                if u'\u4e00' <= i <= u'\u9fff':
                    messagebox.showerror(title="错误", message='密码不能包含汉字')
                    return
                else:
                    pass
        if 8 <= len(password) <= 16:
            pass
        else:
            messagebox.showerror(title="错误", message='密码不不在规定长度')
            return
        return "ok"

    def register(self, event):
        username = self.userEntry.get()
        email = self.emailEntry.get()
        password = self.passwordEntry.get()
        confirmPassword = self.confirmPasswordEntry.get()
        if 5 <= len(username) <= 16:
            if self.checkPassword(password) == "ok":
                if password == confirmPassword:
                    status = register(username, email, password)["status"]
                    print(status)
                    if status == 201:
                        messagebox.showinfo(title="提示", message="激活链接已发送至邮箱%s，请点击激活" % email)
                        self.t2.destroy()
                    elif status == 601:
                        messagebox.showerror(title="错误", message="邮箱已存在")
                    elif status == 602:
                        messagebox.showerror(title="错误", message="邮件发送失败，请检查邮箱是否正确")
                else:
                    messagebox.showerror(title="错误", message='两次输入密码不一致')
        else:
            messagebox.showerror(title="错误", message='用户名不在规定长度')


    def __init__(self):
        self.t2 = Tk()
        self.t2.title("注册")
        self.t2.resizable(False, False)
        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        width = 500
        height = 300
        screenwidth = self.t2.winfo_screenwidth()
        screenheight = self.t2.winfo_screenheight()
        rect = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.t2.geometry(rect)

        # 创建文本
        self.userLabel = Label(self.t2, text="用户名")
        self.emailLabel = Label(self.t2, text="邮箱")
        self.passwordLabel = Label(self.t2, text="密码")
        self.confirmPasswordLabel = Label(self.t2, text="确认密码")
        # 创建输入框（show="*"设置输入后的掩码，为空的话不设掩码）
        self.userEntry = Entry(self.t2, show='', font=('Arial', 10))
        self.emailEntry = Entry(self.t2, show='', font=('Arial', 10))
        self.passwordEntry = Entry(self.t2, show='*', font=('Arial', 10))
        self.confirmPasswordEntry = Entry(self.t2, show='*', font=('Arial', 10))
        # 提示文本
        self.userTips = Label(self.t2, text="请输入5 - 16个字符", font=('楷体', 8))
        self.passwordTips = Label(self.t2, text="请输入8 - 16位密码", font=('楷体', 8))

        # 注册按钮
        self.rb = Button(self.t2, text="注册", bg="green")

        # 绑定位置（0.5相当于整长的一半）
        self.userLabel.place(relx=0.23, rely=0.12, anchor="center")
        self.emailLabel.place(relx=0.23, rely=0.3, anchor="center")
        self.passwordLabel.place(relx=0.23, rely=0.48, anchor="center")
        self.confirmPasswordLabel.place(relx=0.23, rely=0.66, anchor="center")

        self.userEntry.place(relx=0.5, rely=0.12, anchor="center", width=200, height=25)
        self.emailEntry.place(relx=0.5, rely=0.3, anchor="center", width=200, height=25)
        self.passwordEntry.place(relx=0.5, rely=0.48, anchor="center", width=200, height=25)
        self.confirmPasswordEntry.place(relx=0.5, rely=0.66, anchor="center", width=200, height=25)

        self.userTips.place(relx=0.5, rely=0.2, anchor="center")
        self.passwordTips.place(relx=0.5, rely=0.56, anchor="center")

        self.rb.place(relx=0.5, rely=0.85, width=200, height=30, anchor="center")

        # 绑定事件
        self.rb.bind("<ButtonRelease-1>", self.register)

        self.t2.mainloop()


if __name__ == "__main__":
    Register()
