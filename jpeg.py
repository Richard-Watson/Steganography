from PIL import Image, ImageDraw
from openFile import dividedFile

image = Image.open('ans1.png')  # Открываем изображение
draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load()  # Выгружаем значения пикселей

originalFileRGB = []
test = 0
for i in range(width):
    for j in range(height):
        for color in range(0, 3):
            originalFileRGB.append(pix[i, j][color])
for i in range(0, len(dividedFile)):
    originalFileRGB[i] = (originalFileRGB[i] & 0b11111100) + dividedFile[i]

color = 0
for i in range(width):
    for j in range(height):
        draw.point((i, j), (originalFileRGB[color], originalFileRGB[color + 1], originalFileRGB[color + 2]))
        color += 3

image.save("ans1.png")
del draw
