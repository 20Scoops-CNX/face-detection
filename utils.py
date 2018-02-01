import requests
from io import BytesIO
from Tkinter import *
from PIL import ImageTk, Image

base_url = 'https://s3.amazonaws.com/test-face-rekognition/'
root = Tk()
ponds = ['example-image.jpg', 'example-image1.jpg','example-image2.jpg','example-image3.jpg','example-image4.jpg']

def show_image(file_name) :
    if any(file_name in s for s in ponds):
        file_name = 'jedsada.jpg'
    response = requests.get(base_url + file_name)
    root.title(file_name.replace('.jpg',''))
    img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)))
    panel = Label(root, image = img)
    panel.pack(side = "bottom", fill = "both", expand = "yes")
    root.mainloop()
