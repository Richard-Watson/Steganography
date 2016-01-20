from PIL import Image, ImageDraw
from openFile import dividedFile


def stegano(container, hideFile):
    image = Image.open(container)  # Открываем изображение
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
    width = image.size[0]  # Определяем ширину
    height = image.size[1]  # Определяем высоту
    pix = image.load()  # Выгружаем значения пикселей

    if height * width * 3 >= len(dividedFile) + 5 * 4:
        originalFileRGB = []
        for i in range(width):
            for j in range(height):
                for color in range(0, 3):
                    if len(originalFileRGB) < len(dividedFile) + 5 * 4:
                        originalFileRGB.append(pix[i, j][color])
                    else:
                        if len(originalFileRGB) % 3:
                            originalFileRGB.append(pix[i, j][color])
                        break
        for i in range(0, len(dividedFile)):
            originalFileRGB[5 * 4 + i] = (originalFileRGB[5 * 4 + i] & 0b11111100) + dividedFile[i]
        color = 0
        for i in range(width):
            for j in range(height):
                if color < 24:
                    draw.point((i, j), (originalFileRGB[color], originalFileRGB[color + 1], originalFileRGB[color + 2]))
                    color += 3
                else:
                    break
        image.save(container)
        del draw
    else:
        print('Контейнер мал')
