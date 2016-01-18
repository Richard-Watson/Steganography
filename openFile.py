file = open('IRremote.zip', 'rb')
originalFile = bytearray(file.read())
file.close()
dividedFile = []
for i in range(0, len(originalFile)):
    dividedFile.append((originalFile[i] & 0b11000000) >> 6)
    dividedFile.append((originalFile[i] & 0b110000) >> 4)
    dividedFile.append((originalFile[i] & 0b1100) >> 2)
    dividedFile.append(originalFile[i] & 0b11)
