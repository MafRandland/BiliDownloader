"""
This is a downloader of videos on Bilibili
Presented by Maftert Studio
"""
from tkinter import *
from tkinter.ttk import *

import requests as re
from lxml import etree
from you_get import common


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widget()
        self.video_list = []
        self.num = 0

    def name_spider(self, url):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36 "
        }
        self.response = re.get(url=url, headers=self.headers)
        self.response.encoding = "utf-8"
        self.html_root = etree.HTML(self.response.text)
        self.title = self.html_root.xpath("//title/text()")
        return self.title[0]

    @staticmethod
    def get_quality(source):
        if source == "1080p":
            return "dash-flv"
        elif source == "720p":
            return "dash-flv720"
        elif source == "480p":
            return "dash-flv480"
        else:
            return "dash-flv360"

    def confirm_button(self):
        temp_dict = {"url": self.ent02.get(), "quality": self.get_quality(self.cbx01.get())}
        self.video_list.append(temp_dict)
        self.tree.insert("", 0, values=(self.num + 1, self.name_spider(temp_dict["url"]), self.cbx01.get()))
        self.window.destroy()

    def start_downloading(self):
        for video in self.video_list:
            common.any_download_playlist(url=video["url"], stream_id=video["quality"],
                                         info_only=False,
                                         output_dir=self.ent01.get(), merge=True)
        self.video_list.clear()

    def download_window(self):
        self.window = Tk()
        self.window.geometry("250x100")
        self.window.title("添加视频")
        self.lbl02 = Label(self.window, text="视频地址")
        self.lbl02.grid(column=0, row=0, sticky="w")
        self.ent02 = Entry(self.window, width=20)  # 视频地址输入框
        self.ent02.grid(column=1, row=0, sticky="w")
        self.lbl03 = Label(self.window, text="视频清晰度")
        self.lbl03.grid(column=0, row=1, sticky="w")
        self.cbx01 = Combobox(self.window, width=13)
        self.cbx01["values"] = ("360p", "480p", "720p", "1080p")
        self.cbx01.grid(column=1, row=1, sticky="w")
        self.btn02 = Button(self.window, text="确定", command=self.confirm_button)
        self.btn02.grid(column=1, row=2, sticky="s")
        self.window.mainloop()

    def create_widget(self):
        global add_video
        self.btn01 = Button(self, text="添加视频", command=self.download_window)  # 添加视频按钮
        self.btn01.grid(column=0, row=0, sticky="w")
        self.btn03 = Button(self, text="开始下载", command=self.start_downloading)
        self.btn03.grid(column=1, row=0, sticky="w")
        self.lbl01 = Label(self, text="保存地址:")
        self.lbl01.grid(column=0, row=1, sticky="w")
        self.ent01 = Entry(self, width=30)
        self.ent01.grid(column=1, row=1, sticky="w")
        self.y_scroll = Scrollbar(self, orient=VERTICAL)
        self.tree = Treeview(self, show="headings", height=7, yscrollcommand=self.y_scroll)
        self.tree["columns"] = ("编号", "标题", "画质")
        self.tree.column("编号", width=50)
        self.tree.heading("编号", text="编号", anchor="w")
        self.tree.heading("标题", text="视频标题", anchor="w")
        self.tree.heading("画质", text="视频画质", anchor="w")
        self.tree.grid(column=0, row=2, columnspan=3)


if __name__ == '__main__':
    root = Tk()
    root.geometry("500x250")
    root.title("Bilibili视频下载器v1.2.3——Presented by Maftert Studio")
    app = Application(master=root)
    root.mainloop()
