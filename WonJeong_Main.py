import urllib.request as ul
import xml.etree.ElementTree as ET
from urllib.request import urlopen

open_api_key = "a7f5f144889643fcab0acf9caf2eccf8"
params = "&pIndex=1&psize=100&SIGUN_NM=%EC%8B%9C%ED%9D%A5%EC%8B%9C"
url = "https://openapi.gg.go.kr/RegionMnyFacltStus?KEY=" + open_api_key + params

request = ul.Request(url)
# url 데이터 요청

response = ul.urlopen(request)
# 요청받은 데이터 열어줌

res = response.getcode()
# 제대로 데이터가 수신됐는지 확인하는 코드 성공시 200

rows = []

if res == 200:
    responseData = response.read()

    tree = ET.fromstring(responseData)

    for node in tree:
        n_xmp = node.findtext('CMPNM_NM')
        n_in = node.findtext('INDUTYPE_NM')
        n_add = node.findtext('REFINE_ROADNM_ADDR')
        n_lat = node.findtext('REFINE_WGS84_LAT')
        n_log = node.findtext('REFINE_WGS84_LOGT')

        rows.append({
            "상호명 : ": n_xmp,
            "업종명 : ": n_in,
            "주소 : ": n_add,
            "위도 : ": n_lat,
            "경도 : ": n_log
        })

for a in rows:
    print(a)

