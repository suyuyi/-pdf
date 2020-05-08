#C:\Users\song_xinbai\Downloads\19-20春季学期资料\结题报告
import re,requests,time,os,img2pdf,threading,_thread,sys
import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox
def single_img_download(path,url):
    f = open(path,"wb")
    f.write(requests.get(url).content)
    f.close()
class myThread (threading.Thread):
    def __init__(self, path,url):
        threading.Thread.__init__(self)
        self.path = path
        self.url = url
    def run(self):
        single_img_download(self.path, self.url)
class myThread2(threading.Thread):
    def __init__(self, path, num):
        threading.Thread.__init__(self)
        self.path = path
        self.num = num
    def run(self):
        download_convert_mul(self.path, self.num)
def download_img(path,ratify_no):
    url="http://output.nsfc.gov.cn/report/"+str(ratify_no)[:2]+"/"+str(ratify_no)+"_"
    i=1
    thread_wait=[]
    while(requests.get(url+str(i)+".png").status_code!=404):
        s_path=path+"\\"+str(i)+".png"
        s_url=url+str(i)+".png"
        thread=myThread(s_path,s_url)
        thread.start()
        thread_wait.append(thread)
        i+=1
    for t in thread_wait:
        t.join()
    print("download finished")
def img_to_pdf(path):
    img_list=[]
    if len(os.listdir(path))>0:
        for i in range(1,len(os.listdir(path))+1):
            img_name=path+"\\"+str(i)+".png"
            img_list.append(img_name)
        f=open(path+"\\result.pdf","wb")
        pdf_bytes=img2pdf.convert(img_list)
        f.write(pdf_bytes)
        return True
    else:
        return False
def download_convert_mul(path,ratify_no):
    download_img(path,ratify_no)
    result=img_to_pdf(path)
    if result:
        tkinter.messagebox.showinfo(title="Info", message="目标文件：" + str(ratify_no) + "下载完毕")
    else:
        tkinter.messagebox.showerror(title="Error", message="目标文件：" + str(ratify_no) + "下载失败")
def finished(status,threads):
    for t in threads:
        t.join()
    tkinter.messagebox.showinfo(title="Info", message="目标文件全部已完成下载")
    status.set("空闲")
window = tk.Tk()
window.title('国家自然科学基金共享服务网下载工具')
window.geometry('600x400')
try:
    canvas = tk.Canvas(window, width=600, height=135, bg='white')
    image_file = tk.PhotoImage(file=r'17.png')
    image = canvas.create_image(300, 30, anchor='n', image=image_file)
    canvas.pack(side='top')
except BaseException:
    tk.Label(window, text='无法加载图片', font=('Arial', 20)).pack()
tk.Label(window, text='默认为当前文件所在路径，请输入编号/网址，然后点击下载', font=('Arial', 14)).pack()
tk.Label(window, text='Path:', font=('Arial', 14)).place(x=10, y=170)
tk.Label(window, text='No.:', font=('Arial', 14)).place(x=10, y=210)
tk.Label(window, text='Status:', font=('Arial', 14)).place(x=10, y=250)
path_str = tk.StringVar()
path_str.set(sys.path[0])
path_input = tk.Entry(window, textvariable=path_str, font=('Arial', 14))
path_input.place(width=500,x=80, y=170)
num_str = tk.StringVar()
# num_str.set(60873261)
num_input = tk.Entry(window, textvariable=num_str, font=('Arial', 14))
num_input.place(width=500,x=80, y=210)
status = tk.StringVar()
status.set('空闲')
status_output = tk.Entry(window, textvariable=status, font=('Arial', 14))
status_output.place(width=500,x=80, y=250)
def download():
    path = path_input.get()
    # path_str.set("")
    num_raw = num_input.get()
    num_str.set("")
    num_raw_list=str(num_raw).split('、')
    num_list=[]
    for i in num_raw_list:
        match_result_url=re.match(r'^http://output.nsfc.gov.cn/conclusionProject/([0-9]+)',i)
        match_result_num=re.match(r'(^[0-9]+)',i)
        if(match_result_url):
            num_list.append(match_result_url.group(1))
        if(match_result_num):
            num_list.append(match_result_num.group(1))
    thread_wait=[]
    for num in num_list:
        # print(str(num)+'\n')
        if(requests.get("http://output.nsfc.gov.cn/conclusionProject/"+str(num)).status_code!=200):
            tkinter.messagebox.showerror(title="Error",message="无法打开http://output.nsfc.gov.cn/conclusionProject/"+str(num))
            continue
        if(os.path.exists(path+"\\"+str(num))):
            tkinter.messagebox.showerror(title="Error",message="目标文件已存在：" + path+"\\"+str(num))
            continue
        try:
            dir_path=path+"\\"+str(num)
            os.makedirs(dir_path)
            thread=myThread2(dir_path,num)
            thread.start()
            status.set(num+"开始下载")
            thread_wait.append(thread)
        except BaseException:
            tkinter.messagebox.showerror(title="Error",message="无法创建路径" + str(dir_path))
tk.Label(window, text='注意：下载多个文件时，请用‘、’分割编号', font=('Arial', 10)).place(y=330)
btn_login = tk.Button(window, text='下载', command=download)
btn_login.place(width=50,x=275, y=290)
window.mainloop()