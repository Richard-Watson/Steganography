import random
from PIL import Image, ImageDraw
from openFile import dividedFile

mode = int(input('mode:')) #Считываем номер преобразования.
image = Image.open("temp.jpg") #Открываем изображение.
draw = ImageDraw.Draw(image) #Создаем инструмент для рисования.
width = image.size[0] #Определяем ширину.
height = image.size[1] #Определяем высоту.
pix = image.load() #Выгружаем значения пикселей.

if (mode == 0):
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a + b + c) // 3
            draw.point((i, j), (S, S, S))
image.save("ans.jpg", "JPEG")
del draw
