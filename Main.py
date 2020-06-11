import tkinter
import tkinter.ttk

# ﻿GUI창을 생성하고 라벨을 설정한다.
root=tkinter.Tk()
root.title("Students")
root.geometry("540x300+100+100")
root.resizable(False, False)

lbl = tkinter.Label(root, text="Class Notice")
lbl.pack()

# ﻿표 생성하기. colums는 컬럼 이름, displaycolums는 실행될 때 보여지는 순서다.
treeview=tkinter.ttk.Treeview(root, columns=["one", "two","three"], displaycolumns=["one","two","three"])
treeview.pack()

# 각 컬럼 설정. 컬럼 이름, 컬럼 넓이, 정렬 등
treeview.column("#0", width=100,)
treeview.heading("#0", text="index")

treeview.column("#1", width=100, anchor="center")
treeview.heading("one", text="name", anchor="center")

treeview.column("#2", width=100, anchor="center")
treeview.heading("two", text="score", anchor="center")

treeview.column("#3", width=70, anchor="center")
treeview.heading("three", text="rank", anchor="center")

# 표에 삽입될 데이터
treelist=[("Tom", 80, 3), ("Bani", 71, 5), ("Boni", 90, 2), ("Dannel", 78, 4), ("Minho", 93, 1)]

# 표에 데이터 삽입
for i in range(len(treelist)):
    treeview.insert('', 'end', text=i, values=treelist[i], iid=str(i)+"번")

# 슴겨진 항목
top=treeview.insert('', 'end', text="hidden index", iid="5번")
top_mid1=treeview.insert(top, 'end', text="5", values=["Timy", 0, 8], iid="5번-1")
top_mid2=treeview.insert(top, 0, text="6", values=["Ann", 35, 7], iid="5번-0")
top_mid3=treeview.insert(top, 'end', text="7", values=["Sany", 60, 6], iid="5번-2")

# GUI 실행
root.mainloop()