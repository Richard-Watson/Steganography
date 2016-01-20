from PIL import Image, ImageDraw

def getDividedFile(filename):

    file = open(filename, "rb")
    originalFile = bytearray(file.read())
    file.close()

    dividedFile = []
    for i in range(0, len(originalFile)):
        dividedFile.append((originalFile[i] & 0b11000000) >> 6)
        dividedFile.append((originalFile[i] & 0b110000) >> 4)
        dividedFile.append((originalFile[i] & 0b1100) >> 2)
        dividedFile.append(originalFile[i] & 0b11)
    return dividedFile

def getContainerArray(pix, width, height, length):
    ContainerArray = []
    i = 0
    while i < width and len(ContainerArray) < length or len(ContainerArray) % 3:
        j = 0
        while j < height and len(ContainerArray) < length or len(ContainerArray) % 3:
            color = 0
            while color < 3 and len(ContainerArray) < length or len(ContainerArray) % 3:
                ContainerArray.append(pix[i, j][color])
                color += 1
            j += 1
        i += 1
    return ContainerArray

def writeLSB(ContainerArray, dividedFile, stegInfoSize):
    for i in range(0, len(dividedFile)):
        ContainerArray[stegInfoSize + i] = (ContainerArray[stegInfoSize + i] & 0b11111100) + dividedFile[i]

def steg(container, hideFile):
    image = Image.open(container)  # Открываем изображение
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
    width = image.size[0]  # Определяем ширину
    height = image.size[1]  # Определяем высоту
    pix = image.load()  # Выгружаем значения пикселей

    stegInfoSize = 5 * 4
    dividedFile = getDividedFile(hideFile)

    if height * width * 3 >= len(dividedFile) + stegInfoSize:
        originalFileRGB = getContainerArray(pix, width, height, len(dividedFile) + stegInfoSize)
        writeLSB(originalFileRGB, dividedFile, stegInfoSize)

        color = 0
        i = 0
        while i < width and color < len(dividedFile) + stegInfoSize:
            j = 0
            while j < height and color < len(dividedFile) + stegInfoSize:
                draw.point((i, j), (originalFileRGB[color], originalFileRGB[color + 1], originalFileRGB[color + 2]))
                color += 3
                j += 1
            i += 1
        image.save(container)
        return True
    else:
        return False
