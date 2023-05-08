# coding=utf-8
# 使用OpenCV视频中提取帧图片并保存(cv2.VideoCapture)
import os
import cv2
import shutil
import time

import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import askdirectory


# 全局变量
VIDEO_PATH = 'videos/11.mp4'  # 视频地址
EXTRACT_FOLDER = 'pre_imgs'  # 存放帧图片的位置
EXTRACT_FREQUENCY = 1  # 帧提取频率

is_Hidden = True
var = ""
var1 = ""
path = ""

def create_main_windows():
    global rootWindow
    rootWindow = tk.Tk()
    rootWindow.title('GetImgs')
    rootWindow.geometry('777x555')

def create_label():
    global var
    var = tk.StringVar()
    var.set('click me and hidden')
    l = tk.Label(rootWindow, textvariable=var, bg='green', font=('Arial', 12), width=25, height=4)
    l.grid()
    pass

def select_path():
    # global path
    # path_ = askdirectory() #使用askdirectory()方法返回文件夹的路径
    # if path_ == "":
    #     path.get() #当打开文件路径选择框后点击"取消" 输入框会清空路径，所以使用get()方法再获取一次路径
    # else:
    #     path_ = path_.replace("/", "\\")  # 实际在代码中执行的路径为“\“ 所以替换一下
    #     path.set(path_)

    path_ = tk.filedialog.askopenfilename()
    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    # path_ = path_.replace("/", "\\\\")  # path设置path_的值
    # path_ = path_.replace("/", "\\")  # path设置path_的值
    path.set(path_)
    # path.set(os.path.abspath("."))
    # path.set(os.path.abspath(path_))

    global VIDEO_PATH
    VIDEO_PATH = path.get()
    print(path.get())


def open_dir():
    # global path
    dir = tk.filedialog.askdirectory()
    os.system('start ' + dir)
    #print(dir)

def open_file():
    # global path
    file_dir = os.path.dirname(path.get()+"\\")
    os.system('start ' + file_dir)
    #print(dir)

def buttons_listen():
    # global var1
    # var1 = tk.StringVar()
    # var1.set('hidden')
    # b = tk.Button(rootWindow, textvariable=var1, width=12, height=3, command=hidden_me)
    # b.grid()

    global path
    path = tk.StringVar()
    path.set(os.path.abspath("."))
    tk.Label(rootWindow, text="Switch Video to Images").grid(row=1, column=3)
    tk.Label(rootWindow, text=" Pls select video path:").grid(row=2, column=3)
    tk.Label(rootWindow, text=" Target Path: ").grid(row=3, column=2)
    tk.Entry(rootWindow, textvariable=path, state="readonly").grid(row=3, column=3, ipadx=150)

    button_select = tk.Button(rootWindow, text=' File Select', bg='gray', command=select_path).grid(row=3, column=11)
    #button_select.place(x=0, y=250, width=80, height=50)
    button_open = tk.Button(rootWindow, text=' Open Path', bg='gray', command=open_dir).grid(row=3, column=13)
    #button_open.place(x=80, y=250, width=80, height=50)

    # button_7 =tk.Button(rootWindow, text=' Switch ', bg='gray', command=lambda:extract_frames(VIDEO_PATH, EXTRACT_FOLDER, 1))
    # button_7.place(x=11, y=60, width=222, height=50)
    button_switch = tk.Button(rootWindow,  text=' Switch ', bg='red', command=lambda:extract_frames(VIDEO_PATH, EXTRACT_FOLDER, 1)).grid(row=3, column=15)

    button_resize = tk.Button(rootWindow, text='Img Resize', bg='green', command=img_resize).grid(row=6, column=13)
    button_rename = tk.Button(rootWindow, text='Img Rename', bg='grey', command=change_file_name).grid(row=6, column=15)
    pass

def hidden_me():
    global is_Hidden
    global var
    if is_Hidden == False:
        is_Hidden = True
        var.set('click me and hidden')
    else:
        is_Hidden = False
        var.set('')

def extract_frames(video_path, dst_folder, index):
    # 实例化视频对象
    video = cv2.VideoCapture(video_path)
    frame_count = 0

    # 递归删除之前存放帧图片的文件夹，并新建一个
    try:
        shutil.rmtree(EXTRACT_FOLDER)
    except OSError:
        pass
    os.mkdir(EXTRACT_FOLDER)

    while True:
        # 逐帧读取
        _, frame = video.read()
        if frame is None:
            break
        # 按照设置的频率保存图片
        if frame_count % EXTRACT_FREQUENCY == 0:
            # 设置保存文件名
            save_path = "{}/{:>03d}.jpg".format(dst_folder, index)
            # 保存图片
            cv2.imwrite(save_path, frame)
            index += 1  # 保存图片数＋1
        frame_count += 1  # 读取视频帧数＋1

    # 视频总帧数
    print(f'the number of frames: {frame_count}')
    # 打印出所提取图片的总数
    print("Totally save {:d} imgs".format(index - 1))

    # 计算FPS 方法一 get()
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')  # Find OpenCV version
    # (major_ver, minor_ver, subminor_ver) = (4, 5, 4)
    if int(major_ver) < 3:
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)  # 获取当前版本opencv的FPS
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else:
        fps = video.get(cv2.CAP_PROP_FPS)  # 获取当前版本opencv的FPS
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    # 计算FPS 方法二 手动计算 总帧数 / 总时间
    # new_vid = cv2.VideoCapture(video_path)
    # start = time.time()  # 开始时间
    # c = 0
    # while True:
    #     _, frames = new_vid.read()
    #     if frames is None:
    #         break
    #     c += 1
    # end = time.time()  # 结束时间
    # fps2 = c / (end - start)  # 总帧数 / 总时间
    # print(f'frames:{c}')
    # print(f'seconds:{end - start}')
    # print("Frames per second using frames / seconds : {0}".format(fps2))
    # new_vid.release()

    # 最后释放掉实例化的视频
    video.release()

def change_file_name():
    dir_path = "data_plus/"
    files = os.listdir(dir_path)  # 读取文件名

    n=0
    for i in files:
        #设置旧文件名（路径+文件名）
        oldname=os.path.join(dir_path,i)
        #设置新文件名

        n=n+1
        # newname=os.path.join(dir_path,'1'+str(n)+'.jpg')
        newname=os.path.join(dir_path, 'football_'+ str(n)+'.jpg')
        #用os模块中的rename方法对文件改名
        os.rename(oldname,newname)
        print(oldname,'======>',newname)


def img_resize():
    # path = 'work/voc_data/JPEGImages/' #原图像路径
    original_dir = 'imgs/' #原图像路径
    os.mkdir(r"data_plus") #创建新文件夹
    save_path = 'data_plus/'  # 修改后的图像路径
    files = os.listdir(original_dir)
    for file in files:
        img = cv2.imread(original_dir+ "/" + file)
        # img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 转化为灰度图
        try:
            # img = cv2.resize(img,(640,640))
            img = cv2.resize(img,(720,540))
            cv2.imwrite(save_path+"/"+str(file),img)
        except:
            continue

def main():
    create_main_windows()
    # create_label()
    buttons_listen()
    rootWindow.mainloop()

if __name__ == '__main__':
    main()


