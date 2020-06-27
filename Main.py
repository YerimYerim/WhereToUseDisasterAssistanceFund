from WhereToUseDisasterAssistanceFund.ClassMain import Main
from tkinter import *

# ﻿GUI창을 생성하고 라벨을 설정한다.
from WhereToUseDisasterAssistanceFund.introScene import introScene

root = Tk()
root.title("경기 지역화폐가맹점 검색 어플리케이션")
root.geometry("1000x800+100+100")
root.resizable(TRUE, TRUE)
root.configure(bg = 'white')
mainScene = introScene(root)
root.mainloop()
