from tkinter import *

from WhereToUseDisasterAssistanceFund.ClassMain import Main


class introScene:
    def __init__(self, root):
        self.image = PhotoImage(file="background.png")
        self.onButtonImage = PhotoImage(file="onimage.png")
        self.exitButtonImage = PhotoImage(file="exitimage.png")
        label = Label(root, image=self.image, bg='white')
        onButton = Button(root, image=self.onButtonImage, command = self.mainScene)
        exitButton = Button(root, image=self.exitButtonImage, command = self.exit)
        label.pack(side=TOP)
        onButton.pack(side=TOP)
        exitButton.pack(side=BOTTOM)

    def exit(self):
        exit()

    def mainScene(self):
        pass
