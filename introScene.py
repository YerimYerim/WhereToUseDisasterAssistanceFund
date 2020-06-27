from tkinter import *

from WhereToUseDisasterAssistanceFund.ClassMain import MainScene


class introScene(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.image = PhotoImage(file="background.png")
        self.onButtonImage = PhotoImage(file="onimage.png")
        self.exitButtonImage = PhotoImage(file="exitimage.png")
        self.label = Label(self, image=self.image, bg='white')
        self.onButton = Button(self, image=self.onButtonImage, command=lambda: master.switch_frame(MainScene))
        self.exitButton = Button(self, image=self.exitButtonImage, command=self.exit)
        self.label.pack(side=TOP)
        self.onButton.pack(side=TOP)
        self.exitButton.pack(side=BOTTOM)

    def exit(self):
        exit()
