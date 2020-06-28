from threading import Thread
from tkinter import ttk

# ﻿표 생성하기. colums는 컬럼 이름, displaycolums는 실행될 때 보여지는 순서다.
import xml.etree.ElementTree as ET
from WhereToUseDisasterAssistanceFund.getMapData import *
from urllib.parse import quote_plus


def GetDataFromURL(treelist, typeList):
    indexNum = 1

    while indexNum != 11:
        url = "https://openapi.gg.go.kr/RegionMnyFacltStus?KEY=a7f5f144889643fcab0acf9caf2eccf8&pIndex=" \
              + indexNum.__str__() + "&psize=1000&SIGUN_CD=41390"

        request = ul.Request(url)  # url 데이터 요청
        response = ul.urlopen(request)  # 요청받은 데이터 열어줌
        res = response.getcode()  # 제대로 데이터가 수신됐는지 확인하는 코드 성공시 200

        if res == 200:
            responseData = response.read()
            tree = ET.fromstring(responseData)

            for node in tree:
                n_name = node.findtext('CMPNM_NM')  # 상호명
                n_indutype = node.findtext('INDUTYPE_NM')  # 업종명
                if n_indutype is not None:
                    typeList.add(n_indutype)
                n_road_addr = node.findtext('REFINE_ROADNM_ADDR')  # 도로명주소
                n_lotno_addr = node.findtext('REFINE_LOTNO_ADDR')  # 지번주소
                n_lat = node.findtext('REFINE_WGS84_LAT')  # 위도
                n_logt = node.findtext('REFINE_WGS84_LOGT')  # 경도
                n_callNumber = node.findtext('TELNO')
                data = [n_name, n_indutype, n_road_addr, n_callNumber, n_lotno_addr, n_lat, n_logt]
                treelist.append(data)

        indexNum += 1


def showPlace(p_name):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/xml?&key=AIzaSyDKHC9dJVkD4MZt_c-aL1EUe5TRmdsRWtc&language=ko&query="\
          + quote_plus(p_name)

    request = ul.Request(url)
    response = ul.urlopen(request)
    res = response.getcode()

    if res == 200:
        responseData = response.read()
        tree = ET.fromstring(responseData)

        for node in tree:
            n_name = node.findtext('name')  # 상호명
            n_road_addr = node.findtext('formatted_address')  # 도로명주소
            n_rating = node.findtext('rating')  # 평점
            n_photo = node.findtext('photo_reference')  # 사진
            n_place_id = node.findtext('place_id')  # place_id

            data = [n_name, n_road_addr, n_rating, n_photo, n_place_id]
            print(data[0], data[1], data[2], data[3])


