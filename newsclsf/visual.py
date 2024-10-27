# coding: UTF-8

#编写一个用户登录界面和注册界面

import tkinter as tk
import tkinter.messagebox
import pickle
from tkinter.filedialog import askopenfilename

# 分类函数要import的东西
import torch
import numpy as np
from need.predicate import predicate_one  # 对单条文本进行分类用到的函数
from need.predicate import predicate_excel  # 对Excel文件进行分类用到的函数
import need.predicate_config as x

#实例化object,建立窗口window
window = tk.Tk()

#给窗口的可视化取名
window.title('新闻分类')

# window.resizable(0, 0) #阻止Python GUI的大小调整
#窗口大小设置
window.geometry('800x450')

#加载wellcome image
canvas = tk.Canvas(window, width = 800, height = 245,bg = 'Darkcyan')
image_file = tk.PhotoImage(file='logo.gif')  #加载logo图片
image = canvas.create_image(400, 0, anchor = 'n', image = image_file)
canvas.pack(side = 'top')
#tk.Label(window, text = '欢迎使用',font = ('宋体',20)).pack()

#用户信息
tk.Label(window, text='用户名：', font=('宋体',20)).place(x=160,y=290)
tk.Label(window, text='密码：', font=('宋体',20)).place(x=160,y=330)

#用户登录输入框entry
#用户名
var_usr_name = tk.StringVar()
var_usr_name.set('')
entry_usr_name = tk.Entry(window, textvariable = var_usr_name,font = ('宋体',20))
entry_usr_name.place(x=260,y=290)
#用户密码
var_usr_pwd = tk.StringVar()
var_usr_pwd.set('')
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, font=('宋体', 20), show='*')
entry_usr_pwd.place(x=260,y=330)

# 定义用户登录功能
def usr_login():
    # 这两行代码获取用户输入的usr_name和usr_pewd
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()

    #这里设置异常捕获，当我们第一次访问用户信息文件时是不存在的，所以这里设置异常捕获
    #中间的两行就是我们的匹配，即程序将输入的信息和文件中的信息匹配

    try:
        with open('usrs_info.pickle','rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        #这里就是我们没有读到‘usr_file’时，程序会创建一个usr_file这个文件，
        #并将管理员的用户和密码写入，即用户名为admin，密码为admin
        with open('usrs_info.pickle','wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)
            usr_file.close()    #必须先关闭，否则pickle.load()会出现EOFError: Ran out of input
    
    #如果用户名和密码与文件中的匹配成功，则会登录成功，并跳出弹窗登陆成功
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            # tkinter.messagebox.showinfo(title='欢迎', message = '登录成功！')
            news_window()         # 进入分类界面
        else:   #如果用户名匹配成功而密码输入错误，则弹出密码错误
                tkinter.messagebox.showerror(message='密码错误，请重新输入！')
    else:
        is_sign_up = tkinter.messagebox.askyesno('欢迎','你还未注册，是否现在注册？')   # 如果发现用户名不存在
        # 提示是否需要注册新用户
        if is_sign_up:
            usr_sign_up()
    

# 定义用户注册功能
def usr_sign_up():
    def sign_to_news_classificaation():
        # 以下三行就是获取我们注册时所输入的信息
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()
 
        # 这里是打开我们记录数据的文件，将注册信息读出
        with open('usrs_info.pickle', 'rb') as usr_file:
            exist_usr_info = pickle.load(usr_file)
        # 这里就是判断，如果两次密码输入不一致，则提示两次输入密码不一致！
        if np != npf:
            tkinter.messagebox.showerror('错误', '两次输入密码不一致！')
 
        # 如果用户名已经在我们的数据文件中，则提示用户名已存在
        elif nn in exist_usr_info:
            tkinter.messagebox.showerror('错误', '用户名已存在')
 
        # 最后如果输入无以上错误，则将注册输入的信息记录到文件当中，并提示注册成功，然后销毁窗口。
        else:
            exist_usr_info[nn] = np
            with open('usrs_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tkinter.messagebox.showinfo('欢迎', '注册成功!')
            # 然后销毁窗口。
            window_sign_up.destroy()
 
    # 定义长在窗口上的窗口
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('300x200')
    window_sign_up.title('注册窗口')
 
    new_name = tk.StringVar()  # 将输入的注册名赋值给变量
    new_name.set('')  # 将最初显示定为空
    tk.Label(window_sign_up, text='用户名: ').place(x=10, y=10)  # 将`User name:`放置在坐标（10,10）。
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)  # 创建一个注册名的`entry`，变量为`new_name`
    entry_new_name.place(x=130, y=10)  # `entry`放置在坐标（150,10）.
 
    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='密码: ').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=130, y=50)
 
    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='确认密码: ').place(x=10, y=90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=130, y=90)
 
    # 下面的 sign_to_news_classificaation
    btn_comfirm_sign_up = tk.Button(window_sign_up, text='注册', command=sign_to_news_classificaation)
    btn_comfirm_sign_up.place(x=180, y=120)

#游客登录函数
def usr_trav_login():
    # tkinter.messagebox.showinfo('欢迎','游客登录成功！')
    news_window()

#登录和注册按钮
btn_login = tk.Button(window, text='登录',font = ('宋体',30) ,command=usr_login)
btn_login.place(x=560, y=290)
btn_sign_up = tk.Button(window, text='注册',font = ('宋体',20) ,command=usr_sign_up)
btn_sign_up.place(x=700, y=400)

#游客登录
btn_trav_login = tk.Button(window, text = '游客登录', font = ('宋体',20) ,command=usr_trav_login)
btn_trav_login.place(x = 500,y = 400)


