# google 인증키 : AIzaSyA8FMjUnTuZ_9wOse0NJS8TdEbNQP7yzHo

import urllib.request as ul
from tkinter import *
from io import BytesIO
import urllib
from PIL import ImageTk, Image


def showMap(m_lat, m_logt):
    url = "https://maps.googleapis.com/maps/api/staticmap?center=" + m_lat.__str__() + "," + m_logt.__str__() \
          + "&markers=color:red%7Clabel:S%7C" + m_lat.__str__() + "," + m_logt.__str__() \
          + "&zoom=17&size=550x550&maptype=roadmap&key=AIzaSyA8FMjUnTuZ_9wOse0NJS8TdEbNQP7yzHo"

    with urllib.request.urlopen(url) as u:
        raw_data = u.read()
    im = Image.open(BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)

    return image