class MainScene(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.infoTreeview = ttk.Treeview(self, columns=["one", "two", "three", "four", "구주소", "위도", "경도", ],
                                         displaycolumns=["one", "two", "three"])
        self.vbar = Scrollbar(self.infoTreeview, orient=VERTICAL)
        self.typeList = set()
        self.treelist = list()
        self.searchButtonImg = PhotoImage(file="searchbutton.png")
        self.resetButtonImg = PhotoImage(file="resetbutton.png")
        self.th1 = Thread(target=GetDataFromURL, args=(self.treelist, self.typeList))
        self.th1.start()

        self.dong = set()
        self.searchFrame = Frame(self)

        # 원정
        self.topFrame = Frame(master)

        # map
        self.log = 37.5492077
        self.logt = 127.1464824

        self.map_image = showMap(self.log, self.logt, 17)
        self.map = ttk.Label(self.topFrame, image=self.map_image)
        self.map.pack()

        self.DongFrame = Frame(self.searchFrame, height=10)
        self.TypeFrame = Frame(self.searchFrame, height=10)
        self.SearchBarFrame = Frame(self.searchFrame, height=10)

        # Place 정보

        self.DongFrame = Frame(self.searchFrame, height=15, bg="white")
        self.TypeFrame = Frame(self.searchFrame, height=15, bg="white")
        self.SearchBarFrame = Frame(self.searchFrame, height=15, bg="white")

        self.setinfoTreeview()
        self.searchBar = Entry(self.SearchBarFrame,font=('08서울남산체 L', 12))

        self.restartButton = Button(self.searchFrame, image=self.resetButtonImg, command=self.inputData, bg="white")
        self.searchButton = Button(self.searchFrame, image=self.searchButtonImg, command=self.search, bg="white")

        self.typeComboBox = ttk.Combobox(self.TypeFrame, width=12, height=5, textvariable=str, font=('08서울남산체 L', 12))
        self.dongComboBox = ttk.Combobox(self.DongFrame, width=10, height=5, textvariable=str, font=('08서울남산체 L', 12))

        self.hintDongList = Label(self.DongFrame, text="동", width=10, height=1, bg="white", font=('08서울남산체 L', 18))
        self.hintTypeList = Label(self.TypeFrame, text="업종", width=10, height=1, bg="lightyellow",
                                  font=('08서울남산체 L', 18))
        self.hintSearchList = Label(self.SearchBarFrame, text="검색", width=10, height=1, bg="yellow",
                                    font=('08서울남산체 L', 18))

        # setting
        self.setTypeCombobox()
        self.setDongCombobox()
        self.positioning()

    def setTypeCombobox(self):
        typeList = list(self.typeList)
        typeList.sort()
        typeList.insert(0, "")
        self.typeComboBox['values'] = typeList
        self.typeComboBox.current(0)

    def setinfoTreeview(self):
        self.infoTreeview = self.inputData()
        self.vbar.pack(side=RIGHT, fill=Y)
        self.vbar.config(command=self.infoTreeview.yview)
        # 표와 스크롤바 연동
        self.infoTreeview.config(yscrollcommand=self.vbar.set)
        self.infoTreeview.pack(side=BOTTOM, expand=True, fill=BOTH)
        # 각 컬럼 설정. 컬럼 이름, 컬럼 넓이, 정렬 등
        self.infoTreeview.column("#0", width=50, )
        self.infoTreeview.heading("#0", text="번호", anchor="center")
        self.infoTreeview.column("#1", width=200, anchor="center")
        self.infoTreeview.heading("one", text="가게이름", anchor="center")
        self.infoTreeview.column("#2", width=200, anchor="center")
        self.infoTreeview.heading("two", text="업종명", anchor="center")
        self.infoTreeview.column("#3", width=300, anchor="center")
        self.infoTreeview.heading("three", text="주소", anchor="center")
        self.infoTreeview.bind("<Double-1>", self.selected)

    def setDongCombobox(self):
        dongList = set()
        for i in range(len(self.treelist)):
            if self.treelist[i][0] is not None:
                dongName = self.treelist[i][4].split()
                if len(dongName) >= 2 and str(dongName[2]).__contains__("동"):
                    dongList.add(dongName[2])
        dongList = list(dongList)
        dongList.sort()
        dongList.insert(0, "")
        self.dongComboBox['values'] = dongList
        self.dongComboBox.current(0)

    def positioning(self):
        self.topFrame.pack(side=TOP, expand=FALSE, fill=BOTH)
        self.map.pack(side=LEFT, expand=FALSE, fill=X)
        self.restartButton.pack(side=RIGHT, expand=FALSE, fill=X)
        self.searchButton.pack(side=RIGHT, expand=FALSE, fill=X)

        self.searchBar.pack(side=BOTTOM, expand=TRUE, fill=X)
        self.typeComboBox.pack(side=BOTTOM, expand=FALSE, fill=X)
        self.dongComboBox.pack(side=BOTTOM, expand=FALSE, fill=X)

        self.hintTypeList.pack(side=TOP, expand=FALSE, fill=X)
        self.hintDongList.pack(side=TOP, expand=FALSE, fill=X)
        self.hintSearchList.pack(side=TOP, expand=TRUE, fill=X)

        self.SearchBarFrame.pack(side=RIGHT, expand=TRUE, fill=X)
        self.TypeFrame.pack(side=RIGHT, expand=FALSE, fill=X)
        self.DongFrame.pack(side=RIGHT, expand=FALSE, fill=X)
        self.searchFrame.pack(side=BOTTOM, expand=FALSE, fill=X)

    # 표에 데이터 삽입
    def search(self):
        x = self.infoTreeview.get_children()
        for item in x:
            self.infoTreeview.delete(item)

        for i in range(len(self.treelist)):
            if self.treelist[i][0] is not None:
                if str(self.treelist[i][0]).__contains__(self.searchBar.get()) and str(
                        self.treelist[i][1]).__contains__(
                    self.typeComboBox.get()) \
                        and str(self.treelist[i][4]).__contains__(self.dongComboBox.get()):
                    self.infoTreeview.insert('', 'end', text=i, values=self.treelist[i], iid=str(i) + "번")

    def inputData(self):
        self.th1.join()
        x = self.infoTreeview.get_children()
        for item in x:
            self.infoTreeview.delete(item)
        for i in range(len(self.treelist)):
            if self.treelist[i][0] is not None:
                self.infoTreeview.insert('', 'end', text=i, values=self.treelist[i], iid=str(i) + "번")
        return self.infoTreeview

    def selected(self, e):
        selectedItem = self.infoTreeview.item(self.infoTreeview.selection())['values']
        print(selectedItem)

        self.map_image = showMap(selectedItem[5], selectedItem[6], 17)
        self.map.config(image=self.map_image)
        self.map.image = self.map_image
        showPlace(selectedItem[0])





