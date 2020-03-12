# -*- coding: utf-8 -*-
"""
Author: Eric.zhong
Contact: ericzhong2010@qq.com
Create Time: 2020/03/11
File: TraceFileAnalyser.py
Info: 10046 Trace File Analyser Tool
"""

import tkinter.filedialog
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from operator import itemgetter
from tkinter import scrolledtext

class MY_GUI():
    _tabs = ""
    _tab_view = ""
    _tab_text = ""

    def __init__(self, init_window_name):

        """
        窗口相关方法                                说明
        title()                                    设置窗口标题
        geometry("宽x高+x轴偏移+y轴便宜")           设置窗口大小和设置窗口在屏幕的位置
        maxsize(宽,高)                             拖拽时可以设置窗口最大的宽和高
        minsize(宽,高)                             拖拽时可以设置窗口最小的宽和高
        configure(bg="color")                      设置窗口背景颜色，也可以用16进制表示，详细查RGB色彩表
        resizable(True,True)                       设置是否更改窗口大小，第一个参数为宽，第二个为高；若固定窗口可以resizable(0,0)
        state("zoomed")                            最大化窗口
        iconify()                                  最小化窗口
        iconbitmap("xx.ico")                       更改默认窗口图标
        """
        self.init_window_name = init_window_name
        self.init_window_name.geometry('950x600')
        self.width = init_window_name.winfo_screenwidth()  # 获取屏幕宽度
        self.height = init_window_name.winfo_screenheight()  # 获取屏幕高度
        w = 950
        h = 680
        x = (self.width-w)/2
        y = (self.height-h)/2
        self.init_window_name.geometry("%dx%d+%d+%d" %(w,h,0,0))

        # 日志文件路径
        self.get_filepath = StringVar()
        #

    # 获得文件目录
    def get_file(self):
        self.filename = tkinter.filedialog.askopenfilename()
        self.get_filepath.set(self.filename)
        self.getlist(self.filename)

    # Notebook 绑定事件：双击关闭标签并返回[0]号标签
    def onRemoveClick(self,event):
        '''
        获得所选标签的tab_id
        item = self.tab_control.select()
        item = self.tab_control.index(item)
        '''
        item = self.tab_control.index("current")
        # 过滤[0]号标签不被删除
        if item != 0:
            self.tab_control.forget(item)
            self.tab_control.select(0)

    # Treeview绑定事件
    def onDBClick(self, event):
        # 获得所选Treeview项目与项目值
        for item in self.sqltrace_tree.selection():
            item_text = self.sqltrace_tree.item(item, "values")
        flag = True
        # 判断所选项目标签是否已经存在，存在则选中关联标签
        for idx,tabs in enumerate(self.tab_control.tabs()):
            if '编号 #'+item_text[0] in self.tab_control.tab(idx)['text']:
                self.tab_control.select(idx)
                flag = False
                break

        # 如果所选项目标签不存在，则新建标签并赋值
        if flag:
            tab = ttk.Frame(self.tab_control)
            self.tab_control.add(tab, text='编号 #'+item_text[0])
            self.tab_text = scrolledtext.ScrolledText(tab, width=128, height=20,font=("微软雅黑",9),background='#999999')  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
            self.tab_text.insert(INSERT, item_text[4].replace("#","\n"))
            self.tab_text.place(x=10, y=10)  # 滚动文本框在页面的位置
            self.tab_control.select(tab)
        return


    # 获得列表信息
    def getlist(self,filename):
        num = 0
        flag = True
        flag2 = False
        list_no = []
        list_exec = []
        list_fetch = []
        list_total = []
        list_sql = []
        list_overall = ""
        text2 = ""
        fo = open(self.filename, "r+")
        try:
            while True:
                text = fo.readline()
                # 文本为空则退出循环(空行也会有"\n"而非空，因此空则是读取数据到尾部)
                if text == '':
                    break
                if flag2:
                    break
                # 过滤日志头部的无效日志
                if flag:
                    if text.startswith("***********************************") == True:
                        num += 1
                        continue
                if num >= 2:
                    text2 = ""
                    while True:
                        # 根据此规则来定义每组数据的分割位置
                        if "************************************" in text:
                            break
                        # 获取OVERALL信息复制到[0]标签
                        if "OVERALL TOTALS" in text:
                            flag2 = True
                            while text.startswith("************************************")  != True:
                                list_overall = list_overall + text + ""
                                text = fo.readline()
                            self.tab_text.insert(INSERT,list_overall)
                            break
                        # 文本为空则退出循环(空行也会有"\n"而非空，因此空则是读取数据到尾部)
                        if text == '':
                            break
                        flag = False
                        text2 = text2 + text + ""
                        # 过滤Execute值并赋值到list_exec列表
                        if text.startswith("Execute") == True:
                            value = re.findall(
                                r'Execute \s+ ([0-9]\d*)\s+([0-9]\d*\.\d{2})\s+([0-9]\d*\.\d{2})\s+ ([0-9]\d*)\s+ ([0-9]\d*)\s+ ([0-9]\d*)\s+ ([0-9]\d*)',
                                text, re.M | re.I)
                            list_exec.append(float(value[0][2]))
                        # 过滤Fetch值并赋值到list_fetch列表
                        if text.startswith("Fetch") == True:
                            value2 = re.findall(
                                r'Fetch \s+ ([0-9]\d*)\s+([0-9]\d*\.\d{2})\s+([0-9]\d*\.\d{2})\s+ ([0-9]\d*)\s+ ([0-9]\d*)\s+ ([0-9]\d*)\s+ ([0-9]\d*)',
                                text, re.M | re.I)
                            list_fetch.append(float(value[0][2]))
                        text = fo.readline()
                    list_sql.append(text2)
                    list_total.append(float(value[0][2]) + float(value[0][2]))
                    list_no.append(num - 1)
                    num += 1
        finally:
            fo.close()
        self.treeview_sort_insert(list_no, list_exec, list_fetch, list_total, list_sql, 3, True)

    # 排序与输出到TreeView
    def treeview_sort_insert(self,list_no,list_exec,list_fetch,list_total,list_sql,key,reverse):
        self.Lists = list(zip(list_no,list_exec,list_fetch,list_total,list_sql))
        self.Lists = sorted(self.Lists, key=itemgetter(key), reverse=reverse)

        # 遍历输出到Treeview
        for index, lists_item in enumerate(self.Lists):
            tree_text = lists_item[4].replace("\n","#")
            self.sqltrace_tree.insert("", 'end',values=(index + 1,lists_item[1],lists_item[2],lists_item[3],tree_text))

    # Exit GUI cleanly
    def _quit(slef):
        win.quit()
        win.destroy()
        exit()

    # 设置窗口
    def set_init_window(self):
        # Add a title
        self.init_window_name.title("Trace File Analyser - 作者：Eric.zhong(ericzhong2010@qq.com)")

        # 创建frame容器
        '''
        TEXT 与 Button 相关
        '''
        self.labelframe = LabelFrame(width=930, height=60, text="日志文件")
        self.labelframe.grid(column=0, row=1, padx=5, pady=0)

        # 搜索文件并显示路径
        path = Entry(self.labelframe,width=128, textvariable=self.get_filepath).grid(column=1, row=1)
        file = Button(self.labelframe, text="打开", command=self.get_file).grid(column=2, row=1)

        '''
        Treeview 相关
        height = 显示行数
        show   = 
        columns=
        '''
        self.sqlframe = LabelFrame(width=910, height=100, text="SQL语句列表")
        self.sqlframe.grid(column=0, row=2, padx=5, pady=10)

        # 定义树形结构与滚动条
        self.sqltrace_tree = ttk.Treeview(self.sqlframe, height = 8, show="headings", columns=("a", "b", "c", "d", "e"))
        self.vbar = ttk.Scrollbar(self.sqlframe, orient=VERTICAL, command=self.sqltrace_tree.yview)
        self.sqltrace_tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.sqltrace_tree.column("a", width=30, anchor="center")
        self.sqltrace_tree.column("b", width=100, anchor="center")
        self.sqltrace_tree.column("c", width=100, anchor="center")
        self.sqltrace_tree.column("d", width=100, anchor="center")
        self.sqltrace_tree.column("e", width=580, anchor="w")

        self.sqltrace_tree.heading("a", text="No")
        self.sqltrace_tree.heading("b", text="Execute")
        self.sqltrace_tree.heading("c", text="Fetch")
        self.sqltrace_tree.heading("d", text="Total")
        self.sqltrace_tree.heading("e", text="Texts")

        self.sqltrace_tree.grid(row=5, column=0, sticky=NSEW)
        self.sqltrace_tree.bind("<Double-1>", self.onDBClick)
        self.vbar.grid(row=5, column=1, sticky=NS)

        '''
        Notebook 相关
        '''
        self.Tab_labelframe = LabelFrame(width=930, height=400)
        self.Tab_labelframe.grid(column=0, row=3, padx=5, pady=0)

        self.tab_control = ttk.Notebook(self.Tab_labelframe,width=930, height=360)

        self.tabs = ttk.Frame(self.tab_control)
        # textvariable参数是可以通过变量再次赋值，text参数是不可以再次赋值
        self.tab_control.add(self.tabs, text='OVERALL')
        self.tab_text = scrolledtext.ScrolledText(self.tabs, width=128, height=20,font=("微软雅黑",9),background='#999999')  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
        self.tab_text.place(x=10, y=10)  # 滚动文本框在页面的位置
        self.tab_control.pack(expand=1, fill='both')
        self.tab_control.bind("<Double-1>", self.onRemoveClick)


if __name__ == '__main__':
    # 创建tkinter实例
    # Create instance
    init_window = Tk()
    win = MY_GUI(init_window)

    win.set_init_window()
    init_window.mainloop()