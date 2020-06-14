import urllib.request as ul
import xml.etree.ElementTree as ET


def GetDataFromURL(row=list , Induutype = set):
    indexNum = 1

    while indexNum != 11:
        url = "https://openapi.gg.go.kr/RegionMnyFacltStus?KEY=a7f5f144889643fcab0acf9caf2eccf8&pIndex=" \
              + indexNum.__str__() + "&psize=1000&SIGUN_NM=%EC%8B%9C%ED%9D%A5%EC%8B%9C"

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
                    Induutype.add(n_indutype)
                n_road_addr = node.findtext('REFINE_ROADNM_ADDR')  # 도로명주소
                n_lotno_addr = node.findtext('REFINE_LOTNO_ADDR')  # 지번주소
                n_lat = node.findtext('REFINE_WGS84_LAT')  # 위도
                n_logt = node.findtext('REFINE_WGS84_LOGT')  # 경도
                n_callNumber = node.findtext('TELNO')
                data = [n_name, n_indutype, n_road_addr, n_callNumber, n_lotno_addr, n_lat, n_logt]
                row.append(data)

        indexNum = indexNum + 1

