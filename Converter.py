from PIL import Image

def ConvertToPNG(path):
    image = Image.open(path) #Открываем изображение.
    image.save(path[:path.rindex(".") + 1] + "png")