#定义分类的窗口
def news_window():


    nwindow = tk.Tk()
    nwindow.title('新闻分类')
    nwindow.geometry('800x450')
    # nwindow.resizable(0, 0) # 阻止Python GUI的大小调整
    # 输入单条新闻的标签
    lone = tk.Label(nwindow, text='输入单条新闻文本：', font=('宋体', 14))
    lone.place(x=10, y=10)

    # 显示输入新闻的文本框
    tone = tk.Text(nwindow, height=20, width=76)
    tone.place(x=10, y=40)

    # 单条新闻分类的函数
    def oneNews():
        # tkinter.messagebox.showinfo('提示', '输出新闻类别')

        config = x.Config()
        np.random.seed(1)
        torch.manual_seed(1)
        torch.cuda.manual_seed_all(1)
        torch.backends.cudnn.deterministic = True  # 保证每次结果一样

        # predict

        try:
            text = tone.get("0.0", "end")
            # print('输出文本框内容' + text)
            text_dir = 'THUCNews/pre_news'
            excel_dir = 'THUCNews/data/test_4.xlsx'
            model = x.Model(config).to(config.device)
            pre_res = predicate_one(config, model, text)
            # predicate_nums(config,model,text_dir)
            # predicate_excel(config, model, excel_dir)
            return pre_res
        except tk.TclError:
            tkinter.messagebox.showerror("错误", '未输入新闻文本')

    # #定义分类结果显示的text框
    # lnote = tk.Label(nwindow,width = 8,text ='类结果为：',font = ('宋体',14))
    # lnote.place(x = 620,y=80 )
    lan = tk.Label(nwindow, text='分类结果为：', font=('宋体', 14))
    lan.place(x=560, y=80)

    # 分类的结果
    var_answer = tk.StringVar()

    # var_answer.set('类别')
    def print_answer():
        var_answer = oneNews()
        lan.config(text='分类结果为：' + var_answer)

    # 定义按钮，一按就对单条新闻进行分类并展示分类结果
    bone = tk.Button(nwindow, text='确认', bg='DarkCyan', font=('宋体', 14), command=print_answer)
    bone.place(x=560, y=40)

    # 提示批量输入新闻的标签
    lmuch = tk.Label(nwindow, text='批量输入新闻文本（本地上传文件）：', font=('宋体', 14))
    lmuch.place(x=10, y=350)

    # 批量上传文件的路径
    emuch = tk.Entry(nwindow, show=None, font=('Arial', 18), width=38)
    emuch.place(x=10, y=380)

    # 打开批量上传新闻的文件
    def openFile():  # 打开文档
        global filename
        filename = askopenfilename(title='选择一个Excel文件',
                                   filetypes=[('Excel', '*.xlsx'), ('All Files', '*')])  # 选择打开的文档(Excel)
        if filename == "":  # 如果没有选择文档则返回
            return

        # with open(filename,'r') as  fileObj:
        #     content = fileObj.read()      #读取文档内容
        #
        # #新建一个窗口显示读取的文档的内容
        # fileWindow = tk.Toplevel(nwindow)
        # fileWindow.geometry('400x400')
        # fileWindow.title('filename')
        # tFile = tk.Text(fileWindow,content)
        # tFile.pack()
        #
        # fileWindow.mainloop()
        emuch.delete(0, "end")
        emuch.insert(0, filename)  # 将文件路径表示在Entry中

    # #上传文件的函数
    # def up_file():
    #     # tkinter.messagebox.showinfo('提示','上传文件')
    #     openFile()

    # 按钮文件路径
    bmuch = tk.Button(nwindow, text='. . .', bg='DarkCyan', height=1, command=openFile)
    bmuch.place(x=520, y=380)

    # # 设置显示loading...表示正在运行分类中的标签
    # lLoad = tk.Label(nwindow, font=('宋体', 14))
    # lLoad.place(x=700, y=400)
    # # 设置显示loading...表示正在运行分类中

    # pb = Progressbar(nwindow, length=100, mode="indeterminate")
    # pb.pack(padx=5, pady=10)

    # 对Excel文件进行分类的函数
    def file_print_answer():
        # 对Excel文件进行分类时显示进度条
        # pbWindow = tk.Toplevel(nwindow)
        # pbWindow.title('正在对新闻进行分类')

        # 提示正在运行分类
        notLabel = tk.Label(nwindow, text='正在分类，请稍等...')
        notLabel.place(x=700, y=380)
        # pb["Maximal"] = 100
        # pb["value"] = 0

        # 进度条开始滚动
        # model_name = args.model  # bert
        # x = import_module('models.' + model_name)
        config = x.Config()
        np.random.seed(1)
        torch.manual_seed(1)
        torch.cuda.manual_seed_all(1)
        torch.backends.cudnn.deterministic = True  # 保证每次结果一样

        # predict
        excel_dir = filename
        model = x.Model(config).to(config.device)
        predicate_excel(config, model, excel_dir)

        # pb.stop()   # 进度条停止滚动
        # pb.destroy() # 删除进度条
        notLabel.destroy()  # 删除提示正在分类
        tkinter.messagebox.showinfo('提示', '分类完成，分类结果保存在原Excel文件')

    # 定义按钮，一按就对批量新闻进行分类并将结果保存至文件
    ban2 = tk.Button(nwindow, text='确认', bg='DarkCyan', font=('宋体', 13), command=file_print_answer)
    ban2.place(x=560, y=380)

    nwindow.mainloop()



window.mainloop()

