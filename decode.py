from PIL import Image, ImageDraw

image = Image.open("ans1.jpg") #Открываем изображение.
draw = ImageDraw.Draw(image) #Создаем инструмент для рисования.
width = image.size[0] #Определяем ширину.
height = image.size[1] #Определяем высоту.
pix = image.load() #Выгружаем значения пикселей.

originalFileRGB = []
for i in range(width):
    for j in range(height):
        for color in range(0, 3):
            originalFileRGB.append(pix[i, j][color])

letter = 0
message = ""
for j in range(0, 4):
    letter <<= 2
    letter += originalFileRGB[j + i] & 0b11
message += chr(letter)
crypt_byte = bytearray(bytes(message, encoding="utf-8"))

f = open('out', 'wb')
f.write(crypt_byte)
f.close()
