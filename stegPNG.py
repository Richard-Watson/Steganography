from PIL import Image, ImageDraw
from Crypto import crypt
import hashlib

class Container:
    def __init__(self, path):
        self.path = path
        self.image = Image.open(self.path)
        self.draw = ImageDraw.Draw(self.image)
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.pix = self.image.load()

class SteganedFile:
    def __init__(self, path):
        self.path = path
        file = open(self.path, "rb")
        self.Bytes = file.read()
        file.close()

        try:
            self.extension = self.path[self.path.rindex(".") + 1:]
        except ValueError:
            self.extension = ""

        del self.path

class BitPairs:
    def __init__(self, InputObject, bytesAmount = 1): # Принимает bytearray или int, возвращает list значений 0-3
        self.Array = []
        byteSize = 8
        shift = byteSize * bytesAmount - 2
        if type(InputObject) is bytes or type(InputObject) is bytearray:
            for i in range(0, len(InputObject)):
                for j in range(0, int(byteSize / 2)):
                    self.Array.append((InputObject[i] & (0b11 << shift - j * 2)) >> shift - j * 2)
        elif type(InputObject) is int:
            for i in range(0, int(shift / 2) + 1):
                self.Array.append((InputObject & (0b11 << shift - i * 2)) >> shift - i * 2)

container = Container("me.png")
steganoFile = SteganedFile("sherlock.torrent")
steganoFile = BitPairs(steganoFile.Bytes)
print(True)

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

def readLSB(ContainerList, shift = 0, bytesAmount = 1):
    byteSize = 8
    byte = 0
    for i in range(int(byteSize / 2 * shift), int(byteSize / 2 * shift) + int(byteSize / 2) * bytesAmount):
        byte <<= 2
        byte += ContainerList[i] & 0b11
    return byte

def getString(ContainerList, shift, bytesAmount = 1):
    string = ""
    for i in range(0, bytesAmount):
        string += chr(readLSB(ContainerList, shift + i))
    return string

def desteg(container, UseCryptography = True, CryptoPassword = ""):
    # Загружаем изображение-контейнер
    image = Image.open(container)  # Открываем изображение
    width = image.size[0]  # Определяем ширину
    height = image.size[1]  # Определяем высоту
    pix = image.load()  # Выгружаем значения пикселей

    byteSize = 8

    ContainerList = getContainerList(pix, width, height, int(byteSize / 2))
    extensionSize = readLSB(ContainerList)

    ContainerList = getContainerList(pix, width, height, int(byteSize / 2) + extensionSize)
    extension = getString(ContainerList, 1, int(extensionSize / 4))
    if extension:
        extension = "." + extension

    ContainerList = getContainerList(pix, width, height, int(byteSize / 2) * 5 + extensionSize)
    fileSize = readLSB(ContainerList, 1 + int(extensionSize / 4), 4)

    ContainerList = getContainerList(pix, width, height, int(byteSize / 2) * 5 + extensionSize + fileSize)
    fileData = getString(ContainerList, 1 + int(extensionSize / 4) + 4, int(fileSize / 4))
    fileData = bytes(fileData, encoding="iso8859-1")

    WrongPasswd = False
    if UseCryptography:
        passwdhash = hashlib.sha256()
        passwdhash.update(CryptoPassword.encode())
        try:
            fileData = bytearray(crypt(fileData, passwdhash.hexdigest(), False))
        except:
            WrongPasswd = True
    else:
        fileData = bytearray(fileData)
    if not WrongPasswd:
        file = open('out' + extension, 'wb')
        file.write(fileData)
        file.close()

    print("done")

def steg(containerName, steganoFileName, UseCryptography = True, CryptoPassword = ""):

    # Загружаем изображение-контейнер
    container = Container(containerName)
    steganoFile = SteganedFile(steganoFileName)

    if UseCryptography:
        passwdhash = hashlib.sha256()
        passwdhash.update(CryptoPassword.encode())
        stegFileList = crypt(stegFileList, passwdhash.hexdigest())
    stegFileList = bytearray(stegFileList)

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
        image.save(container[:-4] + "_steg" + container[-4:])
        return True
    else:
        return False
