from PIL import Image, ImageDraw
from Crypt import cryptXOR
import hashlib

class Container:
    ByteList = []

    def __init__(self, path):
        self.path = path
        self.image = Image.open(self.path)
        self.draw = ImageDraw.Draw(self.image)
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.pix = self.image.load()

    # Load pixel values
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

    # Read 4 * bytesAmount items in self.ByteList and return int value
    def readByte(self, shift, bytesAmount = 1):
        byteSize = 8
        posParameter = int(byteSize / 2) * shift
        byte = 0
        for i in range(posParameter, posParameter + int(byteSize / 2) * bytesAmount):
            byte <<= 2
            byte += self.ByteList[i] & 0b11
        return byte

    # Read bytesAmount chars and return string
    def readString(self, shift, bytesAmount = 1):
        string = ""
        for i in range(0, bytesAmount):
            string +=  chr(self.readByte(shift + i))
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
    # InputObject - bytearray or int
    # Return list with 0-3 values
    def __init__(self, InputObject, bytesAmount = 1):
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

    # Write bitList to last 2 bits of every byte of Container.ByteList
    def write(self, Container, shift):
        for i in range(0, len(self.bitList)):
            Container.ByteList[shift + i] = (Container.ByteList[shift + i] & 0b11111100) | self.bitList[i]

# Desteganography function
def desteg(containerName, UseCryptography = False, CryptoPassword = ""):
    # Load picture container
    picture = Container(containerName)

    byteSize = 8

    # Read service information from file and encoded data
    picture.initializeByteList(int(byteSize / 2))
    extensionSize = picture.readByte(shift=0)

    picture.initializeByteList(int(byteSize / 2) * (extensionSize + 1))
    extension = picture.readString(shift=1, bytesAmount=extensionSize)

    picture.initializeByteList(int(byteSize / 2) * (extensionSize + 1 + 4))
    steganingFileSize = picture.readByte(shift=extensionSize + 1, bytesAmount=4)

    picture.initializeByteList(int(byteSize / 2) * (extensionSize + 1 + 4 + steganingFileSize))
    steganingFile = picture.readString(shift=extensionSize + 1 + 4, bytesAmount=steganingFileSize)

    if extension:
        extension = "." + extension

    steganingFile = bytes(steganingFile, encoding="iso8859-1")

    if UseCryptography:
        passwdhash = hashlib.sha256()
        passwdhash.update(CryptoPassword.encode())
        steganingFile = cryptXOR(steganingFile, passwdhash.hexdigest())

    steganingFile = bytearray(steganingFile)

    try:
        file = open(picture.path[:picture.path.rindex("/") + 1] + "out" + extension, 'wb')
    except ValueError:
        file = open("out" + extension, 'wb')
    file.write(steganingFile)
    file.close()

    return "Decoded as out" + extension

# Steganography function
def steg(containerName, steganingFileName, UseCryptography = False, CryptoPassword =""):

    picture = Container(containerName) # Load picture container
    steganingFile = SteganingFile(steganingFileName) # Load file
    if UseCryptography:
        passwdhash = hashlib.sha256()
        passwdhash.update(CryptoPassword.encode())
        steganingFile.Bytes = cryptXOR(steganingFile.Bytes, passwdhash.hexdigest())

    extensionSizeBitPairs = BitPairs(len(steganingFile.extension))
    extensionBitPairs = BitPairs(bytes(steganingFile.extension, encoding="UTF-8"))
    steganingFileSizeBitPairs = BitPairs(len(steganingFile.Bytes), bytesAmount=4)

    requiredLength = len(extensionSizeBitPairs.bitList) +\
                     len(extensionBitPairs.bitList) +\
                     len(steganingFileSizeBitPairs.bitList) +\
                     len(steganingFile.Bytes) * 4

    if picture.height * picture.width * 3 >= requiredLength:
        steganingFileBitPairs = BitPairs(steganingFile.Bytes)

        picture.initializeByteList(requiredLength)
        extensionSizeBitPairs.write(picture, 0)
        extensionBitPairs.write(picture, len(extensionSizeBitPairs.bitList))
        steganingFileSizeBitPairs.write(picture, len(extensionSizeBitPairs.bitList) + len(extensionBitPairs.bitList))
        steganingFileBitPairs.write(picture, len(extensionSizeBitPairs.bitList) + len(extensionBitPairs.bitList) + len(steganingFileSizeBitPairs.bitList))

        #Write pixels to picture
        k = 0
        i = 0
        while i < picture.width and k < requiredLength:
            j = 0
            while j < picture.height and k < requiredLength:
                picture.draw.point((i, j), (picture.ByteList[k], picture.ByteList[k + 1], picture.ByteList[k + 2]))
                k += 3
                j += 1
            i += 1
        picture.image.save(picture.path[:picture.path.rindex(".")] + "_steg" + ".png")
        return "Encoded as " + picture.path[picture.path.rindex("/") + 1: ] + "_steg" + ".png"
    else:
        return "Not enough space"