from tkinter import ttk

# ﻿표 생성하기. colums는 컬럼 이름, displaycolums는 실행될 때 보여지는 순서다.
from WhereToUseDisasterAssistanceFund.GetData import *
from WhereToUseDisasterAssistanceFund.init import *
from WhereToUseDisasterAssistanceFund.getMapData import *

treeview = ttk.Treeview(root, columns=["one", "two", "three", "four", "구주소", "위도", "경도", ],
                        displaycolumns=["one", "two", "three"])
Induutype = set()
treelist = list()
GetDataFromURL(treelist, Induutype)
dong = set()


# 표에 데이터 삽입
def search():
    x = treeview.get_children()
    for item in x:
        treeview.delete(item)

    for i in range(len(treelist)):
        if treelist[i][0] is not None:
            if str(treelist[i][0]).__contains__(searchBar.get()) and str(treelist[i][1]).__contains__(sector.get()) \
                    and str(treelist[i][4]).__contains__(DetailType.get()):
                treeview.insert('', 'end', text=i, values=treelist[i], iid=str(i) + "번")


def inputData():
    x = treeview.get_children()
    for item in x:
        treeview.delete(item)
    for i in range(len(treelist)):
        if treelist[i][0] is not None:
            treeview.insert('', 'end', text=i, values=treelist[i], iid=str(i) + "번")
    return treeview


# 스크롤바
treeview = inputData()
vbar = Scrollbar(treeview, orient=VERTICAL)
vbar.pack(side=RIGHT, fill=Y)
vbar.config(command=treeview.yview)
# 표와 스크롤바 연동
treeview.config(yscrollcommand=vbar.set)
treeview.pack(side=BOTTOM, expand=True, fill=BOTH)
# Frame
searchFrame = Frame(root)
searchFrame.pack(side=BOTTOM, expand=FALSE, fill=X)
# 검색버튼
searchBar = Entry(searchFrame)
restartButton = Button(searchFrame, text="리셋", command=inputData)
restartButton.pack(side=RIGHT, expand=FALSE, fill=X)

l1 = Button(searchFrame, text="검색", command=search)
l1.pack(side=RIGHT, expand=FALSE, fill=X)

# 검색 창

searchBar.pack(side=RIGHT, expand=TRUE, fill=X)
# 콤보박스 부분 구현 - 업종
sector = ttk.Combobox(searchFrame, width=12, textvariable=str)
templist = list()
templist.append("")
templist += list(Induutype)
sector['values'] = templist
sector.current(0)
sector.pack(side=RIGHT, expand=FALSE, fill=X)
# 동 콤보박스
dongSplited = list()
dongList = set()
for i in range(len(treelist)):
    if treelist[i][0] is not None:
        dongSplited = treelist[i][4].split()
        if len(dongSplited) >= 2 and str(dongSplited[2]).__contains__("동"):
            dongList.add(dongSplited[2])
dongList = list(dongList)
dongList.sort()
dongList.insert(0, "")
DetailType = ttk.Combobox(searchFrame, width=10, textvariable=str)
DetailType['values'] = dongList
DetailType.pack(side=RIGHT, expand=FALSE, fill=X)
DetailType.current(0)

# 지도
# m_image = showMap(37.4387767330, 126.7820485341)  # 임의의 값, 검색 기능 구현 후 수정
# label = Label(root, image=m_image, height=600, width=800)
# label.pack(side=TOP, expand=True, fill=BOTH)

# 각 컬럼 설정. 컬럼 이름, 컬럼 넓이, 정렬 등
treeview.column("#0", width=50, )
treeview.heading("#0", text="번호", anchor="center")

treeview.column("#2", width=200, anchor="center")
treeview.heading("two", text="가게이름", anchor="center")

treeview.column("#1", width=200, anchor="center")
treeview.heading("one", text="업종명", anchor="center")

treeview.column("#3", width=300, anchor="center")
treeview.heading("three", text="주소", anchor="center")

treeview.heading("구주소", text="구주소", anchor="center")
treeview.heading("위도", text="위도", anchor="center")
treeview.heading("경도", text="경도", anchor="center")


# init(데이터 불러오고 디스플레이 완료)


# 선택시
def selected(e):
    selectedItem = treeview.item(treeview.selection())['values']
    print(selectedItem)


treeview.bind("<Double-1>", selected)
