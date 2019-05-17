from Application import Application

app = Application()

# 设置窗口标题
app.master.title('拼图')
# 设置窗口大小固定
app.master.resizable(width=False, height=False)
# 设置窗口长800，宽650，位置在（50,50）
app.master.geometry('800x650+50+50')

app.mainloop()

