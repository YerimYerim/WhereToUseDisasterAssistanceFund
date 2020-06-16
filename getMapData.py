# google 인증키 : AIzaSyA8FMjUnTuZ_9wOse0NJS8TdEbNQP7yzHo

import urllib.request as ul
from tkinter import*
from io import BytesIO
import urllib
from site_packages.PIL import ImageTk, Image


root = Tk()
root.geometry("500x500+500+200")

gmaps_key = "AIzaSyA8FMjUnTuZ_9wOse0NJS8TdEbNQP7yzHo"
wido = "37.5728359"
geongdo = "126.9746922"

url = "https://maps.googleapis.com/maps/api/staticmap?center=" + wido + "," + geongdo \
    + "&markers=color:red%7Clabel:S%7C" + wido + "," + geongdo \
    + "&zoom=17&size=700x1000&maptype=roadmap&key=" + gmaps_key

with urllib.request.urlopen(url) as u:
    raw_data = u.read()
im = Image.open(BytesIO(raw_data))
image = ImageTk.PhotoImage(im)

label = Label(root, image=image, height=400, width=400)
label.pack()
label.place(x=0, y=0)

root.mainloop()
