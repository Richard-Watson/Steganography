from PIL import Image, ImageDraw

# Принимает bytearray или int, возвращает list значений 0-3
def ByteToBitPairs(Input, byteAmount = 1):
    Output = []
    byteSize = 8
    shift = int(byteSize / 2 - 1) * 2
    if type(Input) is bytearray:
        for i in range(0, len(Input)):
            for j in range(0, int(byteSize / 2)):
                Output.append((Input[i] & (0b11000000 >> j * 2)) >> shift - j * 2)

    elif type(Input) is int:
        if byteAmount == 4:
            shift = byteSize * 4 - 2
            for i in range(0, byteSize * 2):
                Output.append((Input & (0b11000000000000000000000000000000 >> i * 2)) >> shift - i * 2)
        elif byteAmount == 1:
            for i in range(0, int(byteSize / 2)):
                Output.append((Input & (0b11000000 >> i * 2)) >> shift - i * 2)

    return Output

# Возвращает list значений 0-255 (цвета пикселей)
def getContainerList(pix, width, height, requiredLength):
    ContainerList = []
    i = 0
    while i < width and len(ContainerList) < requiredLength or len(ContainerList) % 3:
        j = 0
        while j < height and len(ContainerList) < requiredLength or len(ContainerList) % 3:
            color = 0
            while color < 3 and len(ContainerList) < requiredLength or len(ContainerList) % 3:
                ContainerList.append(pix[i, j][color])
                color += 1
            j += 1
        i += 1
    return ContainerList

# Записывает в последние 2 бита каждого байта ContainerList значения из bitList, начиная со смещения shift
def writeLSB(ContainerList, bitList, shift = 0):
    for i in range(0, len(bitList)):
        ContainerList[shift + i] = (ContainerList[shift + i] & 0b11111100) | bitList[i]


def steg(container, hideFile):

    # Загружаем изображение-контейнер
    image = Image.open(container)  # Открываем изображение
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
    width = image.size[0]  # Определяем ширину
    height = image.size[1]  # Определяем высоту
    pix = image.load()  # Выгружаем значения пикселей

    file = open(hideFile, "rb")
    stegFileList = bytearray(file.read())
    file.close()

    try:
        extensionList = ByteToBitPairs(bytearray(bytes(hideFile[hideFile.rindex(".") + 1:], encoding ='utf-8')))
    except ValueError:
        extensionList = ByteToBitPairs(bytearray(bytes("", encoding ='utf-8')))
    extensionListSize = ByteToBitPairs(len(extensionList))
    stegFileList = ByteToBitPairs(stegFileList)
    stegFileListSize = ByteToBitPairs(len(stegFileList), 4)
    requiredLength = len(extensionListSize) + len(extensionList) + len(stegFileListSize) + len(stegFileList)

    if height * width * 3 >= requiredLength:
        ContainerList = getContainerList(pix, width, height, requiredLength)
        writeLSB(ContainerList, extensionListSize)
        writeLSB(ContainerList, extensionList, len(extensionListSize))
        writeLSB(ContainerList, stegFileListSize, len(extensionListSize) + len(extensionList))
        writeLSB(ContainerList, stegFileList, len(extensionListSize) + len(extensionList) + len(stegFileListSize))

        color = 0
        i = 0
        while i < width and color < requiredLength:
            j = 0
            while j < height and color < requiredLength:
                draw.point((i, j), (ContainerList[color], ContainerList[color + 1], ContainerList[color + 2]))
                color += 3
                j += 1
            i += 1
        image.save(container)
        return True
    else:
        return False
