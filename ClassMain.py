from threading import Thread
from tkinter import ttk

# ﻿표 생성하기. colums는 컬럼 이름, displaycolums는 실행될 때 보여지는 순서다.
import xml.etree.ElementTree as ET
from WhereToUseDisasterAssistanceFund.getMapData import *

from urllib.parse import quote_plus
import urllib.request as ul
from site_packages.PIL import ImageTk, Image


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


def getPlace(p_name):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/xml?&key=AIzaSyDKHC9dJVkD4MZt_c-aL1EUe5TRmdsRWtc&language=ko&query=" \
          + quote_plus(p_name)

    request = ul.Request(url)
    response = ul.urlopen(request)
    res = response.getcode()

    if res == 200:
        responseData = response.read()
        Data = ET.fromstring(responseData)

        tree = Data.iter("result")
        tree2 = Data.iter("photo")

        m_photo = "CnRtAAAATLZNl354RwP_9UKbQ_5Psy40texXePv4oAlgP4qNEkdIrkyse7rPXYGd9D_Uj1rVsQdWT4oRz4QrYAJNpFX7rzqqMlZw2h2E2y5IKMUZ7ouD_SlcHxYq1yL4KbKUv3qtWgTK0A6QbGh87GB3sscrHRIQiG2RrmU_jF4tENr9wGS_YxoUSSDrYjWmrNfeEHSGSc3FyhNLlBU"

        for node in tree:
            n_name = node.findtext('name')  # 상호명
            n_road_addr = node.findtext('formatted_address')  # 도로명주소
            n_rating = node.findtext('rating')  # 평점
            for node2 in tree2:
                m_photo = node2.findtext('photo_reference')

            data = [n_name, n_road_addr, n_rating, m_photo]
            print(data)
            return data


def getPhoto(photo_reference):
    url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyDKHC9dJVkD4MZt_c-aL1EUe5TRmdsRWtc&photoreference=" \
          + photo_reference.__str__()

    with urllib.request.urlopen(url) as u:
        raw_data = u.read()
    im = Image.open(BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)

    return image


class MainScene(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.infoTreeview = ttk.Treeview(self, columns=["one", "two", "three", "four", "구주소", "위도", "경도", ],
                                         displaycolumns=["one", "two", "three"])
        self.vbar = Scrollbar(self.infoTreeview, orient=VERTICAL)
        self.typeList = set()
        self.treelist = list()
        self.th1 = Thread(target=GetDataFromURL, args=(self.treelist, self.typeList))
        self.th1.start()

        self.dong = set()
        self.searchFrame = Frame(self)

        self.topFrame = Frame(master)

        # map
        self.log = 37.5492077
        self.logt = 127.1464824

        self.map_image = showMap(self.log, self.logt, 17)
        self.map = Label(self.topFrame, image=self.map_image)

        self.DongFrame = Frame(self.searchFrame, height=10)
        self.TypeFrame = Frame(self.searchFrame, height=10)
        self.SearchBarFrame = Frame(self.searchFrame, height=10)

        # Place 정보
        self.name = '산기대'
        self.addr = ''
        self.rate = ''
        self.photo = getPhoto(
            'CnRtAAAATLZNl354RwP_9UKbQ_5Psy40texXePv4oAlgP4qNEkdIrkyse7rPXYGd9D_Uj1rVsQdWT4oRz4QrYAJNpFX7rzqqMlZw2h2E2y5IKMUZ7ouD_SlcHxYq1yL4KbKUv3qtWgTK0A6QbGh87GB3sscrHRIQiG2RrmU_jF4tENr9wGS_YxoUSSDrYjWmrNfeEHSGSc3FyhNLlBU')

        self.p_name = Label(self.topFrame, text=self.name)
        self.p_addr = Label(self.topFrame, text=self.addr)
        self.p_rating = Label(self.topFrame, text=self.rate)
        self.p_photo = Label(self.topFrame, image=self.photo, width=500, height=500)

        self.setinfoTreeview()
        self.searchBar = Entry(self.SearchBarFrame)

        self.restartButton = Button(self.searchFrame, text="리셋", command=self.inputData)
        self.searchButton = Button(self.searchFrame, text="검색", command=self.search)

        self.typeComboBox = ttk.Combobox(self.TypeFrame, width=12, height=5, textvariable=str)
        self.dongComboBox = ttk.Combobox(self.DongFrame, width=10, height=5, textvariable=str)

        self.hintDongList = Label(self.DongFrame, text="동 이름", width=10, height=1)
        self.hintTypeList = Label(self.TypeFrame, text="업종", width=10, height=1)
        self.hintSearchList = Label(self.SearchBarFrame, text="검색창", width=10, height=1)

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
        self.p_photo.pack(side=TOP, expand=FALSE, fill=X)
        self.p_name.pack(side=TOP, expand=FALSE, fill=X)
        self.p_addr.pack(side=TOP, expand=FALSE, fill=X)
        self.p_rating.pack(side=TOP, expand=FALSE, fill=X)

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

        place = getPlace(selectedItem[0])
        self.photo = getPhoto(place[3])

        self.p_name.config(text=place[0])
        self.p_addr.config(text=place[1])
        self.p_rating.config(text=place[2])
        self.p_photo.config(image=self.photo)
