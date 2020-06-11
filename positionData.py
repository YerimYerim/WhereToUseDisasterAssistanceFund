from tkinter import ttk

# ﻿표 생성하기. colums는 컬럼 이름, displaycolums는 실행될 때 보여지는 순서다.
from WhereToUseDisasterAssistanceFund.init import *

treeview = ttk.Treeview(root, columns=["one", "two", "three"], displaycolumns=["one", "two", "three"])
treeview.place(x=0, y=600)

type = ttk.Combobox(root, width=10, textvariable=str)
type['values'] = ('dd', 'ddd')
type.place(x=0, y=575)
type.current(0)

DetailType = ttk.Combobox(root, width=10, textvariable=str)
DetailType['values'] = ('dd', 'ddd')
DetailType.place(x=110, y=575)
DetailType.current(0)

# 콤보박스 부분 구현
sector = ttk.Combobox(root, width=9, textvariable=str)
sector['values'] = (
    '수원시', '용인시', '성남시', '부천시', '화성시', '안산시', '안양시', '평택시', '시흥시', '김포시', '광주시', '광명시', '군포시'
    , '하남시', '오산시', '이천시', '안성시', '의왕시', '양평군', '여주시', '과천시', '고양시', '남양주시', '파주시', '의정부시', '양주시'
    , '구리시', '포천시', '동두천시', '가평군', '연천군'
)
sector.place(x=220, y=575)
sector.current(0)
# 검색 부분 구현
l1 = Button(root, text="검색")
l1.place(x=480, y=565)
e1 = Entry(root)
e1.place(x=320, y=575)
# 각 컬럼 설정. 컬럼 이름, 컬럼 넓이, 정렬 등
treeview.column("#0", width=50, )
treeview.heading("#0", text="번호", anchor="center")

treeview.column("#1", width=200, anchor="center")
treeview.heading("one", text="가게이름", anchor="center")

treeview.column("#2", width=300, anchor="center")
treeview.heading("two", text="주소", anchor="center")

treeview.column("#3", width=200, anchor="center")
treeview.heading("three", text="전화번호", anchor="center")

# 표에 삽입될 데이터
treelist = [("Tom", 80, 3), ("Bani", 71, 5), ("Boni", 90, 2), ("Dannel", 78, 4), ("Minho", 93, 1)]

# 표에 데이터 삽입
for i in range(len(treelist)):
    treeview.insert('', 'end', text=i, values=treelist[i], iid=str(i) + "번")

# GUI 실행
