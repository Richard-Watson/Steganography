from stegPNG import steg, desteg

# здесь будет парсер
decode = 1
containerName = "me.png"
hideName = "me.jpg"

if not decode:
    if not steg(containerName, hideName, CryptoPassword="vfczyz"):
        print("Контейнер мал")
else:
    containerName = "me_steg.png"
    desteg(containerName, CryptoPassword="vfczyz")
