import tkinter as tk
from tkinter import TRUE, BOTTOM, FALSE, BOTH

from WhereToUseDisasterAssistanceFund.introScene import introScene


class SceneManager(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("경기 지역화폐가맹점 검색 어플리케이션")
        self.geometry("1000x800+100+100")
        self.resizable(TRUE, TRUE)
        self.configure(bg='white')
        self._frame = None
        self.switch_frame(introScene)
        self._frame.pack()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side=BOTTOM, expand=TRUE, fill=BOTH)