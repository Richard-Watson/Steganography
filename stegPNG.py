from PIL import Image, ImageDraw
from Crypto import crypt
import hashlib

class Container:
    def __init__(self, path):
        self.image = Image.open(path)
        self.draw = ImageDraw.Draw(self.image)
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.pix = self.image.load()

    def initializeByteList(self, requiredLength):
        self.ByteList = []
        i = 0
        while i < self.width and len(self.ByteList) < requiredLength or len(self.ByteList) % 3:
            j = 0
            while j < self.height and len(self.ByteList) < requiredLength or len(self.ByteList) % 3:
                k = 0
                while k < 3 and len(self.ByteList) < requiredLength or len(self.ByteList) % 3:
                    self.ByteList.append(self.pix[i, j][k])
                    k += 1
                j += 1
            i += 1

    def readLSB(self, shift, bytesAmount = 1):
        byteSize = 8
        posParameter = int(byteSize / 2) * shift
        byte = 0
        for i in range(posParameter, posParameter + int(byteSize / 2) * bytesAmount):
            byte <<= 2
            byte += self.ByteList[i] & 0b11
        return byte

    def readString(self, shift, bytesAmount = 1):
        string = ""
        for i in range(0, bytesAmount):
            string +=  chr(self.readLSB(shift + i))
        return string

class SteganingFile:
    def __init__(self, path):
        file = open(path, "rb")
        self.Bytes = file.read()
        file.close()

        try:
            self.extension = path[path.rindex(".") + 1:]
        except ValueError:
            self.extension = ""

class BitPairs:
    def __init__(self, InputObject, bytesAmount = 1): # Принимает bytearray или int, возвращает list значений 0-3
        self.bitList = []
        byteSize = 8
        shift = byteSize * bytesAmount - 2
        if type(InputObject) is bytes or type(InputObject) is bytearray:
            for i in range(0, len(InputObject)):
                for j in range(0, int(byteSize / 2)):
                    self.bitList.append((InputObject[i] & (0b11 << shift - j * 2)) >> shift - j * 2)
        elif type(InputObject) is int:
            for i in range(0, int(shift / 2) + 1):
                self.bitList.append((InputObject & (0b11 << shift - i * 2)) >> shift - i * 2)

    def write(self, Container, shift):
        for i in range(0, len(self.bitList)):
            Container.ByteList[shift + i] = (Container.ByteList[shift + i] & 0b11111100) | self.bitList[i]

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

def steg(containerName, steganingFileName, UseCryptography = True, CryptoPassword =""):

    # Загружаем изображение-контейнер
    picture = Container(containerName)
    steganingFile = SteganingFile(steganingFileName)

    if UseCryptography:
        passwdhash = hashlib.sha256()
        passwdhash.update(CryptoPassword.encode())
        stegFileList = crypt(stegFileList, passwdhash.hexdigest())

    extensionSizeBitPairs = BitPairs(len(steganingFile.extension))
    extensionBitPairs = BitPairs(bytes(steganingFile.extension, encoding="UTF-8"))
    steganingFileSizeBitPairs = BitPairs(len(steganingFile.Bytes), bytesAmount=4)
    steganingFileBitPairs = BitPairs(steganingFile.Bytes)
    del steganingFile
    requiredLength = len(extensionSizeBitPairs.bitList) +\
                     len(extensionBitPairs.bitList) +\
                     len(steganingFileSizeBitPairs.bitList) +\
                     len(steganingFileBitPairs.bitList)

    if picture.height * picture.width * 3 >= requiredLength:
        picture.initializeByteList(requiredLength)
        extensionSizeBitPairs.write(picture, 0)
        writeLSB(ContainerList, extensionList, len(extensionListSize))
        writeLSB(ContainerList, steganingFileSizeBitPairs, len(extensionListSize) + len(extensionList))
        writeLSB(ContainerList, stegFileList, len(extensionListSize) + len(extensionList) + len(steganingFileSizeBitPairs))

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

steg("me.png", "sherlock.torrent", UseCryptography=False)