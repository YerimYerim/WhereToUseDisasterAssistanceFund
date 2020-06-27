from tkinter import ttk

# ﻿표 생성하기. colums는 컬럼 이름, displaycolums는 실행될 때 보여지는 순서다.
from WhereToUseDisasterAssistanceFund.GetData import *
from WhereToUseDisasterAssistanceFund.init import *
from WhereToUseDisasterAssistanceFund.getMapData import *

Induutype = set()

treeview = ttk.Treeview(root, columns=["one", "two", "three", "four", "구주소", "위도", "경도", ],
                        displaycolumns=["one", "two", "three"])
treeview.place(x=0, y=600)

type = ttk.Combobox(root, width=10, textvariable=str)
type['values'] = ('dd', 'ddd')
type.place(x=0, y=575)
type.current(0)

DetailType = ttk.Combobox(root, width=10, textvariable=str)
DetailType['values'] = ('dd', 'ddd')
DetailType.place(x=110, y=575)
DetailType.current(0)
treelist = list()
GetDataFromURL(treelist, Induutype)

# 콤보박스 부분 구현 - 업종
sector = ttk.Combobox(root, width=12, textvariable=str)
sector['values'] = list(Induutype)
sector.place(x=220, y=575)
sector.current(0)
business = sector.get()

# 스크롤바
vbar = Scrollbar(treeview, orient=VERTICAL)
vbar.pack(side=RIGHT, fill=Y)
vbar.config(command=treeview.yview)
treeview.config(yscrollcommand=vbar.set)
treeview.pack(side=BOTTOM, expand=True, fill=BOTH)

# 검색버튼
l1 = Button(root, text="검색")
l1.pack(side=BOTTOM, expand=FALSE, fill=X)

# 검색 창
e1 = Entry(root)
e1.place(x=350, y=575)

# 지도
m_zoom = 17  # 기본 확대값
m_image = showMap(37.4387767330, 126.7820485341, m_zoom)  # 임의의 값, 검색 기능 구현 후 수정

label = Label(root, image=m_image)
label.pack(side=TOP, expand=True, fill=BOTH)
label.place(x=0, y=0)

#

# 각 컬럼 설정. 컬럼 이름, 컬럼 넓이, 정렬 등
treeview.column("#0", width=50, )
treeview.heading("#0", text="번호", anchor="center")

treeview.column("#1", width=200, anchor="center")
treeview.heading("one", text="가게이름", anchor="center")

treeview.column("#2", width=200, anchor="center")
treeview.heading("two", text="업종명", anchor="center")

treeview.column("#3", width=300, anchor="center")
treeview.heading("three", text="주소", anchor="center")

treeview.heading("구주소", text="구주소", anchor="center")
treeview.heading("위도", text="위도", anchor="center")
treeview.heading("경도", text="경도", anchor="center")
# 표에 삽입될 데이터


# 표에 데이터 삽입
for i in range(len(treelist)):
    if treelist[i][0] is not None:
        treeview.insert('', 'end', text=i, values=treelist[i], iid=str(i) + "번")
# GUI 실행
