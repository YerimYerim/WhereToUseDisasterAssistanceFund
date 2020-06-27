from tkinter import ttk

# ﻿표 생성하기. colums는 컬럼 이름, displaycolums는 실행될 때 보여지는 순서다.
from WhereToUseDisasterAssistanceFund.GetData import *
from WhereToUseDisasterAssistanceFund.init import *
from WhereToUseDisasterAssistanceFund.getMapData import *


class Main:
    def __init__(self, root):
        self.infoTreeview = ttk.Treeview(root, columns=["one", "two", "three", "four", "구주소", "위도", "경도", ],
                                    displaycolumns=["one", "two", "three"])
        self.typeList = set()
        self.treelist = list()
        GetDataFromURL(self.treelist, self.typeList)
        self.dong = set()
        self.searchFrame = Frame(root)
        self.infoTreeview = self.inputData()
        self.vbar = Scrollbar(self.infoTreeview, orient=VERTICAL)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.vbar.config(command=self.infoTreeview.yview)
        # 표와 스크롤바 연동
        self.infoTreeview.config(yscrollcommand=self.vbar.set)
        self.infoTreeview.pack(side=BOTTOM, expand=True, fill=BOTH)
        # 각 컬럼 설정. 컬럼 이름, 컬럼 넓이, 정렬 등
        self.infoTreeview.column("#0", width=50, )
        self.infoTreeview.heading("#0", text="번호", anchor="center")

        self.infoTreeview.column("#2", width=200, anchor="center")
        self.infoTreeview.heading("two", text="가게이름", anchor="center")

        self.infoTreeview.column("#1", width=200, anchor="center")
        self.infoTreeview.heading("one", text="업종명", anchor="center")

        self.infoTreeview.column("#3", width=300, anchor="center")
        self.infoTreeview.heading("three", text="주소", anchor="center")
        self.infoTreeview.bind("<Double-1>", self.selected)
        # 검색버튼
        self.searchBar = Entry(self.searchFrame)
        self.restartButton = Button(self.searchFrame, text="리셋", command=self.inputData)
        self.searchButton = Button(self.searchFrame, text="검색", command=self.search)

        # 콤보박스 부분 구현 - 업종
        self.typeComboBox = ttk.Combobox(self.searchFrame, width=12, textvariable=str)
        typeList = list(self.typeList)
        typeList.sort()
        typeList.insert(0, "")
        self.typeComboBox['values'] = typeList
        self.typeComboBox.current(0)

        # 동 콤보박스
        dongName = list()
        dongList = set()
        for i in range(len(self.treelist)):
            if self.treelist[i][0] is not None:
                dongName = self.treelist[i][4].split()
                if len(dongName) >= 2 and str(dongName[2]).__contains__("동"):
                    dongList.add(dongName[2])
        dongList = list(dongList)
        dongList.sort()
        dongList.insert(0, "")
        self.dongComboBox = ttk.Combobox(self.searchFrame, width=10, textvariable=str)
        self.dongComboBox['values'] = dongList
        self.dongComboBox.current(0)

        # FRAME 내에 위치 잡기
        self.searchFrame.pack(side=BOTTOM, expand=FALSE, fill=X)
        self.restartButton.pack(side=RIGHT, expand=FALSE, fill=X)
        self.searchButton.pack(side=RIGHT, expand=FALSE, fill=X)
        self.searchBar.pack(side=RIGHT, expand=TRUE, fill=X)
        self.typeComboBox.pack(side=RIGHT, expand=FALSE, fill=X)
        self.dongComboBox.pack(side=RIGHT, expand=FALSE, fill=X)

    # 표에 데이터 삽입
    def search(self):
        x = self.infoTreeview.get_children()
        for item in x:
            self.infoTreeview.delete(item)

        for i in range(len(self.treelist)):
            if self.treelist[i][0] is not None:
                if str(self.treelist[i][0]).__contains__(self.searchBar.get()) and str(self.treelist[i][1]).__contains__(
                        self.typeComboBox.get()) \
                        and str(self.treelist[i][4]).__contains__(self.dongComboBox.get()):
                    self.infoTreeview.insert('', 'end', text=i, values=self.treelist[i], iid=str(i) + "번")

    def inputData(self):
        x = self.infoTreeview.get_children()
        for item in x:
            self.infoTreeview.delete(item)
        for i in range(len(self.treelist)):
            if self.treelist[i][0] is not None:
                self.infoTreeview.insert('', 'end', text=i, values=self.treelist[i], iid=str(i) + "번")
        return self.infoTreeview

    def selected(self,e):
        selectedItem = self.infoTreeview.item(self.infoTreeview.selection())['values']
        print(selectedItem)
